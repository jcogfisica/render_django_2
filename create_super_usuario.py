# create_superuser.py
from django.contrib.auth import get_user_model

User = get_user_model()

username = "jcogfisica"
email = "jcogfisica@yahoo.com.br"
password = "MON010deo010"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("✅ Superusuário criado com sucesso!")
else:
    user = User.objects.get(username=username)
    user.set_password(password)
    user.save()
    print("🔄 Senha do superusuário atualizada!")