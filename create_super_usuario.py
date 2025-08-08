# create_superuser.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Django2.settings')  # Ajuste para seu settings
django.setup()

from django.contrib.auth.models import User

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'sua_senha')
    print("Super usuário criado.")
else:
    print("Super usuário já existe.")