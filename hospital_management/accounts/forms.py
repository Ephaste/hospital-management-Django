from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from utils.send_email import send_email_custom
from utils.code_generator import random_with_N_digits
from .models import VerificationCode

User = get_user_model()

# --------------------------
# Registration Form
# --------------------------
class CreateAccountForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    re_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password", "re_password")

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get('password') != cleaned_data.get('re_password'):
            raise forms.ValidationError("Passwords do not match")

        if User.objects.filter(email=cleaned_data.get('email')).exists():
            raise forms.ValidationError("Email already exists")

        return cleaned_data

    def save(self, request=None):
        # 1️⃣ Create inactive user
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            is_active=False
        )

        # 2️⃣ Generate verification code
        code = random_with_N_digits()

        # 3️⃣ Save verification code
        code_instance = VerificationCode.objects.create(
            user=user,
            code=code,
            label=VerificationCode.SIGNUP,
            email=user.email
        )

        # 4️⃣ Build activation URL
        activate_url = request.build_absolute_uri(
            f"/activate-account/?code={code_instance.code}&email={code_instance.email}"
        )

        # 5️⃣ Send activation email
        context = {
            "user": user,
            "activate_url": activate_url
        }

        send_email_custom(
            rec=user.email,
            subject="Activate your account",
            context=context
        )

        return user


# --------------------------
# Custom Login Form
# --------------------------

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username or Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                "Account is not activated. Please check your email.",
                code="inactive",
            )

       # super().confirm_Login_allowed(user)