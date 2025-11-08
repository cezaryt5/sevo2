from django import forms
from django.core.exceptions import ValidationError
from .models import Volunteer, PartnerInquiry
from datetime import date, timedelta


class VolunteerRegistrationForm(forms.ModelForm):
    """Volunteer registration form with enhanced validation"""

    class Meta:
        model = Volunteer
        fields = [
            'full_name', 'email', 'phone',
            'date_of_birth', 'address', 'city',
            'skills', 'availability', 'bio', 'profile_picture'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+249 XXX XXX XXX'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Street Address'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City'
            }),
            'skills': forms.CheckboxSelectMultiple(),
            'availability': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Weekends, Evenings, Full-time',
                'rows': 2
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tell us about yourself and why you want to volunteer...',
                'rows': 4
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
        help_texts = {
            'skills': 'Select all that apply',
            'profile_picture': 'Optional: Upload a profile photo',
            'date_of_birth': 'You must be at least 16 years old to volunteer',
        }
        error_messages = {
            'full_name': {
                'required': 'Please enter your full name.',
            },
            'email': {
                'required': 'Please enter your email address.',
                'invalid': 'Please enter a valid email address.',
            },
            'date_of_birth': {
                'required': 'Please enter your date of birth.',
            },
        }

    def clean_full_name(self):
        name = self.cleaned_data.get('full_name')
        if name and len(name) < 3:
            raise ValidationError('Please enter your full name (at least 3 characters).')
        return name

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        if dob:
            # Check if volunteer is at least 16 years old
            min_age_date = date.today() - timedelta(days=16*365)
            if dob > min_age_date:
                raise ValidationError('You must be at least 16 years old to volunteer.')
            # Check if date is not in the future
            if dob > date.today():
                raise ValidationError('Date of birth cannot be in the future.')
        return dob

    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture:
            # Check file size (max 2MB)
            if picture.size > 2 * 1024 * 1024:
                raise ValidationError('Image size must be under 2MB.')
            # Check file type
            allowed_types = ['image/jpeg', 'image/png', 'image/jpg']
            if picture.content_type not in allowed_types:
                raise ValidationError('Only JPG and PNG images are allowed.')
        return picture

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Check if email already exists
        if email and Volunteer.objects.filter(email=email).exists():
            raise ValidationError('A volunteer with this email already exists.')
        return email


class PartnerInquiryForm(forms.ModelForm):
    """Partnership inquiry form with validation"""

    class Meta:
        model = PartnerInquiry
        fields = [
            'organization_name', 'contact_person', 'email',
            'phone', 'partnership_type', 'message'
        ]
        widgets = {
            'organization_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Organization Name'
            }),
            'contact_person': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contact Person Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'organization@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+XXX XXX XXX XXX'
            }),
            'partnership_type': forms.Select(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tell us about your organization and how you would like to partner with SEVO...',
                'rows': 5
            }),
        }
        error_messages = {
            'organization_name': {
                'required': 'Please enter your organization name.',
            },
            'contact_person': {
                'required': 'Please enter the contact person name.',
            },
            'email': {
                'required': 'Please enter your email address.',
                'invalid': 'Please enter a valid email address.',
            },
            'message': {
                'required': 'Please tell us about your partnership proposal.',
            },
        }

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if message and len(message) < 20:
            raise ValidationError('Please provide more details about your partnership proposal (at least 20 characters).')
        return message

    def clean_organization_name(self):
        name = self.cleaned_data.get('organization_name')
        if name and len(name) < 3:
            raise ValidationError('Organization name must be at least 3 characters.')
        return name

