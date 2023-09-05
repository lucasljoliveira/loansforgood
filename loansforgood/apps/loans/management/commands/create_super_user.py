from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create a super admin user"

    def handle(self, *args, **kwargs):
        username = settings.SUPER_USER_NAME
        email = settings.SUPER_USER_EMAIL
        password = settings.SUPER_USER_PASSWORD

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write(
                self.style.SUCCESS("Super admin user created successfully!")
            )
        else:
            self.stdout.write(self.style.SUCCESS("Super admin user already exists."))
