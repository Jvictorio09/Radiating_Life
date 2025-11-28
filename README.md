# Radiating Life

A Django web application project.

## Project Structure

```
myProject/
├── myApp/              # Main Django application
│   ├── templates/      # HTML templates
│   ├── migrations/     # Database migrations
│   └── ...
├── myProject/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── static/             # Static files (CSS, images, etc.)
│   └── images/         # Image assets
├── manage.py           # Django management script
├── requirements.txt    # Python dependencies
└── db.sqlite3          # SQLite database
```

## Features

- Django web framework
- Static file management
- Image gallery
- Template-based UI

## Setup

1. Install dependencies:
```bash
pip install -r myProject/requirements.txt
```

2. Run migrations:
```bash
cd myProject
python manage.py migrate
```

3. Start the development server:
```bash
python manage.py runserver
```

## Technologies

- Django 5.1.2
- Python
- SQLite
- HTML/CSS

## License

This project is public and available for viewing.

