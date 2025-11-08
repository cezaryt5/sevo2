from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Skill(models.Model):
    """Model for volunteer skills"""

    CATEGORY_CHOICES = [
        ('technical', 'Technical'),
        ('medical', 'Medical'),
        ('education', 'Education'),
        ('administrative', 'Administrative'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Volunteer(models.Model):
    """Model for volunteer profiles"""

    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    # Link to User account (optional - volunteers can register without account)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='volunteer_profile')

    # Personal Information
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField(null=True, blank=True)

    # Address
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default='Sudan')

    # Skills and Interests
    skills = models.ManyToManyField(Skill, blank=True, related_name='volunteers')
    interests = models.JSONField(default=list, blank=True, help_text="Areas of interest as JSON array")
    availability = models.TextField(blank=True, help_text="Volunteer availability description")
    bio = models.TextField(blank=True, help_text="Short bio about the volunteer")

    # Profile
    profile_picture = models.ImageField(upload_to='volunteers/', null=True, blank=True)

    # Status and Metrics
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_hours = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    joined_date = models.DateField(default=timezone.now)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.full_name

    @property
    def completed_tasks_count(self):
        return self.tasks.filter(status='completed').count()

    @property
    def events_participated(self):
        return self.events.count()


class VolunteerEvent(models.Model):
    """Model for volunteer events and activities"""

    EVENT_TYPE_CHOICES = [
        ('training', 'Training'),
        ('field_work', 'Field Work'),
        ('fundraising', 'Fundraising'),
        ('awareness', 'Awareness Campaign'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES)
    location = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    max_volunteers = models.IntegerField(default=10)
    registered_volunteers = models.ManyToManyField(Volunteer, blank=True, related_name='events')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_events')
    project = models.ForeignKey('website.Project', on_delete=models.SET_NULL, null=True, blank=True, related_name='volunteer_events')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return self.title

    @property
    def is_full(self):
        return self.registered_volunteers.count() >= self.max_volunteers

    @property
    def spots_remaining(self):
        return max(0, self.max_volunteers - self.registered_volunteers.count())


class VolunteerTask(models.Model):
    """Model for volunteer tasks and hour tracking"""

    STATUS_CHOICES = [
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE, related_name='tasks')
    event = models.ForeignKey(VolunteerEvent, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField()
    hours_logged = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='assigned')
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_tasks')
    verified_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.volunteer.full_name} - {self.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update volunteer's total hours
        if self.status == 'completed' and self.verified_by:
            self.volunteer.total_hours = self.volunteer.tasks.filter(
                status='completed',
                verified_by__isnull=False
            ).aggregate(models.Sum('hours_logged'))['hours_logged__sum'] or 0
            self.volunteer.save()


class PartnerInquiry(models.Model):
    """Model for partnership inquiries"""

    PARTNERSHIP_TYPE_CHOICES = [
        ('funding', 'Funding Partner'),
        ('program', 'Program Partner'),
        ('technical', 'Technical Support'),
    ]

    STATUS_CHOICES = [
        ('new', 'New'),
        ('reviewing', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    organization_name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    partnership_type = models.CharField(max_length=20, choices=PARTNERSHIP_TYPE_CHOICES)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_partnerships')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, help_text="Internal notes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Partner Inquiries'

    def __str__(self):
        return f"{self.organization_name} - {self.partnership_type}"
