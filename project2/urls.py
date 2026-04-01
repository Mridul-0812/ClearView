from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views # Add this

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', include('tasks.urls')),
    
    # This is the line that was missing! 
    # It names the path 'login' so your template can find it.
    path('login/', auth_views.LoginView.as_view(template_name='tasks/login.html'), name='login'),
    
    # Add logout here too so it's globally available
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Redirect the very root of the site to our welcome page
    path('', lambda request: redirect('tasks:welcome')), 
]