from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'website'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('projects/', views.projects_list, name='projects'),
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),
    path('news/', views.news_list, name='news'),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),
    path('get-involved/', views.get_involved, name='get_involved'),

    # Authentication URLs
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.user_profile, name='profile'),

    # Password reset URLs
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='website/password_reset.html',
             email_template_name='website/password_reset_email.html',
             subject_template_name='website/password_reset_subject.txt',
             success_url='/password-reset/done/'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='website/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='website/password_reset_confirm.html',
             success_url='/password-reset-complete/'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='website/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]
