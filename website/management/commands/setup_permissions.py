from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from donations.models import Donation, BankTransfer
from volunteers.models import Volunteer, VolunteerEvent, VolunteerTask
from website.models import Project, NewsArticle, Partner
from dashboard.models import TransparencyMetric, FinancialReport


class Command(BaseCommand):
    help = 'Set up user groups and permissions'

    def handle(self, *args, **kwargs):
        # Create groups
        staff_group, _ = Group.objects.get_or_create(name='Staff')
        volunteer_group, _ = Group.objects.get_or_create(name='Volunteer')
        donor_group, _ = Group.objects.get_or_create(name='Donor')
        
        self.stdout.write('Created groups: Staff, Volunteer, Donor')
        
        # Staff permissions - can manage content
        staff_permissions = [
            # Projects
            'add_project', 'change_project', 'view_project',
            # News
            'add_newsarticle', 'change_newsarticle', 'view_newsarticle',
            # Partners
            'add_partner', 'change_partner', 'view_partner',
            # Volunteers - view and manage
            'view_volunteer', 'change_volunteer',
            'view_volunteerevent', 'change_volunteerevent', 'add_volunteerevent',
            'view_volunteertask', 'change_volunteertask', 'add_volunteertask',
            # Donations - view only
            'view_donation', 'view_banktransfer',
        ]
        
        for perm_codename in staff_permissions:
            try:
                permission = Permission.objects.get(codename=perm_codename)
                staff_group.permissions.add(permission)
            except Permission.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Permission {perm_codename} not found'))
        
        self.stdout.write(self.style.SUCCESS('✓ Staff permissions configured'))
        
        # Volunteer permissions - can view their own data
        volunteer_permissions = [
            'view_volunteer',
            'view_volunteerevent',
            'view_volunteertask',
            'view_project',
            'view_newsarticle',
        ]
        
        for perm_codename in volunteer_permissions:
            try:
                permission = Permission.objects.get(codename=perm_codename)
                volunteer_group.permissions.add(permission)
            except Permission.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Permission {perm_codename} not found'))
        
        self.stdout.write(self.style.SUCCESS('✓ Volunteer permissions configured'))
        
        # Donor permissions - can view their donations
        donor_permissions = [
            'view_donation',
            'view_project',
            'view_newsarticle',
        ]
        
        for perm_codename in donor_permissions:
            try:
                permission = Permission.objects.get(codename=perm_codename)
                donor_group.permissions.add(permission)
            except Permission.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Permission {perm_codename} not found'))
        
        self.stdout.write(self.style.SUCCESS('✓ Donor permissions configured'))
        
        self.stdout.write(self.style.SUCCESS('\n✓ All permissions set up successfully!'))
        self.stdout.write('\nGroups created:')
        self.stdout.write('  - Staff: Can manage content and view volunteers/donations')
        self.stdout.write('  - Volunteer: Can view their own volunteer data')
        self.stdout.write('  - Donor: Can view their own donations')

