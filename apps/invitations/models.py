import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone

class Invitation(models.Model):
    code = models.CharField(max_length=20, unique=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_invitations')
    used_by = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='used_invitation')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    def is_valid(self):
        return self.used_by is None and self.expires_at > timezone.now()

    def __str__(self):
        return f"{self.code} ({'Benutzt' if self.used_by else 'Frei'})"
