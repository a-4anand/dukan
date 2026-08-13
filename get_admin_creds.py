import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dukan.settings')
django.setup()

from django.contrib.auth.models import User

# Check if superuser exists
superusers = User.objects.filter(is_superuser=True)
if superusers.exists():
    su = superusers.first()
    su.set_password('admin123')
    su.save()
    print(f"Username: {su.username}")
    print(f"Password: admin123")
else:
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Username: admin")
    print("Password: admin123")
