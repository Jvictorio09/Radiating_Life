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

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run migrations:
```bash
python manage.py migrate
```

3. Start the development server:
```bash
python manage.py runserver
```

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
