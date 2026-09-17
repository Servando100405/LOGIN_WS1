from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import redirect, render

from .models import Profile


def index_view(request):
    return render(request, 'index.html')


def register_view(request):
    if request.method == 'POST':
        registration_data = request.POST.copy()
        registration_data.setdefault('password2', registration_data.get('password1', ''))
        form = UserCreationForm(registration_data)
        if form.is_valid():
            with transaction.atomic():
                user = form.save(commit=False)
                user.first_name = request.POST.get('first_name', '').strip()
                user.last_name = request.POST.get('last_name', '').strip()
                user.save()
                Profile.objects.create(
                    user=user,
                    account_type=request.POST.get('account_type', 'student'),
                )
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            selected_type = request.POST.get('account_type')
            user = authenticate(username=username, password=password)
            if user is not None:
                profile, _ = Profile.objects.get_or_create(
                    user=user,
                    defaults={'account_type': 'staff' if user.is_staff else 'student'},
                )
                is_staff_account = user.is_superuser or user.is_staff or profile.account_type in ('staff', 'teacher')
                role_matches = (
                    selected_type == 'staff' and is_staff_account
                ) or (
                    selected_type == 'student' and not is_staff_account and profile.account_type == 'student'
                )
                if role_matches:
                    login(request, user)
                    messages.success(request, f'Welcome back, {username}!')
                    return redirect('dashboard')

                form.add_error(None, 'The selected account type does not match this username.')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


@login_required(login_url='login')
def dashboard_view(request):
    profile, _ = Profile.objects.get_or_create(
        user=request.user,
        defaults={'account_type': 'staff' if request.user.is_staff else 'student'},
    )
    if request.user.is_superuser:
        return redirect('admin_dashboard')
    if profile.account_type in ('staff', 'teacher') or request.user.is_staff:
        return redirect('staff_dashboard')

    return render(request, 'dashboard.html', {
        'user': request.user,
        'profile': profile,
    })


@login_required(login_url='login')
def admin_dashboard_view(request):
    profile, _ = Profile.objects.get_or_create(
        user=request.user,
        defaults={'account_type': 'staff' if request.user.is_staff else 'student'},
    )
    if not request.user.is_superuser:
        return redirect('dashboard')

    return render(request, 'admin_dashboard.html', {
        'user': request.user,
        'profile': profile,
        'total_users': User.objects.count(),
        'student_count': Profile.objects.filter(account_type='student').count(),
        'teacher_count': Profile.objects.filter(account_type='teacher').count(),
        'staff_count': Profile.objects.filter(account_type='staff').count(),
        'recent_users': User.objects.order_by('-date_joined')[:6],
    })


@login_required(login_url='login')
def staff_dashboard_view(request):
    profile, _ = Profile.objects.get_or_create(
        user=request.user,
        defaults={'account_type': 'staff'},
    )
    if request.user.is_superuser:
        return redirect('admin_dashboard')
    if profile.account_type not in ('staff', 'teacher') and not request.user.is_staff:
        return redirect('dashboard')

    return render(request, 'staff_dashboard.html', {
        'user': request.user,
        'profile': profile,
        'total_users': User.objects.count(),
        'student_count': Profile.objects.filter(account_type='student').count(),
        'teacher_count': Profile.objects.filter(account_type='teacher').count(),
    })


def logout_view(request):
    logout(request)
    return redirect('login')
