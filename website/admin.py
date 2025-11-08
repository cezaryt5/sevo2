from django.contrib import admin
from .models import Project, NewsArticle, Partner, ContactMessage


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'location', 'progress_percentage', 'start_date', 'created_at']
    list_filter = ['category', 'status', 'start_date']
    search_fields = ['title', 'description', 'location']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'start_date'
    readonly_fields = ['progress_percentage', 'created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'status')
        }),
        ('Description', {
            'fields': ('description', 'full_description')
        }),
        ('Location & Timeline', {
            'fields': ('location', 'start_date', 'end_date')
        }),
        ('Financial', {
            'fields': ('target_amount', 'current_amount', 'progress_percentage')
        }),
        ('Media & Metrics', {
            'fields': ('featured_image', 'metrics')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'is_featured', 'published_at', 'views_count', 'created_at']
    list_filter = ['category', 'is_featured', 'published_at']
    search_fields = ['title', 'excerpt', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    readonly_fields = ['views_count', 'created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'author')
        }),
        ('Content', {
            'fields': ('excerpt', 'content', 'featured_image')
        }),
        ('Publishing', {
            'fields': ('is_featured', 'published_at')
        }),
        ('Metrics', {
            'fields': ('views_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'partnership_type', 'is_active', 'joined_date', 'created_at']
    list_filter = ['partnership_type', 'is_active', 'joined_date']
    search_fields = ['name', 'description']
    date_hierarchy = 'joined_date'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']

    actions = ['mark_as_read', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as read"

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark selected messages as unread"
