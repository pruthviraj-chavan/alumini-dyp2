from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import VerificationRequest

User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    """Form for user registration"""
    role = forms.ChoiceField(choices=[('STUDENT', 'Student'), ('ALUMNI', 'Alumni')])
    branch = forms.CharField(max_length=100, required=True)
    year = forms.CharField(max_length=10, required=True, help_text="Current year for students, passing year for alumni")
    phone = forms.CharField(max_length=15, required=True)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'role', 'branch', 'year', 'phone', 'bio', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']
        user.branch = self.cleaned_data['branch']
        user.year = self.cleaned_data['year']
        user.phone = self.cleaned_data['phone']
        user.bio = self.cleaned_data['bio']
        
        if commit:
            user.save()
        return user

class UserLoginForm(AuthenticationForm):
    """Form for user login"""
    username = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True}))

class VerificationRequestForm(forms.ModelForm):
    """Form for student verification request"""
    student_number = forms.CharField(max_length=50, required=True, help_text="Your student ID number")
    verification_document = forms.FileField(required=False, help_text="Upload your student ID card or any other proof")
    additional_info = forms.CharField(widget=forms.Textarea, required=False, help_text="Any additional information to help verify your identity")
    
    class Meta:
        model = VerificationRequest
        fields = ['student_number', 'verification_document', 'additional_info']

class UserProfileUpdateForm(forms.ModelForm):
    """Form for updating user profile"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'branch', 'year', 'bio')
