from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse


class Project(models.Model):
    """Model for projects/initiatives"""

    CATEGORY_CHOICES = [
        ('water', 'Water'),
        ('education', 'Education'),
        ('health', 'Health'),
        ('women', "Women's Empowerment"),
        ('agriculture', 'Agriculture'),
        ('youth', 'Youth'),
    ]

    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('paused', 'Paused'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(help_text="Short description for cards")
    full_description = models.TextField(help_text="Full project details")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning')
    location = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    progress_percentage = models.IntegerField(default=0)
    featured_image = models.ImageField(upload_to='projects/', null=True, blank=True)
    metrics = models.JSONField(default=dict, blank=True, help_text="Project metrics as JSON")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        # Calculate progress percentage
        if self.target_amount > 0:
            self.progress_percentage = int((self.current_amount / self.target_amount) * 100)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'slug': self.slug})


class NewsArticle(models.Model):
    """Model for news articles and blog posts"""

    CATEGORY_CHOICES = [
        ('success_story', 'Success Story'),
        ('event', 'Event'),
        ('update', 'Update'),
        ('press', 'Press'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    excerpt = models.TextField(help_text="Short excerpt for cards")
    content = models.TextField(help_text="Full article content")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='articles')
    featured_image = models.ImageField(upload_to='news/', null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    views_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name_plural = 'News Articles'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'slug': self.slug})


class Partner(models.Model):
    """Model for partner organizations"""

    PARTNERSHIP_TYPE_CHOICES = [
        ('funding', 'Funding Partner'),
        ('program', 'Program Partner'),
        ('technical', 'Technical Support'),
    ]

    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='partners/', null=True, blank=True)
    website = models.URLField(blank=True)
    partnership_type = models.CharField(max_length=20, choices=PARTNERSHIP_TYPE_CHOICES)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    joined_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    """Model for contact form submissions"""

    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    replied_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"
