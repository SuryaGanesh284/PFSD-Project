from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
    TemplateView, FormView
)
from django.urls import reverse_lazy
from django.db.models import Q, Count, Avg
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import redirect
from django.utils import timezone
from datetime import timedelta
import random

from .models import (
    CustomUser, LearningModule, Quiz, Question, Choice,
    QuizAttempt, QuestionAnswer, DiscussionThread, Comment,
    CommentLike
)
from .forms import (
    CustomUserCreationForm, CustomUserChangeForm, LearningModuleForm,
    QuizForm, QuestionForm, ChoiceForm, DiscussionThreadForm,
    CommentForm, FilterModulesForm
)


# ==================== AUTHENTICATION VIEWS ====================

class RegisterView(CreateView):
    """User registration view."""
    form_class = CustomUserCreationForm
    template_name = 'core/auth/register.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Registration successful! Please log in.')
        return response


def login_view(request):
    """User login view."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'core/auth/login.html')


@login_required(login_url='login')
def logout_view(request):
    """User logout view."""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


# ==================== HOME & DASHBOARD VIEWS ====================

def home_view(request):
    """Home page with platform overview."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    context = {
        'total_modules': LearningModule.objects.filter(status='published').count(),
        'total_users': CustomUser.objects.count(),
        'recent_modules': LearningModule.objects.filter(status='published').order_by('-created_at')[:3],
    }
    return render(request, 'core/home.html', context)


@login_required(login_url='login')
def dashboard_view(request):
    """Role-based dashboard."""
    user = request.user
    
    if user.role == 'admin':
        return redirect('admin_dashboard')
    elif user.role == 'educator':
        return redirect('educator_dashboard')
    else:  # citizen
        return redirect('citizen_dashboard')


@login_required(login_url='login')
def admin_dashboard(request):
    """Admin dashboard with statistics."""
    if request.user.role != 'admin':
        return HttpResponseForbidden('Access denied.')
    
    context = {
        'total_users': CustomUser.objects.count(),
        'total_modules': LearningModule.objects.count(),
        'total_quizzes': Quiz.objects.count(),
        'total_attempts': QuizAttempt.objects.count(),
        'recent_users': CustomUser.objects.order_by('-created_at')[:5],
        'recent_modules': LearningModule.objects.order_by('-created_at')[:5],
    }
    return render(request, 'core/dashboard/admin_dashboard.html', context)


@login_required(login_url='login')
def educator_dashboard(request):
    """Educator dashboard with their content."""
    if request.user.role != 'educator':
        return HttpResponseForbidden('Access denied.')
    
    context = {
        'modules': LearningModule.objects.filter(created_by=request.user),
        'quizzes': Quiz.objects.filter(created_by=request.user),
        'total_attempts': QuizAttempt.objects.filter(quiz__created_by=request.user).count(),
        'avg_score': QuizAttempt.objects.filter(
            quiz__created_by=request.user,
            is_passed=True
        ).aggregate(Avg('percentage'))['percentage__avg'],
    }
    return render(request, 'core/dashboard/educator_dashboard.html', context)


@login_required(login_url='login')
def citizen_dashboard(request):
    """Citizen dashboard with learning progress."""
    if request.user.role != 'citizen':
        return HttpResponseForbidden('Access denied.')
    
    user_attempts = QuizAttempt.objects.filter(user=request.user)
    
    context = {
        'completed_quizzes': user_attempts.filter(is_passed=True).count(),
        'total_attempts': user_attempts.count(),
        'avg_score': user_attempts.filter(is_passed=True).aggregate(Avg('percentage'))['percentage__avg'],
        'recent_attempts': user_attempts.order_by('-started_at')[:5],
        'modules': LearningModule.objects.filter(status='published').order_by('-created_at')[:6],
    }
    return render(request, 'core/dashboard/citizen_dashboard.html', context)


# ==================== USER PROFILE VIEWS ====================

@login_required(login_url='login')
def profile_view(request, pk=None):
    """User profile view."""
    if pk is None:
        user = request.user
    else:
        user = get_object_or_404(CustomUser, pk=pk)
    
    context = {
        'profile_user': user,
        'is_own_profile': user == request.user,
    }
    
    if user.role == 'educator':
        context['modules_count'] = LearningModule.objects.filter(created_by=user).count()
        context['quizzes_count'] = Quiz.objects.filter(created_by=user).count()
    elif user.role == 'citizen':
        attempts = QuizAttempt.objects.filter(user=user)
        context['quizzes_attempted'] = attempts.count()
        context['passed_quizzes'] = attempts.filter(is_passed=True).count()
    
    return render(request, 'core/profile.html', context)


@login_required(login_url='login')
def edit_profile_view(request):
    """Edit user profile view."""
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    context = {'form': form}
    return render(request, 'core/edit_profile.html', context)


# ==================== LEARNING MODULE VIEWS ====================

class ModuleListView(ListView):
    """List all published learning modules."""
    model = LearningModule
    template_name = 'core/modules/module_list.html'
    context_object_name = 'modules'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = LearningModule.objects.filter(status='published').order_by('order', '-created_at')
        
        form = FilterModulesForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data.get('difficulty_level'):
                queryset = queryset.filter(difficulty_level=form.cleaned_data['difficulty_level'])
            if form.cleaned_data.get('search'):
                search = form.cleaned_data['search']
                queryset = queryset.filter(
                    Q(title__icontains=search) | Q(description__icontains=search)
                )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FilterModulesForm(self.request.GET)
        return context


class ModuleDetailView(DetailView):
    """View module details."""
    model = LearningModule
    template_name = 'core/modules/module_detail.html'
    context_object_name = 'module'
    slug_field = 'slug'
    
    def get_queryset(self):
        return LearningModule.objects.filter(status='published')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        module = self.get_object()
        context['quizzes'] = module.quizzes.filter(is_published=True)
        context['discussions'] = module.discussion_threads.all()
        return context


class ModuleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Create learning module (educators only)."""
    model = LearningModule
    form_class = LearningModuleForm
    template_name = 'core/modules/module_form.html'
    login_url = 'login'
    
    def test_func(self):
        return self.request.user.is_educator()
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Module created successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('module_detail', kwargs={'slug': self.object.slug})


class ModuleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update learning module (educators only)."""
    model = LearningModule
    form_class = LearningModuleForm
    template_name = 'core/modules/module_form.html'
    login_url = 'login'
    
    def test_func(self):
        module = self.get_object()
        return self.request.user.is_educator() and module.created_by == self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Module updated successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('module_detail', kwargs={'slug': self.object.slug})


# ==================== QUIZ VIEWS ====================

class QuizListView(ListView):
    """List all published quizzes."""
    model = Quiz
    template_name = 'core/quizzes/quiz_list.html'
    context_object_name = 'quizzes'
    paginate_by = 12
    
    def get_queryset(self):
        return Quiz.objects.filter(is_published=True).order_by('-created_at')


class QuizDetailView(DetailView):
    """View quiz details."""
    model = Quiz
    template_name = 'core/quizzes/quiz_detail.html'
    context_object_name = 'quiz'
    
    def get_queryset(self):
        return Quiz.objects.filter(is_published=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz = self.get_object()
        
        if self.request.user.is_authenticated:
            user_attempts = QuizAttempt.objects.filter(user=self.request.user, quiz=quiz)
            context['user_attempts'] = user_attempts.count()
            context['best_attempt'] = user_attempts.filter(is_passed=True).order_by('-percentage').first()
            context['can_attempt'] = True
            
            if quiz.max_attempts and user_attempts.count() >= quiz.max_attempts:
                context['can_attempt'] = False
        
        return context


class QuizCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Create quiz (educators only)."""
    model = Quiz
    form_class = QuizForm
    template_name = 'core/quizzes/quiz_form.html'
    login_url = 'login'
    
    def test_func(self):
        return self.request.user.is_educator()
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'created_by': self.request.user}
        return kwargs
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Quiz created successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('quiz_detail', kwargs={'pk': self.object.pk})


@login_required(login_url='login')
def quiz_take_view(request, pk):
    """Take a quiz."""
    quiz = get_object_or_404(Quiz, pk=pk, is_published=True)
    
    # Check if user can attempt
    if not request.user.is_citizen():
        messages.error(request, 'Only citizens can take quizzes.')
        return redirect('quiz_detail', pk=quiz.pk)
    
    # Check max attempts
    if quiz.max_attempts:
        attempts = QuizAttempt.objects.filter(user=request.user, quiz=quiz).count()
        if attempts >= quiz.max_attempts:
            messages.error(request, f'You have reached the maximum attempts ({quiz.max_attempts}).')
            return redirect('quiz_detail', pk=quiz.pk)
    
    # Get or create current attempt
    attempt = QuizAttempt.objects.filter(
        user=request.user,
        quiz=quiz,
        completed_at__isnull=True
    ).first()
    
    if not attempt:
        attempt = QuizAttempt.objects.create(user=request.user, quiz=quiz)
        attempt.total_possible_score = sum(q.points for q in quiz.questions.all())
        attempt.save()
    
    # Get questions
    questions = quiz.questions.all()
    if quiz.shuffle_questions:
        questions = list(questions)
        random.shuffle(questions)
    else:
        questions = questions.order_by('order')
    
    if request.method == 'POST':
        # Save answers
        for question in quiz.questions.all():
            field_name = f'question_{question.id}'
            choice_id = request.POST.get(field_name)
            
            if choice_id:
                choice = get_object_or_404(Choice, id=choice_id)
                answer, _ = QuestionAnswer.objects.update_or_create(
                    attempt=attempt,
                    question=question,
                    defaults={'selected_choice': choice, 'is_correct': choice.is_correct}
                )
        
        # Complete attempt
        attempt.completed_at = timezone.now()
        attempt.calculate_score()
        
        messages.success(request, 'Quiz submitted successfully!')
        return redirect('quiz_result', pk=attempt.pk)
    
    context = {
        'quiz': quiz,
        'attempt': attempt,
        'questions': questions,
        'question_count': quiz.questions.count(),
    }
    return render(request, 'core/quizzes/quiz_take.html', context)


class QuizResultView(DetailView):
    """View quiz results."""
    model = QuizAttempt
    template_name = 'core/quizzes/quiz_result.html'
    context_object_name = 'attempt'
    
    def get_queryset(self):
        return QuizAttempt.objects.filter(user=self.request.user, completed_at__isnull=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        attempt = self.get_object()
        context['answers'] = attempt.answers.all()
        context['quiz'] = attempt.quiz
        return context


# ==================== DISCUSSION FORUM VIEWS ====================

class DiscussionThreadListView(ListView):
    """List all discussion threads."""
    model = DiscussionThread
    template_name = 'core/discussions/thread_list.html'
    context_object_name = 'threads'
    paginate_by = 15
    
    def get_queryset(self):
        return DiscussionThread.objects.all().annotate(
            comment_count=Count('comments')
        ).order_by('-is_pinned', '-updated_at')


class DiscussionThreadDetailView(DetailView):
    """View discussion thread details."""
    model = DiscussionThread
    template_name = 'core/discussions/thread_detail.html'
    context_object_name = 'thread'
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.increment_views()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        thread = self.get_object()
        context['comments'] = thread.comments.filter(parent__isnull=True).order_by('-created_at')
        context['comment_form'] = CommentForm()
        return context


class DiscussionThreadCreateView(LoginRequiredMixin, CreateView):
    """Create discussion thread."""
    model = DiscussionThread
    form_class = DiscussionThreadForm
    template_name = 'core/discussions/thread_form.html'
    login_url = 'login'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Thread created successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('thread_detail', kwargs={'pk': self.object.pk})


class DiscussionThreadUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update discussion thread."""
    model = DiscussionThread
    form_class = DiscussionThreadForm
    template_name = 'core/discussions/thread_form.html'
    login_url = 'login'
    
    def test_func(self):
        thread = self.get_object()
        return thread.author == self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Thread updated successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('thread_detail', kwargs={'pk': self.object.pk})


@login_required(login_url='login')
def add_comment_view(request, thread_pk):
    """Add comment to discussion thread."""
    thread = get_object_or_404(DiscussionThread, pk=thread_pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.thread = thread
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('thread_detail', pk=thread.pk)
    
    return redirect('thread_detail', pk=thread.pk)


@login_required(login_url='login')
def like_comment_view(request, comment_pk):
    """Like a comment."""
    comment = get_object_or_404(Comment, pk=comment_pk)
    
    like, created = CommentLike.objects.get_or_create(comment=comment, user=request.user)
    
    if not created:
        like.delete()
        comment.likes_count = max(0, comment.likes_count - 1)
    else:
        comment.likes_count += 1
    
    comment.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'likes_count': comment.likes_count})
    
    return redirect('thread_detail', pk=comment.thread.pk)
