from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import (
    CustomUser, LearningModule, Quiz, Question, Choice,
    QuizAttempt, QuestionAnswer, DiscussionThread, Comment, CommentLike
)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin interface for Custom User model with role-based display."""
    
    list_display = ('username', 'email', 'get_role_display', 'is_email_verified', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_email_verified', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'bio', 'profile_image', 'is_email_verified')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Assignment', {
            'fields': ('role',)
        }),
    )


@admin.register(LearningModule)
class LearningModuleAdmin(admin.ModelAdmin):
    """Admin interface for Learning Modules."""
    
    list_display = ('title', 'get_status_badge', 'difficulty_level', 'created_by', 'order', 'created_at')
    list_filter = ('status', 'difficulty_level', 'created_at')
    search_fields = ('title', 'description', 'created_by__username')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'description', 'content')
        }),
        ('Media', {
            'fields': ('image', 'attachment')
        }),
        ('Settings', {
            'fields': ('status', 'difficulty_level', 'estimated_time', 'order', 'created_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'published_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_status_badge(self, obj):
        """Display status with color badge."""
        colors = {
            'draft': '#FFC107',
            'published': '#28A745',
            'archived': '#6C757D'
        }
        color = colors.get(obj.status, '#007BFF')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 4px;">{}</span>',
            color, obj.get_status_display()
        )
    get_status_badge.short_description = 'Status'


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    """Admin interface for Quizzes."""
    
    list_display = ('title', 'module', 'difficulty', 'get_publish_badge', 'total_questions', 'passing_score', 'created_by')
    list_filter = ('is_published', 'difficulty', 'created_at', 'module')
    search_fields = ('title', 'description', 'module__title', 'created_by__username')
    readonly_fields = ('total_questions', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Quiz Info', {
            'fields': ('title', 'description', 'module', 'difficulty')
        }),
        ('Settings', {
            'fields': ('is_published', 'shuffle_questions', 'show_answers', 'passing_score')
        }),
        ('Constraints', {
            'fields': ('time_limit', 'max_attempts', 'total_questions')
        }),
        ('Creator', {
            'fields': ('created_by',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_publish_badge(self, obj):
        """Display publication status."""
        if obj.is_published:
            return format_html(
                '<span style="background-color: #28A745; color: white; padding: 5px 10px; border-radius: 4px;">Published</span>'
            )
        return format_html(
            '<span style="background-color: #FFC107; color: black; padding: 5px 10px; border-radius: 4px;">Draft</span>'
        )
    get_publish_badge.short_description = 'Status'


class ChoiceInline(admin.TabularInline):
    """Inline admin for answer choices."""
    model = Choice
    extra = 3
    fields = ('text', 'is_correct', 'order')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Admin interface for Quiz Questions."""
    
    inlines = [ChoiceInline]
    list_display = ('get_question_preview', 'quiz', 'question_type', 'order', 'points')
    list_filter = ('quiz', 'question_type', 'created_at')
    search_fields = ('text', 'quiz__title')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Question', {
            'fields': ('quiz', 'text', 'question_type', 'order')
        }),
        ('Answer Details', {
            'fields': ('explanation', 'points')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_question_preview(self, obj):
        """Display question preview."""
        return f"Q{obj.order}: {obj.text[:50]}..."
    get_question_preview.short_description = 'Question'


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    """Admin interface for Answer Choices."""
    
    list_display = ('get_choice_text', 'question', 'is_correct', 'order')
    list_filter = ('is_correct', 'created_at')
    search_fields = ('text', 'question__text')
    
    def get_choice_text(self, obj):
        """Display choice text with correct indicator."""
        marker = '✓' if obj.is_correct else '✗'
        return f"{marker} {obj.text[:50]}"
    get_choice_text.short_description = 'Choice'


class QuestionAnswerInline(admin.TabularInline):
    """Inline admin for quiz answers."""
    model = QuestionAnswer
    extra = 0
    readonly_fields = ('question', 'selected_choice', 'is_correct', 'answered_at')
    can_delete = False


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    """Admin interface for Quiz Attempts."""
    
    inlines = [QuestionAnswerInline]
    list_display = ('user', 'quiz', 'get_score_display', 'get_pass_badge', 'started_at')
    list_filter = ('is_passed', 'quiz', 'started_at')
    search_fields = ('user__username', 'quiz__title')
    readonly_fields = (
        'user', 'quiz', 'started_at', 'completed_at', 'score',
        'total_possible_score', 'percentage', 'is_passed',
        'total_questions_attempted', 'total_questions_correct', 'time_taken'
    )
    
    fieldsets = (
        ('Attempt Info', {
            'fields': ('user', 'quiz')
        }),
        ('Timeline', {
            'fields': ('started_at', 'completed_at', 'time_taken')
        }),
        ('Scoring', {
            'fields': ('score', 'total_possible_score', 'percentage', 'is_passed')
        }),
        ('Statistics', {
            'fields': ('total_questions_attempted', 'total_questions_correct')
        }),
    )
    
    def get_score_display(self, obj):
        """Display score in readable format."""
        if obj.score is None:
            return "In Progress"
        return f"{obj.score}/{obj.total_possible_score}"
    get_score_display.short_description = 'Score'
    
    def get_pass_badge(self, obj):
        """Display pass/fail status."""
        if obj.is_passed is None:
            return format_html(
                '<span style="background-color: #17A2B8; color: white; padding: 5px 10px; border-radius: 4px;">In Progress</span>'
            )
        if obj.is_passed:
            return format_html(
                '<span style="background-color: #28A745; color: white; padding: 5px 10px; border-radius: 4px;">Passed</span>'
            )
        return format_html(
            '<span style="background-color: #DC3545; color: white; padding: 5px 10px; border-radius: 4px;">Failed</span>'
        )
    get_pass_badge.short_description = 'Result'


@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(admin.ModelAdmin):
    """Admin interface for Question Answers."""
    
    list_display = ('attempt', 'question', 'get_selected_choice', 'get_correctness_badge')
    list_filter = ('is_correct', 'answered_at')
    search_fields = ('question__text', 'attempt__user__username')
    readonly_fields = ('attempt', 'question', 'selected_choice', 'is_correct', 'answered_at')
    
    def get_selected_choice(self, obj):
        """Display selected choice."""
        return obj.selected_choice.text[:50] if obj.selected_choice else "Not answered"
    get_selected_choice.short_description = 'Selected Choice'
    
    def get_correctness_badge(self, obj):
        """Display if answer is correct."""
        if obj.is_correct:
            return format_html(
                '<span style="background-color: #28A745; color: white; padding: 5px 10px; border-radius: 4px;">Correct</span>'
            )
        return format_html(
            '<span style="background-color: #DC3545; color: white; padding: 5px 10px; border-radius: 4px;">Incorrect</span>'
        )
    get_correctness_badge.short_description = 'Result'


class CommentInline(admin.TabularInline):
    """Inline admin for thread comments."""
    model = Comment
    extra = 0
    fields = ('author', 'content', 'likes_count', 'created_at')
    readonly_fields = ('author', 'likes_count', 'created_at')
    can_delete = False


@admin.register(DiscussionThread)
class DiscussionThreadAdmin(admin.ModelAdmin):
    """Admin interface for Discussion Threads."""
    
    inlines = [CommentInline]
    list_display = ('title', 'author', 'get_status_badge', 'module', 'views_count', 'created_at')
    list_filter = ('status', 'is_pinned', 'module', 'created_at')
    search_fields = ('title', 'content', 'author__username', 'module__title')
    readonly_fields = ('views_count', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Thread', {
            'fields': ('title', 'content', 'author')
        }),
        ('Organization', {
            'fields': ('module', 'status', 'is_pinned')
        }),
        ('Statistics', {
            'fields': ('views_count',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_status_badge(self, obj):
        """Display thread status."""
        colors = {
            'open': '#28A745',
            'closed': '#6C757D',
            'pinned': '#FFC107'
        }
        color = colors.get(obj.status, '#007BFF')
        return format_html(
            '<span style="background-color: {}; color: {}; padding: 5px 10px; border-radius: 4px;">{}</span>',
            color, 'white' if color != '#FFC107' else 'black', obj.get_status_display()
        )
    get_status_badge.short_description = 'Status'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin interface for Comments."""
    
    list_display = ('get_author_display', 'get_content_preview', 'thread', 'likes_count', 'created_at')
    list_filter = ('is_edited', 'created_at')
    search_fields = ('content', 'author__username', 'thread__title')
    readonly_fields = ('thread', 'author', 'likes_count', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Comment', {
            'fields': ('thread', 'author', 'parent', 'content')
        }),
        ('Engagement', {
            'fields': ('likes_count', 'is_edited')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_author_display(self, obj):
        """Display author name."""
        return obj.author.get_full_name() or obj.author.username
    get_author_display.short_description = 'Author'
    
    def get_content_preview(self, obj):
        """Display content preview."""
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    get_content_preview.short_description = 'Content'


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    """Admin interface for Comment Likes."""
    
    list_display = ('user', 'get_comment_preview', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'comment__content')
    readonly_fields = ('user', 'comment', 'created_at')    
    def get_comment_preview(self, obj):
        """Get a preview of the liked comment."""
        if obj.comment:
            preview = obj.comment.content[:50] + '...' if len(obj.comment.content) > 50 else obj.comment.content
            return preview
        return '(Deleted)'
    get_comment_preview.short_description = 'Comment Preview'