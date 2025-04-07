from django.db import models
from django.core.validators import MinValueValidator
from django.utils.text import slugify


class Product(models.Model):
    product_id = models.IntegerField(max_length=100, unique=True, primary_key=True)
    product_name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    reviews = models.PositiveIntegerField(default=0)  # NumReviews from CSV
    quantity = models.PositiveIntegerField(default=0)  # StockQuantity from CSV
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    sales = models.PositiveIntegerField(default=0)
    date_added = models.DateField()  # or DateTimeField if your CSV includes time
    # Optional: Add a slug field for SEO-friendly URLs
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    # Optional: Add image field if your products have images
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    class Meta:
        ordering = ['-date_added']  # Default ordering by newest first

    def __str__(self):
        return self.product_name

    # Optional: Add save method to automatically create slug
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f"{slugify(self.product_name)}-{self.product_id}"
        super().save(*args, **kwargs)
