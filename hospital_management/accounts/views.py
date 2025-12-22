from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout

from .forms import CreateAccountForm, CustomLoginForm


def account_creation(request):
    form = CreateAccountForm()

    if request.method == 'POST':
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            form.save()
            print("Account created successfully.")
            messages.success(request, "Account created successfully. Please login.")
            return redirect("login")

    context = {
        "form": form,
        "name": "Account Creation"
    }
    return render(request, 'accounts/register.html', context)


def custom_login(request):
    if request.method == 'POST':
        print()
        print("Login attempt:")
        print()
        form = CustomLoginForm(request, data=request.POST)
        print("Form data:", form.is_valid())
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            print("Login successful.")
            return redirect('home')  # or dashboard
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = CustomLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def custom_logout_view(request):
    logout(request)
    return redirect('login')
