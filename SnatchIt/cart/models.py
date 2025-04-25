from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Cart(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Cart for {self.user.username} - {self.status}"

    def total_cost(self):
        return sum(item.total_price() for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.title}"

    def total_price(self):
        return self.product.price * self.quantity

    def decrease_stock(self):
        if self.product.stock >= self.quantity:
            self.product.stock -= self.quantity
            self.product.save()
        else:
            raise ValueError("Not enough stock available.")
