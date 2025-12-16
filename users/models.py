from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    role = models.CharField(max_length=10, choices=[("farmer","Farmer"),("buyer","Buyer")])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name','phone','role']
