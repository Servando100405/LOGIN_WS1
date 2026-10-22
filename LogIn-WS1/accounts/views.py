from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.shortcuts import redirect, render


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'The username or password is incorrect.')
    return render(request, 'login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')

        if not username:
            messages.error(request, 'Enter a username.')
        elif password != password2:
            messages.error(request, 'The passwords do not match.')
        elif User.objects.filter(username__iexact=username).exists():
            messages.error(request, 'That username is already taken.')
        else:
            try:
                validate_password(password, user=User(username=username))
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                )
            except ValidationError as error:
                for message in error.messages:
                    messages.error(request, message)
            except IntegrityError:
                messages.error(request, 'That username is already taken.')
            else:
                login(request, user)
                return redirect('dashboard')
    return render(request, 'register.html')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    display_name = request.user.get_full_name() or request.user.username
    return render(request, 'dashboard.html', {'display_name': display_name})