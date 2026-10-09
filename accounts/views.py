from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# Home (first page, always shown)
def home(request):
    return render(request, 'home.html')


# Register
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            if request.POST['password'] == request.POST['confirm_password']:
                username = request.POST['username']
                email = request.POST['email']
                password = request.POST['password']
                User.objects.create_user(
                    username=username,
                    password=password,
                    email=email
                )
                messages.success(request, 'Registration done successfully')
                return redirect('login')
            else:
                messages.error(request, 'Password and confirm password not matching')
        else:
            messages.error(request, 'Invalid credentials')

    else:
        form = RegistrationForm()

    context = {
        'form': form
    }

    return render(request, 'register.html', context)


# Login
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, 'Login successful')
            return redirect('product_list')
        else:
            messages.error(request, 'Invalid username or password')

    form = LoginForm()

    context = {
        'form': form
    }

    return render(request, 'user_login.html', context)


@login_required(login_url='login')
def profile(request):
    return render(request, 'profile.html')


# Logout
def user_logout(request):
    logout(request)
    messages.success(request, 'logout successful!')
    return redirect('login')