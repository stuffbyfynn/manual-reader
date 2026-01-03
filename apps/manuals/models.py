from django.db import models
from django.utils.text import slugify

class Brand(models.Model):
    name = models.CharField('Marke', max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    logo = models.ImageField('Logo', upload_to='brands/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class VehicleModel(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='models')
    name = models.CharField('Modell', max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        unique_together = ('brand', 'name')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.brand.name}-{self.name}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brand.name} {self.name}"

class Manual(models.Model):
    vehicle_model = models.ForeignKey(VehicleModel, on_delete=models.CASCADE, related_name='manuals')
    year = models.IntegerField('Baujahr')
    title = models.CharField('Titel', max_length=255)
    file = models.FileField('PDF Datei', upload_to='manuals/')
    version = models.CharField('Version', max_length=20, default='1.0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.vehicle_model} ({self.year}) - {self.title}"
