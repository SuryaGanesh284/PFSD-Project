from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home_view, name='home'),
    
    # Authentication
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/educator/', views.educator_dashboard, name='educator_dashboard'),
    path('dashboard/citizen/', views.citizen_dashboard, name='citizen_dashboard'),
    
    # Profile
    path('profile/', views.profile_view, name='profile'),
    path('profile/<int:pk>/', views.profile_view, name='user_profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    
    # Learning Modules
    path('modules/', views.ModuleListView.as_view(), name='module_list'),
    path('modules/create/', views.ModuleCreateView.as_view(), name='module_create'),
    path('modules/<slug:slug>/', views.ModuleDetailView.as_view(), name='module_detail'),
    path('modules/<slug:slug>/edit/', views.ModuleUpdateView.as_view(), name='module_edit'),
    
    # Quizzes
    path('quizzes/', views.QuizListView.as_view(), name='quiz_list'),
    path('quizzes/create/', views.QuizCreateView.as_view(), name='quiz_create'),
    path('quizzes/<int:pk>/', views.QuizDetailView.as_view(), name='quiz_detail'),
    path('quizzes/<int:pk>/take/', views.quiz_take_view, name='quiz_take'),
    path('quizzes/result/<int:pk>/', views.QuizResultView.as_view(), name='quiz_result'),
    
    # Discussions
    path('discussions/', views.DiscussionThreadListView.as_view(), name='thread_list'),
    path('discussions/create/', views.DiscussionThreadCreateView.as_view(), name='thread_create'),
    path('discussions/<int:pk>/', views.DiscussionThreadDetailView.as_view(), name='thread_detail'),
    path('discussions/<int:pk>/edit/', views.DiscussionThreadUpdateView.as_view(), name='thread_edit'),
    
    # Comments & Engagement
    path('discussions/<int:thread_pk>/comment/', views.add_comment_view, name='add_comment'),
    path('comments/<int:comment_pk>/like/', views.like_comment_view, name='like_comment'),
]
