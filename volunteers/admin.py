from django.contrib import admin
from django.utils import timezone
from .models import Skill, Volunteer, VolunteerEvent, VolunteerTask, PartnerInquiry


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']
    search_fields = ['name']


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'status', 'total_hours', 'joined_date', 'created_at']
    list_filter = ['status', 'country', 'joined_date']
    search_fields = ['full_name', 'email', 'phone', 'city']
    date_hierarchy = 'joined_date'
    readonly_fields = ['total_hours', 'created_at', 'updated_at']
    filter_horizontal = ['skills']

    fieldsets = (
        ('Personal Information', {
            'fields': ('user', 'full_name', 'email', 'phone', 'date_of_birth')
        }),
        ('Address', {
            'fields': ('address', 'city', 'country')
        }),
        ('Skills & Interests', {
            'fields': ('skills', 'interests', 'availability', 'bio')
        }),
        ('Profile', {
            'fields': ('profile_picture', 'status')
        }),
        ('Metrics', {
            'fields': ('total_hours', 'joined_date'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['approve_volunteers', 'deactivate_volunteers']

    def approve_volunteers(self, request, queryset):
        queryset.update(status='active')
    approve_volunteers.short_description = "Approve selected volunteers"

    def deactivate_volunteers(self, request, queryset):
        queryset.update(status='inactive')
    deactivate_volunteers.short_description = "Deactivate selected volunteers"


@admin.register(VolunteerEvent)
class VolunteerEventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'location', 'start_date', 'status', 'max_volunteers', 'created_at']
    list_filter = ['event_type', 'status', 'start_date']
    search_fields = ['title', 'description', 'location']
    date_hierarchy = 'start_date'
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['registered_volunteers']

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'event_type', 'project')
        }),
        ('Location & Time', {
            'fields': ('location', 'start_date', 'end_date')
        }),
        ('Volunteers', {
            'fields': ('max_volunteers', 'registered_volunteers')
        }),
        ('Status', {
            'fields': ('status', 'created_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(VolunteerTask)
class VolunteerTaskAdmin(admin.ModelAdmin):
    list_display = ['volunteer', 'title', 'date', 'hours_logged', 'status', 'verified_by', 'created_at']
    list_filter = ['status', 'date', 'verified_by']
    search_fields = ['volunteer__full_name', 'title', 'description']
    date_hierarchy = 'date'
    readonly_fields = ['created_at', 'updated_at', 'verified_at']

    fieldsets = (
        ('Task Information', {
            'fields': ('volunteer', 'event', 'title', 'description')
        }),
        ('Time Tracking', {
            'fields': ('date', 'hours_logged', 'status')
        }),
        ('Verification', {
            'fields': ('verified_by', 'verified_at', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['verify_tasks']

    def verify_tasks(self, request, queryset):
        for task in queryset:
            task.status = 'completed'
            task.verified_by = request.user
            task.verified_at = timezone.now()
            task.save()
    verify_tasks.short_description = "Verify and complete selected tasks"


@admin.register(PartnerInquiry)
class PartnerInquiryAdmin(admin.ModelAdmin):
    list_display = ['organization_name', 'contact_person', 'email', 'partnership_type', 'status', 'created_at']
    list_filter = ['partnership_type', 'status', 'created_at']
    search_fields = ['organization_name', 'contact_person', 'email', 'message']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'reviewed_at']

    fieldsets = (
        ('Organization Information', {
            'fields': ('organization_name', 'contact_person', 'email', 'phone')
        }),
        ('Partnership Details', {
            'fields': ('partnership_type', 'message')
        }),
        ('Review', {
            'fields': ('status', 'reviewed_by', 'reviewed_at', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_as_reviewing', 'approve_inquiries', 'reject_inquiries']

    def mark_as_reviewing(self, request, queryset):
        queryset.update(status='reviewing')
    mark_as_reviewing.short_description = "Mark as under review"

    def approve_inquiries(self, request, queryset):
        for inquiry in queryset:
            inquiry.status = 'approved'
            inquiry.reviewed_by = request.user
            inquiry.reviewed_at = timezone.now()
            inquiry.save()
    approve_inquiries.short_description = "Approve selected inquiries"

    def reject_inquiries(self, request, queryset):
        for inquiry in queryset:
            inquiry.status = 'rejected'
            inquiry.reviewed_by = request.user
            inquiry.reviewed_at = timezone.now()
            inquiry.save()
    reject_inquiries.short_description = "Reject selected inquiries"
