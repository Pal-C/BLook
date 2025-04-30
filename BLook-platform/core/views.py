from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm
from django.contrib.auth import login, authenticate
from django.contrib import messages

def index(request):
    return HttpResponse("Hello, world. You're at the core index.")

def home(request):
    return render(request, 'main/home.html')

def auth_screen(request):
    login_form = AuthenticationForm()
    register_form = UserCreationForm()
    password_reset_form = PasswordResetForm()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'login':
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('home')
            else:
                messages.error(request, "Invalid login credentials.")

        elif action == 'register':
            register_form = UserCreationForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                messages.success(request, f"Account created for {user.username}!")
                return redirect('home')
            else:
                messages.error(request, "Please correct the registration errors.")

    context = {
        'login_form': login_form,
        'register_form': register_form,
        'password_reset_form': password_reset_form,
    }

    return render(request, 'main/auth.html', context)

