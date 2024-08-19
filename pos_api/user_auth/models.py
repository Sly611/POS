from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin

# Create your models here.

class CustomBaseUserManager(BaseUserManager):
    
    def create_user(self, username,  email, password=None, **extra_fields):

        if not username:
            raise ValueError("user must have username")
        if not email:
            raise ValueError("user must have valid email")
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)  # Corrected save method
        return user
    
    def create_superuser(self, username, email, password=None,  **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)
        

class CustomUser(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=64, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomBaseUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def has_module_perms(self, app_label):
        return self.is_superuser
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser
    
    def __str__(self):
        return self.username