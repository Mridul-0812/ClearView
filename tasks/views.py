import ssl
# Global bypass for macOS Python certificate issues
ssl._create_default_https_context = ssl._create_unverified_context

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.core.mail import send_mail, get_connection
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from .models import Task
from django.contrib import messages

# New imports for Analytics & Time Awareness
from django.utils import timezone
from datetime import timedelta, date
from django.db.models import Count

# --- 1. LANDING & AUTH LOGIC ---

def welcome(request):
    if request.user.is_authenticated:
        return redirect("tasks:index")
    return render(request, "tasks/welcome.html")

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        email = request.POST.get('email')
        
        if form.is_valid() and email:
            # 1. Check if email exists BEFORE saving anything
            if User.objects.filter(email=email).exists():
                return render(request, 'tasks/signup.html', {
                    'form': form, 
                    'error': "This email is already registered."
                })

            # 2. Prepare user object in memory (DO NOT save yet)
            user = form.save(commit=False)
            user.email = email
            user.is_active = True 
            
            try:
                # 3. Only save to DB if we are about to attempt email sending
                user.save()
                
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                protocol = 'https' if request.is_secure() else 'http'
                link = f"{protocol}://{request.get_host()}/tasks/activate/{uid}/{token}/"
                
                connection = get_connection(
                    backend=settings.EMAIL_BACKEND,
                    ssl_context=ssl._create_unverified_context()
                )
                
                send_mail(
                    'Confirm your ZenStack Account',
                    f'Welcome {user.username}!\n\nClick here to activate your account: {link}',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    connection=connection,
                    fail_silently=False,
                )
                
                messages.success(request, "Success! Please check your Gmail inbox to activate your account.")
                return redirect('tasks:login')
            
            except Exception as e:
                # 4. Clean up the user record if email fails so the username stays available
                if user.pk:
                    user.delete() 
                return render(request, 'tasks/signup.html', {
                    'form': form, 
                    'error': f"Failed to send email. Ensure your Gmail App Password is correct. Error: {str(e)}"
                })
        else:
            error_msg = "Please correct the errors below." if form.errors else "Email is required."
            return render(request, 'tasks/signup.html', {'form': form, 'error': error_msg})
                
    else:
        form = UserCreationForm()
    return render(request, 'tasks/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, "Account activated! Welcome to ZenStack.")
        return redirect('tasks:index')
    else:
        return render(request, 'tasks/activation_invalid.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('tasks:index')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'tasks/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('tasks:welcome')


# --- 2. DASHBOARD & TASK LOGIC ---

@login_required
def index(request):
    tasks = Task.objects.filter(
        user=request.user, 
        is_archived=False
    ).order_by('-created_at') 
    
    # Dynamic date coloring logic
    today_date = date.today()
    for task in tasks:
        if task.due_date:
            delta = (task.due_date - today_date).days
            if delta < 0: task.urgency = 'overdue'
            elif delta <= 1: task.urgency = 'soon'
            else: task.urgency = 'safe'
        else:
            task.urgency = 'none'

    return render(request, "tasks/index.html", {"tasks": tasks})

@login_required
def add(request):
    if request.method == "POST":
        task_title = request.POST.get("title")
        task_priority = request.POST.get("priority")
        task_due = request.POST.get("due_date")
        
        if task_title:
            Task.objects.create(
                user=request.user,
                title=task_title, 
                priority=task_priority,
                due_date=task_due if task_due else None
            )
            return redirect("tasks:index")
    return render(request, "tasks/add.html")

@login_required
def delete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.is_archived = True 
    task.save()
    return redirect("tasks:index")

@login_required
def zen_beats(request):
    return render(request, "tasks/beats.html")

@login_required
def toggle(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = not task.completed 
    
    if task.completed:
        task.completed_at = timezone.now()
    else:
        task.completed_at = None
        
    task.save()
    return redirect("tasks:index")

# --- 3. ANALYTICS ---

@login_required
def focus_timer(request):
    """View for the productivity timer page"""
    return render(request, "tasks/timer.html")

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == "POST":
        title = request.POST.get("title")
        priority = request.POST.get("priority")
        due_date = request.POST.get("due_date")

        task.title = title
        task.priority = priority
        
        if due_date:
            task.due_date = due_date
        else:
            task.due_date = None
            
        task.save() 
        return redirect("tasks:index")

    return render(request, "tasks/edit.html", {"task": task})

@login_required
def climb_stats(request):
    today = timezone.localdate()
    
    labels = []
    data_points = []
    
    for i in range(6, -1, -1):
        target_day = today - timedelta(days=i)
        labels.append(target_day.strftime('%a')) 
        
        count = Task.objects.filter(
            user=request.user,
            completed=True,
            completed_at__date=target_day
        ).count()
        data_points.append(count)

    total_completed = Task.objects.filter(user=request.user, completed=True).count()
    daily_count = data_points[-1] 
    total_active = Task.objects.filter(user=request.user, completed=False, is_archived=False).count()

    badges = []
    if total_completed >= 10:
        badges.append({'name': 'Sherpa', 'icon': '🧗', 'desc': '10+ Total Tasks Done'})
    if daily_count > 0 and total_active == 0:
        badges.append({'name': 'Everest', 'icon': '🏔️', 'desc': 'Cleared the Board Today'})

    return render(request, "tasks/stats.html", {
        "labels": labels,
        "data": data_points,
        "badges": badges,
        "total_done": total_completed
    })