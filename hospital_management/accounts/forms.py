from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()  # this will now be your CustomUser

# --------------------------
# Registration Form
# --------------------------
class CreateAccountForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}), label="Username")
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name'}), label="First Name")
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name'}), label="Last Name")
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}), label="Email")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), label="Password")
    re_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}), label="Confirm Password")

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password", "re_password")

    def clean(self):
        if self.data['password'] != self.data['re_password']:
            raise forms.ValidationError("Passwords don't match")
        elif User.objects.filter(email=self.data['email']).exists():
            raise forms.ValidationError("Email already exists")
        return super().clean()

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        return user


# --------------------------
# Custom Login Form
# --------------------------
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username or Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
