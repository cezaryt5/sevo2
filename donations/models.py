from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


class Donation(models.Model):
    """Model for donation records"""

    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
        ('SDG', 'Sudanese Pound'),
    ]

    DONATION_TYPE_CHOICES = [
        ('one_time', 'One-time'),
        ('recurring', 'Recurring'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('paypal', 'PayPal'),
        ('stripe', 'Stripe'),
        ('bank_transfer', 'Bank Transfer'),
        ('crypto', 'Cryptocurrency'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    # Donor Information
    donor_name = models.CharField(max_length=200)
    donor_email = models.EmailField()
    donor_phone = models.CharField(max_length=20, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='donations')

    # Donation Details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    donation_type = models.CharField(max_length=20, choices=DONATION_TYPE_CHOICES, default='one_time')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')

    # Transaction Details
    transaction_id = models.CharField(max_length=200, unique=True, blank=True)
    receipt_number = models.CharField(max_length=50, unique=True, blank=True)

    # Optional Fields
    message = models.TextField(blank=True, help_text="Optional message from donor")
    is_anonymous = models.BooleanField(default=False)
    project = models.ForeignKey('website.Project', on_delete=models.SET_NULL, null=True, blank=True, related_name='donations')

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.donor_name} - {self.currency} {self.amount}"

    def save(self, *args, **kwargs):
        # Generate unique transaction ID if not exists
        if not self.transaction_id:
            self.transaction_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"

        # Generate receipt number if payment is completed
        if self.payment_status == 'completed' and not self.receipt_number:
            self.receipt_number = f"RCP-{timezone.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"
            if not self.completed_at:
                self.completed_at = timezone.now()

        super().save(*args, **kwargs)


class BankTransfer(models.Model):
    """Model for local Sudan bank transfer donations"""

    VERIFICATION_STATUS_CHOICES = [
        ('pending', 'Pending Verification'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]

    BANK_CHOICES = [
        ('Bank of Khartoum', 'Bank of Khartoum'),
        ('Faisal Islamic Bank', 'Faisal Islamic Bank'),
        ('Omdurman National Bank', 'Omdurman National Bank'),
        ('Al Baraka Bank', 'Al Baraka Bank'),
        ('Bank of Sudan', 'Bank of Sudan'),
    ]

    donation = models.OneToOneField(Donation, on_delete=models.CASCADE, related_name='bank_transfer')
    bank_name = models.CharField(max_length=100, choices=BANK_CHOICES)
    account_number = models.CharField(max_length=50, blank=True)
    payment_proof = models.FileField(upload_to='payment_proofs/')
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_STATUS_CHOICES, default='pending')
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_transfers')
    verified_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Bank Transfer - {self.donation.donor_name} - {self.bank_name}"


class DonationGoal(models.Model):
    """Model for donation goals/campaigns"""

    title = models.CharField(max_length=200)
    description = models.TextField()
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default='USD')
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    project = models.ForeignKey('website.Project', on_delete=models.SET_NULL, null=True, blank=True, related_name='goals')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def progress_percentage(self):
        if self.target_amount > 0:
            return int((self.current_amount / self.target_amount) * 100)
        return 0

    @property
    def is_completed(self):
        return self.current_amount >= self.target_amount
