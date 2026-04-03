from django.apps import AppConfig
from django.db.models.signals import post_migrate

def create_admin(sender, **kwargs):
    from django.contrib.auth.models import User
    # This creates a fresh account on Render's Postgres database
    if not User.objects.filter(username='Mridul-Render').exists():
        User.objects.create_superuser('Mridul-Render', 'your-email@example.com', 'YourPassword123!')

class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'

    def ready(self):
        post_migrate.connect(create_admin, sender=self)