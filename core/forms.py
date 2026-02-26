from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from .models import (
    CustomUser, LearningModule, Quiz, Question, Choice,
    DiscussionThread, Comment, QuizAttempt, QuestionAnswer
)


class CustomUserCreationForm(UserCreationForm):
    """Form for creating new users with role selection."""
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email address'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name'
            }),
            'role': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
    
    def clean_email(self):
        """Validate that email is unique."""
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('This email is already registered.')
        return email


class CustomUserChangeForm(UserChangeForm):
    """Form for updating user profile."""
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'profile_image')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
        }


class LearningModuleForm(forms.ModelForm):
    """Form for creating and editing learning modules."""
    
    class Meta:
        model = LearningModule
        fields = ('title', 'slug', 'description', 'content', 'image', 'attachment',
                  'difficulty_level', 'estimated_time', 'status', 'order')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Module title'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'URL slug (auto-generated)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief description'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Module content'
            }),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'attachment': forms.FileInput(attrs={'class': 'form-control'}),
            'difficulty_level': forms.Select(attrs={'class': 'form-select'}),
            'estimated_time': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Minutes'
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Display order'
            }),
        }


class QuizForm(forms.ModelForm):
    """Form for creating and editing quizzes."""
    
    class Meta:
        model = Quiz
        fields = ('title', 'description', 'module', 'difficulty', 'passing_score',
                  'time_limit', 'shuffle_questions', 'show_answers', 'max_attempts', 'is_published')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Quiz title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Quiz description'
            }),
            'module': forms.Select(attrs={'class': 'form-select'}),
            'difficulty': forms.Select(attrs={'class': 'form-select'}),
            'passing_score': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '100'
            }),
            'time_limit': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Minutes (optional)'
            }),
            'max_attempts': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Unlimited if empty'
            }),
            'shuffle_questions': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'show_answers': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class QuestionForm(forms.ModelForm):
    """Form for creating and editing quiz questions."""
    
    class Meta:
        model = Question
        fields = ('text', 'question_type', 'order', 'explanation', 'points')
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Question text'
            }),
            'question_type': forms.Select(attrs={'class': 'form-select'}),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Question order'
            }),
            'explanation': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Explanation (optional)'
            }),
            'points': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Points for correct answer'
            }),
        }


class ChoiceForm(forms.ModelForm):
    """Form for creating and editing answer choices."""
    
    class Meta:
        model = Choice
        fields = ('text', 'is_correct', 'order')
        widgets = {
            'text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choice text'
            }),
            'is_correct': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Order'
            }),
        }


class DiscussionThreadForm(forms.ModelForm):
    """Form for creating and editing discussion threads."""
    
    class Meta:
        model = DiscussionThread
        fields = ('title', 'content', 'module')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Thread title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Share your thoughts...'
            }),
            'module': forms.Select(attrs={
                'class': 'form-select'
            }),
        }


class CommentForm(forms.ModelForm):
    """Form for adding comments to discussion threads."""
    
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write a comment...',
                'maxlength': '1000'
            }),
        }


class QuizAttemptForm(forms.Form):
    """Form for answering quiz questions."""
    
    def __init__(self, quiz, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.quiz = quiz
        self.questions = quiz.questions.all().order_by('order')
        
        for question in self.questions:
            if question.question_type == 'multiple_choice':
                choices = [(choice.id, choice.text) for choice in question.choices.all().order_by('order')]
                self.fields[f'question_{question.id}'] = forms.ChoiceField(
                    label=question.text,
                    choices=choices,
                    widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
                    required=False
                )
            elif question.question_type == 'true_false':
                choices = [('true', 'True'), ('false', 'False')]
                self.fields[f'question_{question.id}'] = forms.ChoiceField(
                    label=question.text,
                    choices=choices,
                    widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
                    required=False
                )


class QuestionAnswerForm(forms.ModelForm):
    """Form for recording quiz answers."""
    
    class Meta:
        model = QuestionAnswer
        fields = ('selected_choice',)
        widgets = {
            'selected_choice': forms.RadioSelect(),
        }


class FilterModulesForm(forms.Form):
    """Form for filtering learning modules."""
    
    DIFFICULTY_CHOICES = [('', 'All Levels')] + LearningModule._meta.get_field('difficulty_level').choices
    STATUS_CHOICES = [('', 'All Status')] + LearningModule._meta.get_field('status').choices
    
    difficulty_level = forms.ChoiceField(
        choices=DIFFICULTY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search modules...'
        })
    )
