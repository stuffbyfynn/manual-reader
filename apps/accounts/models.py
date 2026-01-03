from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email ist erforderlich')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('status', 'active')
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField('E-Mail-Adresse', unique=True)
    
    STATUS_CHOICES = (
        ('pending', 'Wartend auf Freigabe'),
        ('active', 'Aktiv'),
        ('blocked', 'Gesperrt'),
    )
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='pending')
    last_session_key = models.CharField(max_length=40, null=True, blank=True)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices')
    fingerprint = models.CharField(max_length=255)
    user_agent = models.TextField()
    ip_address = models.GenericIPAddressField()
    is_approved = models.BooleanField(default=False)
    last_seen = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'fingerprint')

    def __str__(self):
        return f"{self.user.email} - {self.fingerprint[:8]}"
