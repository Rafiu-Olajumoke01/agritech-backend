from django.db import models
from users.models import CustomUser

class Farmer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    farm_name = models.CharField(max_length=255)
    farm_location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.farm_name


class Product(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='products')
    crop_type = models.CharField(max_length=100)  
    quantity_with_unit = models.CharField(max_length=50)  
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.farmer.farm_name} - {self.crop_type} ({self.quantity_with_unit})"
