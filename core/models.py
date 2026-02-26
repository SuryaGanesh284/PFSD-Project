from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class CustomUser(AbstractUser):
    """
    Custom User model with role-based access control.
    Roles: ADMIN, EDUCATOR, CITIZEN
    """
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('educator', 'Educator'),
        ('citizen', 'Citizen'),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='citizen',
        help_text='User role in the platform'
    )
    bio = models.TextField(
        blank=True,
        null=True,
        help_text='User biography'
    )
    profile_image = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True,
        help_text='User profile picture'
    )
    is_email_verified = models.BooleanField(
        default=False,
        help_text='Email verification status'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'custom_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['role']),
            models.Index(fields=['email']),
        ]
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def is_admin_user(self):
        return self.role == 'admin'
    
    def is_educator(self):
        return self.role == 'educator'
    
    def is_citizen(self):
        return self.role == 'citizen'


class LearningModule(models.Model):
    """
    Learning modules containing educational content about constitutional aspects.
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(
        max_length=255,
        unique=True,
        help_text='Module title'
    )
    description = models.TextField(help_text='Module description')
    content = models.TextField(help_text='Module main content')
    slug = models.SlugField(
        unique=True,
        help_text='URL-friendly identifier'
    )
    
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_modules',
        help_text='Educator who created this module'
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        help_text='Publication status'
    )
    
    order = models.PositiveIntegerField(
        default=0,
        help_text='Display order'
    )
    
    image = models.ImageField(
        upload_to='modules/',
        blank=True,
        null=True,
        help_text='Module cover image'
    )
    
    attachment = models.FileField(
        upload_to='modules/attachments/',
        blank=True,
        null=True,
        help_text='Additional PDF or document'
    )
    
    difficulty_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
        ],
        default='beginner',
        help_text='Difficulty level'
    )
    
    estimated_time = models.PositiveIntegerField(
        default=15,
        help_text='Estimated reading time in minutes'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'learning_module'
        verbose_name = 'Learning Module'
        verbose_name_plural = 'Learning Modules'
        ordering = ['order', '-created_at']
        indexes = [
            models.Index(fields=['status', 'order']),
            models.Index(fields=['slug']),
        ]
    
    def __str__(self):
        return self.title


class Quiz(models.Model):
    """
    Quizzes created by educators to test citizen knowledge on modules.
    """
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    title = models.CharField(
        max_length=255,
        help_text='Quiz title'
    )
    description = models.TextField(help_text='Quiz description')
    module = models.ForeignKey(
        LearningModule,
        on_delete=models.CASCADE,
        related_name='quizzes',
        help_text='Associated learning module'
    )
    
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_quizzes',
        help_text='Educator who created quiz'
    )
    
    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        default='medium',
        help_text='Quiz difficulty'
    )
    
    total_questions = models.PositiveIntegerField(
        default=0,
        help_text='Total number of questions (auto-calculated)'
    )
    
    passing_score = models.PositiveIntegerField(
        default=60,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text='Minimum score to pass (%)'
    )
    
    time_limit = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text='Time limit in minutes'
    )
    
    is_published = models.BooleanField(
        default=False,
        help_text='Quiz visibility'
    )
    
    shuffle_questions = models.BooleanField(
        default=True,
        help_text='Randomize question order'
    )
    
    show_answers = models.BooleanField(
        default=True,
        help_text='Show correct answers after completion'
    )
    
    max_attempts = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text='Maximum attempts (null = unlimited)'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'quiz'
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quizzes'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['module', 'is_published']),
        ]
    
    def __str__(self):
        return self.title
    
    def update_question_count(self):
        """Update total questions count"""
        self.total_questions = self.questions.count()
        self.save()


class Question(models.Model):
    """
    Individual questions within a quiz.
    Supports multiple choice format with one correct answer.
    """
    QUESTION_TYPE_CHOICES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
    ]
    
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='questions',
        help_text='Parent quiz'
    )
    
    text = models.TextField(help_text='Question text')
    question_type = models.CharField(
        max_length=50,
        choices=QUESTION_TYPE_CHOICES,
        default='multiple_choice',
        help_text='Type of question'
    )
    
    order = models.PositiveIntegerField(
        default=0,
        help_text='Display order within quiz'
    )
    
    explanation = models.TextField(
        blank=True,
        null=True,
        help_text='Explanation for the correct answer'
    )
    
    points = models.PositiveIntegerField(
        default=1,
        help_text='Points for correct answer'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'question'
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
        ordering = ['quiz', 'order']
        indexes = [
            models.Index(fields=['quiz', 'order']),
        ]
    
    def __str__(self):
        return f"{self.quiz.title} - Q{self.order}: {self.text[:50]}"


class Choice(models.Model):
    """
    Answer choices for multiple choice questions.
    """
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='choices',
        help_text='Parent question'
    )
    
    text = models.TextField(help_text='Choice text')
    is_correct = models.BooleanField(
        default=False,
        help_text='Mark if this is correct answer'
    )
    
    order = models.PositiveIntegerField(
        default=0,
        help_text='Display order'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'choice'
        verbose_name = 'Choice'
        verbose_name_plural = 'Choices'
        ordering = ['question', 'order']
        indexes = [
            models.Index(fields=['question', 'is_correct']),
        ]
    
    def __str__(self):
        return f"{self.question.text[:30]} - {self.text[:40]}"


class QuizAttempt(models.Model):
    """
    Tracks user quiz attempts and results.
    """
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='quiz_attempts',
        help_text='User who took the quiz'
    )
    
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='attempts',
        help_text='Quiz attempted'
    )
    
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    score = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text='Total score obtained'
    )
    
    total_possible_score = models.PositiveIntegerField(
        default=0,
        help_text='Total possible score'
    )
    
    percentage = models.FloatField(
        null=True,
        blank=True,
        help_text='Score percentage'
    )
    
    is_passed = models.BooleanField(
        null=True,
        blank=True,
        help_text='Whether user passed the quiz'
    )
    
    total_questions_attempted = models.PositiveIntegerField(
        default=0,
        help_text='Questions answered'
    )
    
    total_questions_correct = models.PositiveIntegerField(
        default=0,
        help_text='Correct answers'
    )
    
    time_taken = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text='Time taken in seconds'
    )
    
    class Meta:
        db_table = 'quiz_attempt'
        verbose_name = 'Quiz Attempt'
        verbose_name_plural = 'Quiz Attempts'
        ordering = ['-started_at']
        indexes = [
            models.Index(fields=['user', 'quiz']),
            models.Index(fields=['is_passed']),
        ]
        unique_together = []
    
    def __str__(self):
        return f"{self.user.username} - {self.quiz.title}"
    
    def calculate_score(self):
        """Calculate score based on answers"""
        answers = self.answers.all()
        correct = sum(1 for answer in answers if answer.is_correct)
        self.total_questions_correct = correct
        self.total_questions_attempted = answers.count()
        
        total_points = sum(answer.question.points for answer in answers)
        correct_points = sum(
            answer.question.points for answer in answers if answer.is_correct
        )
        
        self.score = correct_points
        self.total_possible_score = total_points
        
        if total_points > 0:
            self.percentage = (correct_points / total_points) * 100
            self.is_passed = self.percentage >= self.quiz.passing_score
        
        self.save()


class QuestionAnswer(models.Model):
    """
    Records which answer a user selected for each question.
    """
    attempt = models.ForeignKey(
        QuizAttempt,
        on_delete=models.CASCADE,
        related_name='answers',
        help_text='Quiz attempt this answer belongs to'
    )
    
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        help_text='Question answered'
    )
    
    selected_choice = models.ForeignKey(
        Choice,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text='Choice selected by user'
    )
    
    is_correct = models.BooleanField(
        default=False,
        help_text='Whether answer was correct'
    )
    
    answered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'question_answer'
        verbose_name = 'Question Answer'
        verbose_name_plural = 'Question Answers'
        ordering = ['attempt', 'question__order']
    
    def __str__(self):
        return f"{self.attempt} - {self.question}"


class DiscussionThread(models.Model):
    """
    Discussion threads for forums related to modules or general topics.
    """
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('pinned', 'Pinned'),
    ]
    
    title = models.CharField(
        max_length=255,
        help_text='Thread title'
    )
    
    content = models.TextField(help_text='Thread content')
    
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='discussion_threads',
        help_text='Thread creator'
    )
    
    module = models.ForeignKey(
        LearningModule,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='discussion_threads',
        help_text='Related module (optional)'
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='open',
        help_text='Thread status'
    )
    
    is_pinned = models.BooleanField(
        default=False,
        help_text='Pin thread to top'
    )
    
    views_count = models.PositiveIntegerField(
        default=0,
        help_text='Number of views'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'discussion_thread'
        verbose_name = 'Discussion Thread'
        verbose_name_plural = 'Discussion Threads'
        ordering = ['-is_pinned', '-updated_at']
        indexes = [
            models.Index(fields=['-is_pinned', '-created_at']),
            models.Index(fields=['module', 'status']),
        ]
    
    def __str__(self):
        return self.title
    
    def increment_views(self):
        """Increment view count"""
        self.views_count += 1
        self.save(update_fields=['views_count'])


class Comment(models.Model):
    """
    Comments on discussion threads.
    Supports nested replies through parent field.
    """
    thread = models.ForeignKey(
        DiscussionThread,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text='Parent thread'
    )
    
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text='Comment author'
    )
    
    content = models.TextField(help_text='Comment content')
    
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        help_text='Parent comment (for nested replies)'
    )
    
    is_edited = models.BooleanField(
        default=False,
        help_text='Whether comment has been edited'
    )
    
    likes_count = models.PositiveIntegerField(
        default=0,
        help_text='Number of likes'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'comment'
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['thread', 'author']),
            models.Index(fields=['parent']),
        ]
    
    def __str__(self):
        return f"{self.author.username} - {self.content[:50]}"


class CommentLike(models.Model):
    """
    Tracks likes on comments.
    """
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name='likes',
        help_text='Comment being liked'
    )
    
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comment_likes',
        help_text='User who liked'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'comment_like'
        verbose_name = 'Comment Like'
        verbose_name_plural = 'Comment Likes'
        unique_together = ('comment', 'user')
        indexes = [
            models.Index(fields=['comment', 'user']),
        ]
    
    def __str__(self):
        return f"{self.user.username} liked {self.comment.id}"
