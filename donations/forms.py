from django import forms
from django.core.exceptions import ValidationError
from .models import Donation, BankTransfer
from website.models import Project


class DonationForm(forms.ModelForm):
    """Base donation form with enhanced validation"""

    class Meta:
        model = Donation
        fields = [
            'donor_name', 'donor_email', 'donor_phone',
            'amount', 'currency', 'donation_type',
            'payment_method', 'project', 'message', 'is_anonymous'
        ]
        widgets = {
            'donor_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name'
            }),
            'donor_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com'
            }),
            'donor_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+249 XXX XXX XXX'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '100',
                'min': '1',
                'step': '0.01'
            }),
            'currency': forms.Select(attrs={'class': 'form-control'}),
            'donation_type': forms.Select(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'project': forms.Select(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Optional message...',
                'rows': 3
            }),
            'is_anonymous': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        error_messages = {
            'donor_name': {
                'required': 'Please enter your name.',
            },
            'donor_email': {
                'required': 'Please enter your email address.',
                'invalid': 'Please enter a valid email address.',
            },
            'amount': {
                'required': 'Please enter a donation amount.',
                'invalid': 'Please enter a valid amount.',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make project optional
        self.fields['project'].required = False
        self.fields['project'].empty_label = "General Fund"
        # Filter only active projects
        self.fields['project'].queryset = Project.objects.filter(
            status__in=['planning', 'ongoing']
        )
        # Add help text
        self.fields['amount'].help_text = 'Minimum donation: 1 SDG or equivalent'
        self.fields['is_anonymous'].help_text = 'Check this if you want to remain anonymous'

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount and amount < 1:
            raise ValidationError('Donation amount must be at least 1.')
        if amount and amount > 1000000:
            raise ValidationError('Donation amount seems unusually high. Please contact us directly for large donations.')
        return amount

    def clean_donor_name(self):
        name = self.cleaned_data.get('donor_name')
        if name and len(name) < 2:
            raise ValidationError('Please enter your full name.')
        return name


class BankTransferForm(forms.ModelForm):
    """Form for Sudan bank transfer details with validation"""

    class Meta:
        model = BankTransfer
        fields = ['bank_name', 'account_number', 'payment_proof']
        widgets = {
            'bank_name': forms.Select(attrs={'class': 'form-control'}),
            'account_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your account number (optional)'
            }),
            'payment_proof': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*,.pdf'
            }),
        }
        help_texts = {
            'payment_proof': 'Upload a screenshot or photo of your bank transfer receipt (JPG, PNG, or PDF)',
        }
        error_messages = {
            'bank_name': {
                'required': 'Please select your bank.',
            },
            'payment_proof': {
                'required': 'Please upload proof of your bank transfer.',
            },
        }

    def clean_payment_proof(self):
        proof = self.cleaned_data.get('payment_proof')
        if proof:
            # Check file size (max 5MB)
            if proof.size > 5 * 1024 * 1024:
                raise ValidationError('File size must be under 5MB.')
            # Check file type
            allowed_types = ['image/jpeg', 'image/png', 'image/jpg', 'application/pdf']
            if proof.content_type not in allowed_types:
                raise ValidationError('Only JPG, PNG, and PDF files are allowed.')
        return proof

