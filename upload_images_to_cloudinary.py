"""
Cloudinary Image Uploader Script

This script processes static images, converts high-resolution images to WebP,
uploads them to Cloudinary, and stores the URLs in PostgreSQL.

Usage:
    python upload_images_to_cloudinary.py [--static-dir static/images] [--threshold 1920]
"""

import os
import sys
import logging
from pathlib import Path
from typing import Optional, Tuple
import argparse

# Add project root to path to import Django settings
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myProject.settings')
import django
django.setup()

from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
from PIL import Image
import psycopg

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('image_upload.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Image formats supported for conversion
SUPPORTED_IMAGE_FORMATS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
WEBP_QUALITY = 90  # High quality WebP conversion
HIGH_RES_THRESHOLD = 1920  # Default threshold for high-resolution images


def load_env() -> dict:
    """
    Load environment variables from .env file.
    
    Returns:
        dict: Dictionary containing all required environment variables
    """
    load_dotenv()
    
    env_vars = {
        'cloudinary_cloud_name': os.getenv('CLOUDINARY_CLOUD_NAME'),
        'cloudinary_api_key': os.getenv('CLOUDINARY_API_KEY'),
        'cloudinary_api_secret': os.getenv('CLOUDINARY_API_SECRET'),
        'database_url': os.getenv('DATABASE_URL'),
        'postgres_db': os.getenv('POSTGRES_DB'),
        'postgres_user': os.getenv('POSTGRES_USER'),
        'postgres_password': os.getenv('POSTGRES_PASSWORD'),
        'postgres_host': os.getenv('POSTGRES_HOST', 'localhost'),
        'postgres_port': os.getenv('POSTGRES_PORT', '5432'),
    }
    
    # Validate Cloudinary credentials
    if not all([env_vars['cloudinary_cloud_name'], 
                env_vars['cloudinary_api_key'], 
                env_vars['cloudinary_api_secret']]):
        raise ValueError("Missing Cloudinary credentials in .env file")
    
    # Validate database connection
    if not env_vars['database_url'] and not all([
        env_vars['postgres_db'], 
        env_vars['postgres_user'], 
        env_vars['postgres_password']
    ]):
        raise ValueError("Missing PostgreSQL credentials in .env file")
    
    logger.info("Environment variables loaded successfully")
    return env_vars


def configure_cloudinary(cloud_name: str, api_key: str, api_secret: str):
    """
    Configure Cloudinary with credentials.
    
    Args:
        cloud_name: Cloudinary cloud name
        api_key: Cloudinary API key
        api_secret: Cloudinary API secret
    """
    cloudinary.config(
        cloud_name=cloud_name,
        api_key=api_key,
        api_secret=api_secret
    )
    logger.info(f"Cloudinary configured for cloud: {cloud_name}")


def get_image_dimensions(image_path: Path) -> Tuple[int, int]:
    """
    Get image dimensions.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Tuple of (width, height)
    """
    try:
        with Image.open(image_path) as img:
            return img.size
    except Exception as e:
        logger.error(f"Error reading image dimensions for {image_path}: {e}")
        return (0, 0)


def convert_to_webp(image_path: Path, output_path: Optional[Path] = None) -> Path:
    """
    Convert image to WebP format with high quality preservation.
    
    Args:
        image_path: Path to the original image
        output_path: Optional output path (if None, creates temp file)
        
    Returns:
        Path to the converted WebP image
    """
    if output_path is None:
        output_path = image_path.with_suffix('.webp')
    
    try:
        with Image.open(image_path) as img:
            # Convert RGBA to RGB if necessary (WebP doesn't support RGBA well)
            if img.mode in ('RGBA', 'LA'):
                # Create white background
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'RGBA':
                    rgb_img.paste(img, mask=img.split()[3])  # Use alpha channel as mask
                else:
                    rgb_img.paste(img)
                img = rgb_img
            elif img.mode not in ('RGB', 'L'):
                img = img.convert('RGB')
            
            # Save as WebP with high quality
            img.save(output_path, 'WEBP', quality=WEBP_QUALITY, method=6)
            logger.info(f"Converted {image_path.name} to WebP: {output_path.name}")
            return output_path
    except Exception as e:
        logger.error(f"Error converting {image_path} to WebP: {e}")
        raise


def upload_to_cloudinary(image_path: Path, public_id: Optional[str] = None) -> dict:
    """
    Upload image to Cloudinary.
    
    Args:
        image_path: Path to the image file to upload
        public_id: Optional public ID for the uploaded image
        
    Returns:
        Dictionary containing upload response with URL, public_id, format, etc.
    """
    try:
        upload_options = {
            'resource_type': 'image',
            'quality': 'auto:good',  # Auto quality optimization
            'fetch_format': 'auto',  # Auto format selection
        }
        
        if public_id:
            upload_options['public_id'] = public_id
        
        result = cloudinary.uploader.upload(
            str(image_path),
            **upload_options
        )
        
        logger.info(f"Successfully uploaded {image_path.name} to Cloudinary")
        return result
    except Exception as e:
        logger.error(f"Error uploading {image_path} to Cloudinary: {e}")
        raise


def get_db_connection(env_vars: dict):
    """
    Get PostgreSQL database connection.
    
    Args:
        env_vars: Dictionary containing database credentials
        
    Returns:
        Database connection object
    """
    try:
        # Try DATABASE_URL first (for Railway/Heroku style)
        if env_vars['database_url']:
            conn = psycopg.connect(env_vars['database_url'])
        else:
            # Use individual connection parameters
            conn = psycopg.connect(
                dbname=env_vars['postgres_db'],
                user=env_vars['postgres_user'],
                password=env_vars['postgres_password'],
                host=env_vars['postgres_host'],
                port=env_vars['postgres_port']
            )
        
        logger.info("Database connection established")
        return conn
    except Exception as e:
        logger.error(f"Error connecting to database: {e}")
        raise


def create_media_assets_table(conn):
    """
    Create media_assets table if it doesn't exist.
    
    Args:
        conn: Database connection
    """
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS media_assets (
                    id SERIAL PRIMARY KEY,
                    original_path VARCHAR(500) NOT NULL,
                    file_name VARCHAR(255) NOT NULL,
                    cloudinary_url VARCHAR(1000) NOT NULL,
                    cloudinary_public_id VARCHAR(500),
                    format VARCHAR(10),
                    width INTEGER,
                    height INTEGER,
                    file_size BIGINT,
                    was_converted BOOLEAN DEFAULT FALSE,
                    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # Create indexes
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_media_assets_original_path 
                ON media_assets(original_path);
            """)
            
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_media_assets_cloudinary_public_id 
                ON media_assets(cloudinary_public_id);
            """)
            
            conn.commit()
            logger.info("media_assets table created/verified")
    except Exception as e:
        logger.error(f"Error creating media_assets table: {e}")
        conn.rollback()
        raise


def save_to_postgres(conn, original_path: str, file_name: str, upload_result: dict, 
                    was_converted: bool, file_size: int):
    """
    Save image metadata to PostgreSQL.
    
    Args:
        conn: Database connection
        original_path: Original file path relative to static directory
        file_name: Original file name
        upload_result: Cloudinary upload response dictionary
        was_converted: Whether the image was converted to WebP
        file_size: File size in bytes
    """
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO media_assets 
                (original_path, file_name, cloudinary_url, cloudinary_public_id, 
                 format, width, height, file_size, was_converted)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (
                original_path,
                file_name,
                upload_result.get('secure_url') or upload_result.get('url'),
                upload_result.get('public_id'),
                upload_result.get('format'),
                upload_result.get('width'),
                upload_result.get('height'),
                upload_result.get('bytes') or file_size,
                was_converted
            ))
            conn.commit()
            logger.info(f"Saved metadata for {file_name} to database")
    except Exception as e:
        logger.error(f"Error saving {file_name} to database: {e}")
        conn.rollback()
        raise


def process_image(image_path: Path, static_dir: Path, threshold: int, 
                 conn, env_vars: dict) -> bool:
    """
    Process a single image: convert if needed, upload, and save to database.
    
    Args:
        image_path: Path to the image file
        static_dir: Base static directory path
        threshold: Resolution threshold for conversion
        conn: Database connection
        env_vars: Environment variables dictionary
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Get relative path from static directory
        try:
            relative_path = image_path.relative_to(static_dir)
        except ValueError:
            relative_path = Path(image_path.name)
        
        original_path = str(relative_path).replace('\\', '/')
        file_name = image_path.name
        file_size = image_path.stat().st_size
        
        logger.info(f"Processing: {file_name}")
        
        # Get image dimensions
        width, height = get_image_dimensions(image_path)
        max_dimension = max(width, height)
        
        # Determine if conversion is needed
        needs_conversion = (
            max_dimension > threshold and 
            image_path.suffix.lower() in SUPPORTED_IMAGE_FORMATS
        )
        
        # Convert to WebP if needed
        upload_path = image_path
        was_converted = False
        temp_webp_path = None
        
        if needs_conversion:
            logger.info(f"Converting {file_name} to WebP (resolution: {width}x{height})")
            temp_webp_path = convert_to_webp(image_path)
            upload_path = temp_webp_path
            was_converted = True
        
        # Upload to Cloudinary
        # Use relative path without extension as public_id
        public_id = str(relative_path.with_suffix('')).replace('\\', '/')
        upload_result = upload_to_cloudinary(upload_path, public_id=public_id)
        
        # Save to database
        save_to_postgres(
            conn, 
            original_path, 
            file_name, 
            upload_result, 
            was_converted,
            file_size
        )
        
        # Clean up temporary WebP file if created
        if temp_webp_path and temp_webp_path.exists() and temp_webp_path != image_path:
            temp_webp_path.unlink()
            logger.info(f"Cleaned up temporary file: {temp_webp_path.name}")
        
        logger.info(f"✓ Successfully processed: {file_name}")
        return True
        
    except Exception as e:
        logger.error(f"✗ Failed to process {image_path.name}: {e}")
        return False


def scan_and_process_images(static_dir: Path, threshold: int = HIGH_RES_THRESHOLD):
    """
    Scan static directory and process all images.
    
    Args:
        static_dir: Path to static directory containing images
        threshold: Resolution threshold for WebP conversion
    """
    # Load environment variables
    env_vars = load_env()
    
    # Configure Cloudinary
    configure_cloudinary(
        env_vars['cloudinary_cloud_name'],
        env_vars['cloudinary_api_key'],
        env_vars['cloudinary_api_secret']
    )
    
    # Connect to database
    conn = get_db_connection(env_vars)
    
    try:
        # Create table if needed
        create_media_assets_table(conn)
        
        # Find all image files
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp'}
        image_files = [
            f for f in static_dir.rglob('*')
            if f.suffix.lower() in image_extensions and f.is_file()
        ]
        
        if not image_files:
            logger.warning(f"No image files found in {static_dir}")
            return
        
        logger.info(f"Found {len(image_files)} image(s) to process")
        
        # Process each image
        successful = 0
        failed = 0
        
        for image_path in image_files:
            if process_image(image_path, static_dir, threshold, conn, env_vars):
                successful += 1
            else:
                failed += 1
        
        logger.info(f"\n{'='*60}")
        logger.info(f"Processing complete!")
        logger.info(f"Successful: {successful}")
        logger.info(f"Failed: {failed}")
        logger.info(f"Total: {len(image_files)}")
        logger.info(f"{'='*60}")
        
    finally:
        conn.close()
        logger.info("Database connection closed")


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Upload static images to Cloudinary and store URLs in PostgreSQL'
    )
    parser.add_argument(
        '--static-dir',
        type=str,
        default='static/images',
        help='Path to static images directory (default: static/images)'
    )
    parser.add_argument(
        '--threshold',
        type=int,
        default=HIGH_RES_THRESHOLD,
        help=f'Resolution threshold for WebP conversion (default: {HIGH_RES_THRESHOLD})'
    )
    
    args = parser.parse_args()
    
    # Resolve static directory path
    static_dir = Path(args.static_dir)
    if not static_dir.is_absolute():
        static_dir = BASE_DIR / static_dir
    
    if not static_dir.exists():
        logger.error(f"Static directory not found: {static_dir}")
        sys.exit(1)
    
    logger.info(f"Starting image upload process...")
    logger.info(f"Static directory: {static_dir}")
    logger.info(f"Resolution threshold: {args.threshold}px")
    
    try:
        scan_and_process_images(static_dir, args.threshold)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()

