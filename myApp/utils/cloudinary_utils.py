"""
Cloudinary utility functions for image upload and optimization.
"""

import os
import io
from PIL import Image
import cloudinary
import cloudinary.uploader
from django.conf import settings

# Compression settings
MAX_BYTES = 10 * 1024 * 1024  # 10MB
TARGET_BYTES = int(MAX_BYTES * 0.93)  # 9.3MB (slightly under limit)


def smart_compress_to_bytes(image_file, max_bytes=MAX_BYTES, target_bytes=TARGET_BYTES, quality=85):
    """
    Intelligently compress an image to fit within size limits while preserving quality.
    
    Args:
        image_file: File-like object or path to image
        max_bytes: Maximum allowed size in bytes
        target_bytes: Target size to compress to
        quality: Starting quality (85-95 recommended)
    
    Returns:
        BytesIO object containing compressed image
    """
    # Open image
    if isinstance(image_file, str):
        img = Image.open(image_file)
    else:
        img = Image.open(image_file)
        image_file.seek(0)  # Reset file pointer
    
    # Convert RGBA to RGB if necessary (JPEG doesn't support transparency)
    if img.mode in ('RGBA', 'LA', 'P'):
        # Create white background
        rgb_img = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'P':
            img = img.convert('RGBA')
        if img.mode in ('RGBA', 'LA'):
            if img.mode == 'LA':
                # Convert LA to RGBA first
                rgba_img = Image.new('RGBA', img.size)
                rgba_img.paste(img, mask=img.split()[1] if len(img.split()) > 1 else None)
                img = rgba_img
            rgb_img.paste(img, mask=img.split()[3] if len(img.split()) > 3 else None)
        img = rgb_img
    elif img.mode not in ('RGB', 'L'):
        img = img.convert('RGB')
    
    # Get initial size
    output = io.BytesIO()
    img.save(output, format='JPEG', quality=quality, optimize=True)
    current_size = output.tell()
    
    # If already under target, return
    if current_size <= target_bytes:
        output.seek(0)
        return output
    
    # Binary search for optimal quality
    min_quality = 30
    max_quality = quality
    best_output = output
    
    while min_quality <= max_quality:
        mid_quality = (min_quality + max_quality) // 2
        output = io.BytesIO()
        
        try:
            img.save(output, format='JPEG', quality=mid_quality, optimize=True)
            size = output.tell()
            
            if size <= target_bytes:
                best_output = output
                min_quality = mid_quality + 1
            else:
                max_quality = mid_quality - 1
        except Exception:
            max_quality = mid_quality - 1
    
    # If still too large, resize image
    best_output.seek(0)
    if best_output.tell() > max_bytes:
        # Calculate resize factor
        factor = (max_bytes / best_output.tell()) ** 0.5
        new_size = (int(img.size[0] * factor), int(img.size[1] * factor))
        img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # Recompress at good quality
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=85, optimize=True)
        best_output = output
    
    best_output.seek(0)
    return best_output


def upload_to_cloudinary(image_file, folder='uploads', public_id=None, 
                         compress=True, convert_to_webp=True):
    """
    Upload image to Cloudinary with smart compression and optimization.
    
    Args:
        image_file: File-like object, path, or bytes
        folder: Cloudinary folder path
        public_id: Optional public ID for the image
        compress: Whether to compress before upload
        convert_to_webp: Whether to convert to WebP format
    
    Returns:
        Dictionary with upload result including URLs
    """
    try:
        # Prepare file for upload
        if isinstance(image_file, bytes):
            file_obj = io.BytesIO(image_file)
        elif isinstance(image_file, str):
            # It's a file path
            with open(image_file, 'rb') as f:
                file_obj = io.BytesIO(f.read())
        else:
            # It's a file-like object
            file_obj = image_file
            if hasattr(file_obj, 'seek'):
                file_obj.seek(0)
        
        # Compress if needed
        if compress:
            file_obj = smart_compress_to_bytes(file_obj)
        
        # Upload options
        upload_options = {
            'resource_type': 'image',
            'folder': folder,
        }
        
        if convert_to_webp:
            upload_options['format'] = 'webp'
            upload_options['quality'] = 'auto:good'
        
        if public_id:
            upload_options['public_id'] = public_id
        
        # Upload to Cloudinary
        result = cloudinary.uploader.upload(
            file_obj,
            **upload_options
        )
        
        # Generate URL variants
        secure_url = result.get('secure_url', result.get('url', ''))
        
        # Web-optimized URL (if not already WebP)
        if convert_to_webp and 'webp' not in secure_url.lower():
            web_url = secure_url.replace('/upload/', '/upload/f_webp,q_80,w_1920/')
        else:
            web_url = secure_url.replace('/upload/', '/upload/q_80,w_1920/')
        
        # Thumbnail URL
        thumb_url = secure_url.replace('/upload/', '/upload/c_thumb,w_300,h_300,q_80/')
        
        # Add custom URL variants to result
        result['web_url'] = web_url
        result['thumb_url'] = thumb_url
        
        return result
        
    except Exception as e:
        raise Exception(f"Error uploading to Cloudinary: {str(e)}")


def get_cloudinary_urls(public_id, folder=None):
    """
    Generate multiple URL variants for a Cloudinary image.
    
    Args:
        public_id: Cloudinary public ID
        folder: Optional folder path
    
    Returns:
        Dictionary with different URL variants
    """
    if folder:
        full_public_id = f"{folder}/{public_id}"
    else:
        full_public_id = public_id
    
    base_url = cloudinary.utils.cloudinary_url(full_public_id)[0]
    
    return {
        'original': base_url,
        'web_optimized': base_url.replace('/upload/', '/upload/f_webp,q_80,w_1920/'),
        'thumbnail': base_url.replace('/upload/', '/upload/c_thumb,w_300,h_300,q_80/'),
        'secure': base_url.replace('http://', 'https://') if 'http://' in base_url else base_url,
    }

