from django.contrib import admin
from django.utils import timezone
from .models import Donation, BankTransfer, DonationGoal


class BankTransferInline(admin.StackedInline):
    model = BankTransfer
    extra = 0
    readonly_fields = ['created_at', 'verified_at']


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['donor_name', 'amount', 'currency', 'payment_method', 'payment_status', 'created_at']
    list_filter = ['payment_method', 'payment_status', 'currency', 'donation_type', 'created_at']
    search_fields = ['donor_name', 'donor_email', 'transaction_id', 'receipt_number']
    date_hierarchy = 'created_at'
    readonly_fields = ['transaction_id', 'receipt_number', 'created_at', 'updated_at', 'completed_at']
    inlines = [BankTransferInline]

    fieldsets = (
        ('Donor Information', {
            'fields': ('donor_name', 'donor_email', 'donor_phone', 'user')
        }),
        ('Donation Details', {
            'fields': ('amount', 'currency', 'donation_type', 'payment_method', 'payment_status')
        }),
        ('Transaction', {
            'fields': ('transaction_id', 'receipt_number', 'project')
        }),
        ('Additional', {
            'fields': ('message', 'is_anonymous')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_as_completed', 'mark_as_failed']

    def mark_as_completed(self, request, queryset):
        queryset.update(payment_status='completed', completed_at=timezone.now())
    mark_as_completed.short_description = "Mark selected donations as completed"

    def mark_as_failed(self, request, queryset):
        queryset.update(payment_status='failed')
    mark_as_failed.short_description = "Mark selected donations as failed"


@admin.register(BankTransfer)
class BankTransferAdmin(admin.ModelAdmin):
    list_display = ['donation', 'bank_name', 'verification_status', 'verified_by', 'created_at']
    list_filter = ['bank_name', 'verification_status', 'created_at']
    search_fields = ['donation__donor_name', 'donation__donor_email', 'account_number']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'verified_at']

    fieldsets = (
        ('Transfer Details', {
            'fields': ('donation', 'bank_name', 'account_number', 'payment_proof')
        }),
        ('Verification', {
            'fields': ('verification_status', 'verified_by', 'verified_at', 'rejection_reason')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    actions = ['verify_transfer', 'reject_transfer']

    def verify_transfer(self, request, queryset):
        for transfer in queryset:
            transfer.verification_status = 'verified'
            transfer.verified_by = request.user
            transfer.verified_at = timezone.now()
            transfer.save()

            # Update donation status
            transfer.donation.payment_status = 'completed'
            transfer.donation.completed_at = timezone.now()
            transfer.donation.save()
    verify_transfer.short_description = "Verify selected bank transfers"

    def reject_transfer(self, request, queryset):
        queryset.update(verification_status='rejected')
    reject_transfer.short_description = "Reject selected bank transfers"


@admin.register(DonationGoal)
class DonationGoalAdmin(admin.ModelAdmin):
    list_display = ['title', 'target_amount', 'current_amount', 'progress_percentage', 'is_active', 'start_date', 'end_date']
    list_filter = ['is_active', 'start_date', 'end_date']
    search_fields = ['title', 'description']
    date_hierarchy = 'start_date'
    readonly_fields = ['current_amount', 'created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'project')
        }),
        ('Financial', {
            'fields': ('target_amount', 'current_amount', 'currency')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
