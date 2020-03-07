import re
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django import forms
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

User = get_user_model()


class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('full_name', 'phone', 'email',)

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if not full_name:
            raise forms.ValidationError("Please enter your name")

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('full_name', 'phone', 'email', 'nid', 'password', 'is_active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


# class GuestRegisterForm(forms.Form):
#     email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
#     phone = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))


class LoginForm(forms.Form):
    phone = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

    def clean(self):
        phone = self.cleaned_data.get('phone')
        password = self.cleaned_data.get('password')
        user = authenticate(username=phone, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return self.cleaned_data
    #
    # def login(self, request):
    #     email = self.cleaned_data.get('email')
    #     password = self.cleaned_data.get('password')
    #     user = authenticate(username=email, password=password)
    #     return user


class RegisterForm(forms.Form):
    error_css_class = "error"
    full_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}),max_length=200)
    phone = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}),max_length=14,min_length=11)
    nid = forms.CharField(label="NID", widget=forms.TextInput(attrs={"class": "form-control"}),max_length=17,min_length=10)
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control'}), max_length=100,
                             error_messages={'invalid': ("Email invalide.")}, validators=[validate_email])
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}),
                               validators=[validate_password], required=True)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={"class": "form-control"}),
                                required=True)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("This 'email' is taken")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        qs = User.objects.filter(phone=phone)
        if qs.exists():
            raise forms.ValidationError("This 'phone' number is taken")
        return phone

    def clean_nid(self):
        nid = self.cleaned_data.get("nid")
        qs = User.objects.filter(nid=nid)
        if qs.exists():
            raise forms.ValidationError("This 'nid' number is taken")
        return nid

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password2 != password:
            raise forms.ValidationError('Password have to match!')
        if not password:  # Check Password is Empty
            raise forms.ValidationError("Password Is Required")
        return data

# class SignUpForm(UserCreationForm):
#     username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
#     first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
#     last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
#     email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
#     password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
#     password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={"class": "form-control"}))
#
#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
#
#     def clean_username(self):
#         username = self.cleaned_data.get("username")
#         qs = User.objects.filter(username=username)
#         if qs.exists():
#             raise forms.ValidationError("This 'username' is taken!")
#         return username
#
#     def clean_email(self):
#         email = self.cleaned_data.get("email")
#         qs = User.objects.filter(email=email)
#         if qs.exists():
#             raise forms.ValidationError("This 'email' is taken")
#         return email
#
#     def clean(self):
#         data = self.cleaned_data
#         password = self.cleaned_data.get("password")
#         password2 = self.cleaned_data.get("password2")
#         if password2 != password:
#             raise forms.ValidationError('Password have to match!')
#         return data
