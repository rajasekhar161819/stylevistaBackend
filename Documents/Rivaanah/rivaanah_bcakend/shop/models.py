from django.db import models
from accounts.models import User

class Product(models.Model):
    TEXTILE_TYPES = (
        ('saree', 'Saree'),
        ('lehenga', 'Lehenga'),
        ('kurta', 'Kurta'),
        ('Shirts', 'shirts'),
        ('t-shirts', 'T-shirts'),
    )
    SIZE_CHOICES = (
        ('XS', 'Extar Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),
        ('XXXL', 'Triple Extra Large'),
    )
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=TEXTILE_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sizes = models.JSONField(default=dict)
    colors = models.JSONField(default=dict, null=True, blank=True)
    description = models.TextField()
    details = models.JSONField(default=dict, null=True, blank=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    gallery = models.JSONField(default=dict, null=True, blank=True)
    rating = models.FloatField(null=True, blank=True, default=5.0)
    reviews = models.IntegerField(null=True, blank=True, default=1)
    inStock = models.BooleanField(null=True, blank=True, default=True)
    isNew = models.BooleanField(null=True, blank=True, default=True)
    isFeatured = models.BooleanField(null=True, blank=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    address= models.JSONField(default=dict, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
