from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('home', 'Home Products'),
        ('fresh', 'Fresh Fish'),
        ('sea', 'Sea Fish'),
        ('prawn', 'Prawns'),
        ('dry', 'Dry Fish'),
    ]

    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    

class Order(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('packed', 'Packed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ]

    PAYMENT_CHOICES = [
        ('gpay', 'GPay'),
        ('phonepe', 'PhonePe'),
        ('cod', 'Cash On Delivery'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    mobile = models.CharField(max_length=15)
    alt_mobile = models.CharField(max_length=15, blank=True, null=True)

    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    country = models.CharField(max_length=100)

    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    # price at the time of purchase (important!)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # ✅ total price (calculated)
    @property
    def total_price(self):
        return self.price * self.quantity

    # ✅ string representation (useful in admin panel)
    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

    # ✅ optional: save override (auto safety)
    def save(self, *args, **kwargs):
        # Ensure price is always set from product if not provided
        if not self.price:
            self.price = self.product.price
        super().save(*args, **kwargs)