from django.db import models
from farmers.models import Product
from buyers.models import Buyer

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Automatically calculate total_price based on product price_per_unit
        if self.product.price_per_unit:
            self.total_price = self.product.price_per_unit * self.quantity
        else:
            self.total_price = 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.id} - {self.product.crop_type} for {self.buyer.user.full_name}"
