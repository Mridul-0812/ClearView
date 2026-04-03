from django.apps import AppConfig
from django.db.models.signals import post_migrate

def cleanup_database(sender, **kwargs):
    from django.contrib.auth.models import User
    
    # 1. Define the lists of what you want to get rid of
    usernames_to_delete = ['Mridul-G', 'Mridul-0812', 'Mridul-0812G'] 
    emails_to_delete = ['guptamridul2009@gmail.com', 'guptamridul2009+1@gmail.com']

    # 2. Delete by username
    deleted_users = User.objects.filter(username__in=usernames_to_delete).delete()
    
    # 3. Delete by email
    deleted_emails = User.objects.filter(email__in=emails_to_delete).delete()

    # This will show up in your Render Logs so you know it worked
    print(f"--- CLEANUP COMPLETE: Removed {deleted_users[0]} usernames and {deleted_emails[0]} emails ---")

class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'

    def ready(self):
        # This runs every time the server restarts on Render
        post_migrate.connect(cleanup_database, sender=self)