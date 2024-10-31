from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Settings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="settings")
    apps_to_block = models.JSONField(default=list)  # Array of app names to block

    def __str__(self):
        return f"Settings for {self.user.username}"
