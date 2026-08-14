from django.db import models

# Create your models here.
# models.py

from django.contrib.auth.models import User



class Rating(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    name = models.CharField(max_length=100, blank=True, null=True)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comments = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name if self.name else "Anonymous"} - {self.rating} Stars'


class Contact(models.Model):
    name = models.CharField(max_length=255)
    phone=models.IntegerField(max_length=10,null=True)
    message = models.TextField()
    category = models.CharField(max_length=50, choices=[('General', 'General'), ('Complaint', 'Complaint'), ('Suggestion', 'Suggestion')],null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, help_text="Category name (e.g. Dabeli, Pizza, Burger)")
    css_class = models.CharField(max_length=50, blank=True, editable=False)

    def save(self, *args, **kwargs):
        from django.utils.text import slugify
        self.css_class = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class MenuItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True, max_length=500)
    image_url = models.CharField(max_length=500, blank=True, null=True, help_text="Fallback for static images")
    order_link = models.URLField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name


class HomePageContent(models.Model):
    # Hero Section
    hero_title = models.CharField(max_length=200, default="TASTY")
    hero_subtitle = models.CharField(max_length=200, default="Treat Yourself: Relish Surat's tastiest Fast Food at Wallet-Friendly Prices!")
    hero_image = models.ImageField(upload_to='site_images/', blank=True, null=True, max_length=500)
    hero_image_url = models.CharField(max_length=500, blank=True, null=True, help_text="Fallback for static images")
    
    # About Section
    about_title = models.CharField(max_length=200, default="We Are Dinesh Dabeli")
    about_text = models.TextField()
    about_image = models.ImageField(upload_to='site_images/', blank=True, null=True, max_length=500)
    about_image_url = models.CharField(max_length=500, blank=True, null=True, help_text="Fallback for static images")

    def save(self, *args, **kwargs):
        from django.core.exceptions import ValidationError
        if self.__class__.objects.count() and not self.pk:
            raise ValidationError("You can only create one instance of Home Page Content.")
        super(HomePageContent, self).save(*args, **kwargs)

    def __str__(self):
        return "Home Page Content"

class Offer(models.Model):
    title = models.CharField(max_length=100)
    discount_text = models.CharField(max_length=50)
    image = models.ImageField(upload_to='offers/', blank=True, null=True, max_length=500)
    image_url = models.CharField(max_length=500, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class ShopSettings(models.Model):
    whatsapp_number = models.CharField(max_length=15, default='919876543210', help_text="WhatsApp number with country code, e.g. 919876543210")
    delivery_charge = models.DecimalField(max_digits=6, decimal_places=2, default=30.00, help_text="Delivery charge in ₹")
    free_delivery_above = models.DecimalField(max_digits=6, decimal_places=2, default=200.00, help_text="Free delivery for orders above this amount. Set to 0 to always charge.")
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="Discount percentage on total (0 for no discount)")
    discount_min_order = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, help_text="Minimum order amount to apply discount")
    is_delivery_available = models.BooleanField(default=True, help_text="Enable/disable delivery orders")
    shop_open_message = models.CharField(max_length=200, default="We're open! Order now.", blank=True)
    shop_closed_message = models.CharField(max_length=200, default="We're currently closed. Please try again later.", blank=True)
    is_shop_open = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        from django.core.exceptions import ValidationError
        if self.__class__.objects.count() and not self.pk:
            raise ValidationError("You can only create one instance of Shop Settings.")
        super(ShopSettings, self).save(*args, **kwargs)

    def __str__(self):
        return "Shop Settings"

    class Meta:
        verbose_name = "Shop Settings"
        verbose_name_plural = "Shop Settings"
