import os
from typing import Optional
from allauth.socialaccount.models import SocialApp
from django.apps import apps
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.core.management import call_command
from app.models import Hazard
from app.factories import DisasterFactory

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Clear existing data')

    def handle(self, *args, **options):

        clear = options['clear']

        if clear:
            call_command('flush', '--noinput')
            self.stdout.write(self.style.SUCCESS('Successfully cleaned existing data'))

        """Seed inital data"""
        self.load_fixtures('hazard')
        self.load_fixtures('location')

        groups = ['volunteers']
        for group in groups:
            self.create_group(group)

        self.create_admin()

        site = self.create_site()
        social_app, _ = self.create_socials()

        # Add to site
        if site not in social_app.sites.all():
            social_app.sites.add(site)
            self.stdout.write(self.style.SUCCESS(f'Added OAuth app to site: {site.domain}'))
        
        self.create_disasters(10)

    def create_group(self, group_name):
        if not Group.objects.filter(name=group_name).exists():
            Group.objects.create(name=group_name)
            self.stdout.write(self.style.SUCCESS(f'Successfully created group "{group_name}"'))
        else:
            self.stdout.write(self.style.WARNING(f'Group "{group_name}" already exists'))
    
    def create_admin(self) -> Optional[User]:
        # Create a superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            user = User.objects.create_superuser('admin', 'admin@mdrf.pk', 'admin')
            self.stdout.write(self.style.SUCCESS('Successfully created superuser "admin"'))
            return user
        else:
            self.stdout.write(self.style.WARNING('Superuser "admin" already exists'))

    # def assign_group_user(self, group_name, username):
    #     user = User.objects.get(username=username)
    #     group = Group.objects.get(name=group_name)

    #     if not group.user_set.filter(username=username).exists():
    #         group.user_set.add(user)
    #         self.stdout.write(self.style.SUCCESS(f'{username} assigned to group: "{group_name}"'))
    #     else:
    #         self.stdout.write(self.style.WARNING(f'{username} user already in group "{group_name}"'))

    def load_fixtures(self, name):
        # Load hazard data from fixture
        model = apps.get_model('app', name)
        data = model.objects.all()
        if not data.exists():
            call_command('loaddata', f'{name}.json', verbosity=1)
            self.stdout.write(self.style.SUCCESS(f'Successfully loaded {model} fixture data'))
        else:
            self.stdout.write(self.style.WARNING('Hazard data already exists, skipping fixture loading'))

    def create_site(self) -> Site:
        # Update site for local development
        site = Site.objects.get_current()
        site.domain = 'localhost:8000'
        site.name = 'Local Development'
        site.save()
        self.stdout.write(self.style.SUCCESS('Successfully updated site for local development'))
        return site

    def create_socials(self) -> tuple[SocialApp, bool]: 
        # Setup Google OAuth SocialApp
        client_id = os.getenv('GOOGLE_OAUTH2_CLIENT_ID')
        client_secret = os.getenv('GOOGLE_OAUTH2_CLIENT_SECRET')

        social_app, created = SocialApp.objects.get_or_create(
            provider='google',
            name='Google OAuth',
            client_id=client_id,
            secret=client_secret,
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created Google OAuth SocialApp'))
        else:
            self.stdout.write(self.style.WARNING('Google OAuth SocialApp already exists'))

        return (social_app, created)
    
    def create_disasters(self, num=10):
        DisasterFactory.create_batch(num)
        self.stdout.write(self.style.SUCCESS('Successfully created disasters'))