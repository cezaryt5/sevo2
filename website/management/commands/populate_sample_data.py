from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from website.models import Project, NewsArticle, Partner
from donations.models import Donation, DonationGoal
from volunteers.models import Skill, Volunteer
from dashboard.models import TransparencyMetric, FinancialReport


class Command(BaseCommand):
    help = 'Populate database with sample data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')
        
        # Create admin user if doesn't exist
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@sevo.org',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Created admin user'))
        
        # Create Skills
        skills_data = [
            ('Teaching', 'education'),
            ('Medical Care', 'medical'),
            ('Engineering', 'technical'),
            ('Project Management', 'administrative'),
            ('Social Work', 'other'),
            ('Agriculture', 'technical'),
            ('IT Support', 'technical'),
        ]
        
        for skill_name, category in skills_data:
            Skill.objects.get_or_create(name=skill_name, category=category)
        self.stdout.write(self.style.SUCCESS(f'Created {len(skills_data)} skills'))
        
        # Create Projects
        projects_data = [
            {
                'title': 'Clean Water Initiative - Darfur',
                'description': 'Building wells to provide clean water access to rural communities in Darfur.',
                'full_description': 'This project aims to construct 10 water wells in remote villages of Darfur, providing clean water access to over 5,000 people. The wells will be equipped with hand pumps and maintained by trained local volunteers.',
                'category': 'water',
                'status': 'ongoing',
                'location': 'Darfur, Sudan',
                'target_amount': 50000,
                'current_amount': 32000,
            },
            {
                'title': 'Girls Education Program',
                'description': 'Sponsoring education for girls in rural Sudan.',
                'full_description': 'Supporting 200 girls with school fees, supplies, and mentorship to ensure they complete their education.',
                'category': 'education',
                'status': 'ongoing',
                'location': 'Khartoum, Sudan',
                'target_amount': 30000,
                'current_amount': 18000,
            },
            {
                'title': 'Women Empowerment Training',
                'description': 'Vocational training for women in tailoring and handicrafts.',
                'full_description': 'Providing vocational training to 100 women in tailoring, handicrafts, and small business management.',
                'category': 'women',
                'status': 'planning',
                'location': 'Omdurman, Sudan',
                'target_amount': 20000,
                'current_amount': 5000,
            },
            {
                'title': 'Mobile Health Clinic',
                'description': 'Bringing healthcare to remote communities.',
                'full_description': 'Operating a mobile health clinic to provide basic healthcare services to underserved areas.',
                'category': 'health',
                'status': 'completed',
                'location': 'Blue Nile State, Sudan',
                'target_amount': 40000,
                'current_amount': 40000,
            },
        ]
        
        for proj_data in projects_data:
            project, created = Project.objects.get_or_create(
                title=proj_data['title'],
                defaults={
                    **proj_data,
                    'start_date': timezone.now().date() - timedelta(days=90),
                    'end_date': timezone.now().date() + timedelta(days=180),
                }
            )
            if created:
                self.stdout.write(f'Created project: {project.title}')
        
        # Create News Articles
        news_data = [
            {
                'title': 'New Water Well Completed in Darfur Village',
                'excerpt': 'Community celebrates access to clean water after years of hardship.',
                'content': 'After months of hard work, we are proud to announce the completion of a new water well in a remote Darfur village. This well will serve over 500 people and significantly improve their quality of life.',
                'category': 'success_story',
                'is_featured': True,
            },
            {
                'title': 'Annual Fundraising Gala Announced',
                'excerpt': 'Join us for our biggest fundraising event of the year.',
                'content': 'We are excited to announce our annual fundraising gala on December 15th. The event will feature traditional Sudanese music, food, and stories from our beneficiaries.',
                'category': 'event',
                'is_featured': False,
            },
            {
                'title': '100 Girls Graduate from Education Program',
                'excerpt': 'Celebrating the success of our girls education initiative.',
                'content': 'We are thrilled to celebrate the graduation of 100 girls from our education sponsorship program. These young women are now equipped to pursue higher education and careers.',
                'category': 'success_story',
                'is_featured': False,
            },
        ]
        
        for news in news_data:
            article, created = NewsArticle.objects.get_or_create(
                title=news['title'],
                defaults={
                    **news,
                    'author': admin_user,
                    'published_at': timezone.now() - timedelta(days=10),
                }
            )
            if created:
                self.stdout.write(f'Created news article: {article.title}')
        
        # Create Partners
        partners_data = [
            {'name': 'UN Women', 'partnership_type': 'funding', 'joined_date': timezone.now().date()},
            {'name': 'UNICEF Sudan', 'partnership_type': 'program', 'joined_date': timezone.now().date()},
            {'name': 'Water.org', 'partnership_type': 'technical', 'joined_date': timezone.now().date()},
        ]

        for partner_data in partners_data:
            partner, created = Partner.objects.get_or_create(
                name=partner_data['name'],
                defaults=partner_data
            )
            if created:
                self.stdout.write(f'Created partner: {partner.name}')
        
        # Create Transparency Metrics
        TransparencyMetric.objects.get_or_create(
            metric_type='wells_built',
            period='all_time',
            defaults={'value': 45, 'date': timezone.now().date()}
        )
        TransparencyMetric.objects.get_or_create(
            metric_type='women_trained',
            period='all_time',
            defaults={'value': 1200, 'date': timezone.now().date()}
        )
        TransparencyMetric.objects.get_or_create(
            metric_type='people_helped',
            period='all_time',
            defaults={'value': 45000, 'date': timezone.now().date()}
        )
        
        self.stdout.write(self.style.SUCCESS('Created transparency metrics'))
        
        # Create Financial Report
        FinancialReport.objects.get_or_create(
            year=2024,
            defaults={
                'title': '2024 Annual Financial Report',
                'total_donations': 250000,
                'program_expenses_percentage': 85,
                'fundraising_expenses_percentage': 10,
                'admin_expenses_percentage': 5,
                'is_published': True,
                'published_at': timezone.now(),
            }
        )
        
        self.stdout.write(self.style.SUCCESS('Created financial report'))
        
        self.stdout.write(self.style.SUCCESS('✓ Sample data population complete!'))

