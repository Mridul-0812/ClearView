from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.contrib import messages

app_name = "tasks"

# Simple subclass to inject the success message when the form is valid
class SuccessMessagePasswordResetView(auth_views.PasswordResetView):
    def form_valid(self, form):
        messages.success(self.request, "A reset link has been sent to your email!")
        return super().form_valid(form)

urlpatterns = [
    # Dashboard & Landing
    path("", views.index, name="index"),
    path("welcome/", views.welcome, name="welcome"),
    
    # Task Management
    path("add/", views.add, name="add"),
    path("delete/<int:task_id>/", views.delete, name="delete"),
    path("toggle/<int:task_id>/", views.toggle, name="toggle"),
    
    # Productivity Tools & Analytics
    path("timer/", views.focus_timer, name="timer"), 
    path("stats/", views.climb_stats, name="climb_stats"), # New Stats/Analytics Route
    
    # Auth Logic
    path("signup/", views.signup, name="signup"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    
    # Add this inside your urlpatterns list
    path("edit/<int:task_id>/", views.edit_task, name="edit"),
    path('beats/', views.zen_beats, name='zen_beats'),
    
    # Password Reset Workflow
    path('password-reset/', 
         SuccessMessagePasswordResetView.as_view(
             template_name='tasks/password_reset.html',
             email_template_name='tasks/password_reset_email.html',
             success_url=reverse_lazy('tasks:password_reset_done')
         ), 
         name='password_reset'),
         
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='tasks/password_reset_done.html'
         ), 
         name='password_reset_done'),
         
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='tasks/password_reset_confirm.html',
             success_url=reverse_lazy('tasks:password_reset_complete')
         ), 
         name='password_reset_confirm'),
         
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='tasks/password_reset_complete.html'
         ), 
         name='password_reset_complete'),
]