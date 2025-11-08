#!/usr/bin/env python
"""Script to set admin password"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sevo_website.settings')
django.setup()

from django.contrib.auth.models import User

user = User.objects.get(username='admin')
user.set_password('admin123')
user.save()
print("Admin password set to: admin123")

