from django.db import models
from django.utils.text import slugify
import json


class MediaAsset(models.Model):
    """Model to store Cloudinary media asset information."""
    original_path = models.CharField(max_length=500, help_text="Original file path relative to static directory")
    file_name = models.CharField(max_length=255, help_text="Original file name")
    cloudinary_url = models.URLField(max_length=1000, help_text="Full Cloudinary URL")
    cloudinary_public_id = models.CharField(max_length=500, blank=True, null=True, help_text="Cloudinary public ID")
    format = models.CharField(max_length=10, blank=True, null=True, help_text="Image format (webp, jpg, png, etc.)")
    width = models.IntegerField(blank=True, null=True, help_text="Image width in pixels")
    height = models.IntegerField(blank=True, null=True, help_text="Image height in pixels")
    file_size = models.BigIntegerField(blank=True, null=True, help_text="File size in bytes")
    was_converted = models.BooleanField(default=False, help_text="Whether the image was converted to WebP")
    uploaded_at = models.DateTimeField(auto_now_add=True, help_text="When the image was uploaded")
    
    class Meta:
        db_table = 'media_assets'
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['original_path']),
            models.Index(fields=['cloudinary_public_id']),
        ]
    
    def __str__(self):
        return f"{self.file_name} - {self.cloudinary_url[:50]}..."


class SEO(models.Model):
    """SEO metadata for the homepage."""
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    keywords = models.CharField(max_length=500, blank=True)
    og_image = models.URLField(blank=True)
    og_title = models.CharField(max_length=200, blank=True)
    og_description = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "SEO"
        verbose_name_plural = "SEO"
    
    def __str__(self):
        return self.title or "SEO Settings"


class Navigation(models.Model):
    """Navigation menu items."""
    label = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    sort_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['sort_order']
        verbose_name_plural = "Navigation Items"
    
    def __str__(self):
        return self.label


class Hero(models.Model):
    """Hero section content."""
    title = models.CharField(max_length=200, blank=True)
    subtitle = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    button_text = models.CharField(max_length=100, blank=True)
    button_url = models.CharField(max_length=200, blank=True)
    content = models.JSONField(default=dict, blank=True)  # Flexible content storage
    
    class Meta:
        verbose_name_plural = "Hero"
    
    def __str__(self):
        return self.title or "Hero Section"


class About(models.Model):
    """About section content."""
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    content = models.JSONField(default=dict, blank=True)
    
    class Meta:
        verbose_name_plural = "About"
    
    def __str__(self):
        return self.title or "About Section"


class Stat(models.Model):
    """Statistics/numbers section."""
    number = models.CharField(max_length=50)
    label = models.CharField(max_length=100)
    icon = models.CharField(max_length=100, blank=True)
    sort_order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['sort_order']
        verbose_name = "Statistic"
        verbose_name_plural = "Statistics"
    
    def __str__(self):
        return f"{self.number} - {self.label}"


class Service(models.Model):
    """Service items."""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    icon = models.CharField(max_length=100, blank=True)
    sort_order = models.IntegerField(default=0)
    content = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['sort_order']
    
    def __str__(self):
        return self.title


class ServicesSection(models.Model):
    """Services section header/content."""
    title = models.CharField(max_length=200, blank=True)
    subtitle = models.TextField(blank=True)
    content = models.JSONField(default=dict, blank=True)
    
    class Meta:
        verbose_name = "Services Section"
        verbose_name_plural = "Services Section"
    
    def __str__(self):
        return self.title or "Services Section"


class Portfolio(models.Model):
    """Portfolio section header."""
    title = models.CharField(max_length=200, blank=True)
    subtitle = models.TextField(blank=True)
    content = models.JSONField(default=dict, blank=True)
    
    class Meta:
        verbose_name_plural = "Portfolio"
    
    def __str__(self):
        return self.title or "Portfolio Section"


class PortfolioProject(models.Model):
    """Individual portfolio project."""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    gallery = models.JSONField(default=list, blank=True)  # Array of image URLs
    category = models.CharField(max_length=100, blank=True)
    sort_order = models.IntegerField(default=0)
    content = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['sort_order']
        verbose_name = "Portfolio Project"
        verbose_name_plural = "Portfolio Projects"
    
    def __str__(self):
        return self.title


class Testimonial(models.Model):
    """Customer testimonials."""
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200, blank=True)
    company = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    image_url = models.URLField(blank=True)
    rating = models.IntegerField(default=5, blank=True, null=True)
    sort_order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['sort_order']
    
    def __str__(self):
        return f"{self.name} - {self.company or self.role}"


class FAQ(models.Model):
    """Frequently asked questions."""
    question = models.CharField(max_length=500)
    answer = models.TextField()
    category = models.CharField(max_length=100, blank=True)
    sort_order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['sort_order']
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
    
    def __str__(self):
        return self.question


class FAQSection(models.Model):
    """FAQ section header."""
    title = models.CharField(max_length=200, blank=True)
    subtitle = models.TextField(blank=True)
    content = models.JSONField(default=dict, blank=True)
    
    class Meta:
        verbose_name = "FAQ Section"
        verbose_name_plural = "FAQ Section"
    
    def __str__(self):
        return self.title or "FAQ Section"


class Contact(models.Model):
    """Contact section."""
    title = models.CharField(max_length=200, blank=True)
    subtitle = models.TextField(blank=True)
    content = models.JSONField(default=dict, blank=True)
    
    class Meta:
        verbose_name_plural = "Contact"
    
    def __str__(self):
        return self.title or "Contact Section"


class ContactInfo(models.Model):
    """Contact information items."""
    type = models.CharField(max_length=50)  # email, phone, address, etc.
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=500)
    icon = models.CharField(max_length=100, blank=True)
    sort_order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['sort_order']
        verbose_name = "Contact Info"
        verbose_name_plural = "Contact Info"
    
    def __str__(self):
        return f"{self.label}: {self.value}"


class ContactFormField(models.Model):
    """Contact form field definitions."""
    name = models.CharField(max_length=100)
    label = models.CharField(max_length=200)
    field_type = models.CharField(max_length=50)  # text, email, textarea, etc.
    required = models.BooleanField(default=False)
    placeholder = models.CharField(max_length=200, blank=True)
    sort_order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['sort_order']
        verbose_name = "Contact Form Field"
        verbose_name_plural = "Contact Form Fields"
    
    def __str__(self):
        return f"{self.label} ({self.field_type})"


class SocialLink(models.Model):
    """Social media links."""
    platform = models.CharField(max_length=100)  # facebook, twitter, instagram, etc.
    url = models.URLField()
    icon = models.CharField(max_length=100, blank=True)
    sort_order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['sort_order']
        verbose_name = "Social Link"
        verbose_name_plural = "Social Links"
    
    def __str__(self):
        return self.platform


class Footer(models.Model):
    """Footer content."""
    copyright_text = models.CharField(max_length=500, blank=True)
    content = models.JSONField(default=dict, blank=True)
    
    class Meta:
        verbose_name_plural = "Footer"
    
    def __str__(self):
        return "Footer"
