# How to Import Images from Local Files in Django

## Step 1: Directory Structure

Your project now has the following structure:
```
myProject/
├── static/
│   ├── images/          ← Place your image files here
│   ├── css/
│   └── js/
```

## Step 2: Place Your Images

1. Copy your image files (jpg, png, gif, etc.) into the `myProject/static/images/` folder
2. Example: If you have `yoga-pose.jpg`, place it at `myProject/static/images/yoga-pose.jpg`

## Step 3: Use Images in Templates

### In your template file (home.html), make sure you have:

```django
{% load static %}
```

This should be at the top of your template file, after `{% extends %}`.

### Example 1: Using `<img>` tag

**Before (using URL):**
```html
<img src="https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=800" alt="Yoga Pose">
```

**After (using local file):**
```html
<img src="{% static 'images/yoga-pose.jpg' %}" alt="Yoga Pose">
```

### Example 2: Using background-image in CSS

**Before (using URL):**
```css
background: url('https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=1920') center/cover;
```

**After (using local file):**
```css
background: url('{% static "images/hero-background.jpg" %}') center/cover;
```

### Example 3: Inline style attribute

```html
<div style="background-image: url('{% static 'images/background.jpg' %}');">
    Content here
</div>
```

## Step 4: Update Your Template

Here's how to update the yoga pose image in home.html:

**Find this line:**
```css
background: url('https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=800') center/cover;
```

**Replace with:**
```css
background: url('{% static "images/yoga-pose.jpg" %}') center/cover;
```

## Step 5: Collect Static Files (for production)

When you're ready to deploy, run:
```bash
python manage.py collectstatic
```

This collects all static files into the `staticfiles` directory.

## Quick Reference

- **Template tag**: `{% static 'images/filename.jpg' %}`
- **Directory**: `myProject/static/images/`
- **File path in template**: `images/filename.jpg` (relative to static folder)

## Example: Complete Image Usage

```django
{% load static %}
{% extends 'myApp/base.html' %}

{% block content %}
    <!-- Using img tag -->
    <img src="{% static 'images/coach-photo.jpg' %}" alt="Coach" class="rounded-lg">
    
    <!-- Using background in CSS -->
    <div class="hero-section" style="background-image: url('{% static 'images/hero-bg.jpg' %}');">
        <h1>Welcome</h1>
    </div>
    
    <!-- In style block -->
    <style>
        .section-bg {
            background: url('{% static "images/section-bg.jpg" %}') center/cover;
        }
    </style>
{% endblock %}
```

## Troubleshooting

1. **Image not showing?**
   - Make sure the file is in `myProject/static/images/`
   - Check the filename matches exactly (case-sensitive)
   - Make sure you have `{% load static %}` at the top

2. **Still using old images?**
   - Clear your browser cache
   - Restart your Django development server

3. **Path not found?**
   - Verify `STATICFILES_DIRS` in `settings.py` includes `BASE_DIR / 'static'`
   - Check that `django.contrib.staticfiles` is in `INSTALLED_APPS`




