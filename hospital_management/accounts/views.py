from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from .models import VerificationCode


from .forms import CreateAccountForm, CustomLoginForm


def account_creation(request):
    form = CreateAccountForm()

    if request.method == 'POST':
        form = CreateAccountForm(request.POST)

        if form.is_valid():
            # ✅ PASS request to form.save
            print(" Form is valid. Creating account...")
            form.save(request=request)

            messages.success(
                request,
                "Account created successfully. Please check your email to activate your account."
            )
            return redirect("login")

    return render(request, 'accounts/register.html', {
        "form": form,
        "name": "Account Creation"
    })


def custom_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            messages.success(
                request,
                "Welcome to Hospital Management System"
            )
            print(" Login successful. Redirecting to dashboard...")
            return redirect('dashboard:home')

        else:
            # ✅ DO NOT hardcode message — show real form error
            for error in form.non_field_errors():
                messages.error(request, error)

    else:
        form = CustomLoginForm()

    return render(request, 'accounts/login.html', {'form': form})



def activate_account(request):
    code = request.GET.get('code')
    email = request.GET.get('email')

    try:
        verification = VerificationCode.objects.get(
            code=code,
            email=email,
            label=VerificationCode.SIGNUP
        )
        user = verification.user
        user.is_active = True
        user.save()

        # Remove verification code after use
        verification.delete()

        messages.success(request, "Account activated successfully. You can now login.")
        return redirect('login')

    except VerificationCode.DoesNotExist:
        messages.error(request, "Invalid or expired activation link.")
        return redirect('login')


def custom_logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')
