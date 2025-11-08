from django.contrib import admin
from .models import TransparencyMetric, FinancialReport


@admin.register(TransparencyMetric)
class TransparencyMetricAdmin(admin.ModelAdmin):
    list_display = ['metric_type', 'value', 'period', 'date', 'created_at']
    list_filter = ['metric_type', 'period', 'date']
    search_fields = ['metric_type', 'notes']
    date_hierarchy = 'date'
    readonly_fields = ['created_at']

    fieldsets = (
        ('Metric Information', {
            'fields': ('metric_type', 'value', 'period', 'date')
        }),
        ('Additional', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(FinancialReport)
class FinancialReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'year', 'total_donations', 'is_published', 'published_at', 'created_at']
    list_filter = ['year', 'is_published', 'published_at']
    search_fields = ['title']
    date_hierarchy = 'created_at'
    readonly_fields = ['published_at', 'created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'year')
        }),
        ('Financial Breakdown', {
            'fields': ('total_donations', 'program_expenses_percentage',
                      'fundraising_expenses_percentage', 'admin_expenses_percentage')
        }),
        ('Report File', {
            'fields': ('report_file',)
        }),
        ('Publishing', {
            'fields': ('is_published', 'published_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['publish_reports', 'unpublish_reports']

    def publish_reports(self, request, queryset):
        queryset.update(is_published=True)
    publish_reports.short_description = "Publish selected reports"

    def unpublish_reports(self, request, queryset):
        queryset.update(is_published=False)
    unpublish_reports.short_description = "Unpublish selected reports"
