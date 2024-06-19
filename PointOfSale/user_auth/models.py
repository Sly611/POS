from django.db import models
# from django.contrib.auth.models import AbstractBaseUser
# from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.

# class CustomBaseUserManager(BaseUserManager):
    
#     def create_user(self, username, password, first_name, last_name, email, phone, gender, **extra_fields):

#         if not username:
#             raise ValueError("user must have username")
#         if not phone:
#             raise ValueError("user must have phone number")
#         if not email:
#             raise ValueError("user must have valid email")
        
#         user = self.model(username=username, first_name=first_name, last_name=last_name, email=email, phone=phone, gender=gender, **extra_fields)
#         user.set_password(password)
#         self.save(user)
#         return user
    
#     def create_super_user(self, username, password, email, gender, **extra_fields):
#         """
#         Creates and saves a superuser with the given phone number, password, and other fields.
#         """
#         user = self.create_user(username, password, email, gender, **extra_fields)
#         user.is_staff = True
#         user.is_superuser = True
#         self.save(user)
#         return user
        



class CustomUser(AbstractUser):
    role_choices = (
        ('manager', 'Manager'), 
        ('staff', 'Staff'), 
        ('security', 'Security'), 
        ('cleaner', 'Cleaner'),
        ('customer', 'Customer')
        )
    phone = models.CharField(max_length=11, unique=True)
    address = models.TextField()
    gender = models.CharField(max_length=32, choices=(('M', 'male'), ('F', 'female')))
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    role = models.CharField(max_length=64, choices=role_choices, blank=True, null=True)
    date_joined = models.DateField(auto_now_add=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['phone','role','gender']


    def __str__(self):
        return self.username


@receiver(post_save, sender=CustomUser)
def set_superuser(sender, instance, created, **kwargs):
    if created and instance.role == 'manager':
        instance.is_staff = True
        instance.is_superuser = True
        instance.save()
