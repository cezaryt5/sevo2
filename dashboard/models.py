from django.db import models
from django.utils import timezone


class TransparencyMetric(models.Model):
    """Model for transparency dashboard metrics"""

    METRIC_TYPE_CHOICES = [
        ('donation_total', 'Total Donations'),
        ('projects_funded', 'Projects Funded'),
        ('people_helped', 'People Helped'),
        ('volunteers_active', 'Active Volunteers'),
        ('wells_built', 'Wells Built'),
        ('students_sponsored', 'Students Sponsored'),
        ('families_supported', 'Families Supported'),
    ]

    PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
        ('all_time', 'All Time'),
    ]

    metric_type = models.CharField(max_length=50, choices=METRIC_TYPE_CHOICES)
    value = models.DecimalField(max_digits=15, decimal_places=2)
    period = models.CharField(max_length=20, choices=PERIOD_CHOICES)
    date = models.DateField(default=timezone.now)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', 'metric_type']
        unique_together = ['metric_type', 'period', 'date']

    def __str__(self):
        return f"{self.get_metric_type_display()} - {self.period} - {self.date}"


class FinancialReport(models.Model):
    """Model for annual financial reports"""

    title = models.CharField(max_length=200)
    year = models.IntegerField()

    # Financial Breakdown
    total_donations = models.DecimalField(max_digits=12, decimal_places=2)
    program_expenses_percentage = models.DecimalField(max_digits=5, decimal_places=2, help_text="Percentage spent on programs")
    fundraising_expenses_percentage = models.DecimalField(max_digits=5, decimal_places=2, help_text="Percentage spent on fundraising")
    admin_expenses_percentage = models.DecimalField(max_digits=5, decimal_places=2, help_text="Percentage spent on administration")

    # Report File
    report_file = models.FileField(upload_to='reports/', help_text="PDF report file")

    # Publishing
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-year']
        unique_together = ['year']

    def __str__(self):
        return f"{self.title} - {self.year}"

    def save(self, *args, **kwargs):
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)
