# Radiating Life

A Django web application project ready for deployment on Railway.

## Project Structure

```
.
├── manage.py           # Django management script
├── requirements.txt    # Python dependencies
├── db.sqlite3          # SQLite database
├── myApp/              # Main Django application
│   ├── templates/      # HTML templates
│   ├── migrations/     # Database migrations
│   └── ...
├── myProject/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── static/             # Static files (CSS, images, etc.)
    └── images/         # Image assets
```

## Features

- Django web framework
- Static file management
- Image gallery
- Template-based UI
- Cloudinary image upload integration
- PostgreSQL database support

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run migrations:
```bash
python manage.py migrate
```

3. Create a `.env` file (see `ENV_SETUP.md` for details):
```bash
# Copy the example and fill in your credentials
cp .env.example .env
# Edit .env with your Cloudinary and PostgreSQL credentials
```

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Start the development server:
```bash
python manage.py runserver
```

## Cloudinary Image Uploader

The project includes a script to upload static images to Cloudinary and store URLs in PostgreSQL.

### Usage:

```bash
# Upload images from default directory (static/images)
python upload_images_to_cloudinary.py

# Specify custom directory
python upload_images_to_cloudinary.py --static-dir static/images

# Custom resolution threshold (default: 1920px)
python upload_images_to_cloudinary.py --threshold 2560
```

### Features:
- Automatically converts high-resolution images (>1920px) to WebP format
- Preserves high quality while optimizing file size
- Uploads to Cloudinary with automatic optimization
- Stores metadata (URLs, dimensions, format) in PostgreSQL
- Comprehensive logging to `image_upload.log`

See `ENV_SETUP.md` for environment variable configuration.

## Railway Deployment

This project is structured for easy deployment on Railway. The Django project files are at the root level for Railway to automatically detect and deploy.

### Railway Setup:
- Railway will automatically detect the Django project
- Set the start command: `python manage.py runserver` or use gunicorn: `gunicorn myProject.wsgi:application`
- Add environment variables as needed in Railway dashboard

## Technologies

- Django 5.1.2
- Python
- SQLite
- HTML/CSS

## License

This project is public and available for viewing.
