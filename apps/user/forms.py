from django import forms
from django.core.exceptions import ValidationError
from .models import User
from apps.college.models import CollegeBranch, CollegeStudent, CollegeStaff


class UserSignUpForm(forms.ModelForm):
    """
    Form for registering a new user account.
    """

    def __init__(self, *args, **kwargs):
        super(UserSignUpForm, self).__init__(*args, **kwargs)

        self.fields['user_type'].label = "I am a"

    first_name = forms.CharField(
        label='First Name',
        widget=forms.TextInput(
            attrs={'placeholder': "First Name"}
        )
    )
    last_name = forms.CharField(
        label='Last Name',
        widget=forms.TextInput(
            attrs={'placeholder': "Last Name"}
        )
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.TextInput(attrs={'placeholder': 'Email'})
    )
    phone_number = forms.CharField(
        label='Phone Number',
        widget=forms.TextInput(
            attrs={'placeholder': "Phone Number"}
        )
    )
    branch = forms.ModelChoiceField(
        queryset=CollegeBranch.objects.all().order_by('branch_name'),
        empty_label="Select Branch",
        widget=forms.Select(attrs={'required': 'true' }),
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )

    class Meta:
        """Model with fields in form."""

        model = User
        fields = (
            'user_type', 'branch', 'first_name', 'last_name', 'phone_number',
            'email', 'password',
        )

    def clean_email(self):
        """Def which enforces uniqueness of email addresses."""
        email = self.cleaned_data['email'].lower()

        user = User.objects.filter(email=email)
        if user.count():
            raise ValidationError("Email ID exists")
        
        return email

    def save(self, commit=True):
        """
        Create the user.

        Returns the user object after creation
        """

        user = User.objects.create_user(
            self.cleaned_data['email'],
            self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']   
        )
        user.is_active = True
        user.college_branch = self.cleaned_data['branch']
        user.phone_number = self.cleaned_data['phone_number']
        user.user_type = self.cleaned_data['user_type']
        user.save()

        return user


class UserLoginForm(forms.Form):
    """
    Form for login
    """

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(
        label='Email',
        widget=forms.TextInput(attrs={'placeholder': 'Email'})
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )


    def clean_email(self):
        """Def which enforces uniqueness of email addresses."""
        email = self.cleaned_data['email'].lower()

        r = User.objects.filter(email=email)

        if r.count() == 0:
            raise ValidationError("Email ID does not exist")

        return email
