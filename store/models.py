from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    image = models.ImageField(upload_to='user_profiles/')
    company = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    status = models.IntegerField(default=0)

    # Admin status: 1
    # Seller status: 2
    # Customer status: 3

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'


class Category(models.Model):
    title = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ['-id']


class Product(models.Model):
    image = models.ImageField(upload_to='product_images')
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_count = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Order #{self.pk} - User: {self.user.username}, Product: {self.product.title}"


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return f'Cart of {self.user.username}'
