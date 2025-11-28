from django.db import models


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
