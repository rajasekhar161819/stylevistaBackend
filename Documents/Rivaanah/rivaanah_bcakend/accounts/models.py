from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('rivaanah-admin3304$', 'Rivaanah Admin'),
    )

    class GenderChoices(models.TextChoices):
        MALE = 'male', 'Male'
        FEMALE = 'female', 'Female'

    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)  
    date_of_birth = models.DateField(blank=True,null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    gender = models.CharField(max_length=50, choices=GenderChoices.choices, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    address = models.JSONField(default=dict, blank=True, null=True)