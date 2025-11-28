# Dashboard System Setup Guide

This guide explains how to set up and use the WordPress-like CMS dashboard system.

## Quick Start

1. **Install dependencies** (already in requirements.txt):
   ```bash
   pip install -r requirements.txt
   ```

2. **Create migrations and migrate**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```

4. **Configure environment variables** (create `.env` file):
   ```env
   CLOUDINARY_CLOUD_NAME=your_cloud_name
   CLOUDINARY_API_KEY=your_api_key
   CLOUDINARY_API_SECRET=your_api_secret
   ```

5. **Run server and access dashboard**:
   ```bash
   python manage.py runserver
   # Navigate to http://localhost:8000/dashboard/
   ```

## Features Implemented

✅ **All Models Created**: SEO, Navigation, Hero, About, Stats, Services, Portfolio, Testimonials, FAQs, Contact, Footer, Social Links
✅ **Cloudinary Integration**: Smart compression, WebP conversion, automatic optimization
✅ **Image Picker Modal**: Reusable component with gallery and upload tabs
✅ **Dashboard Views**: Complete CRUD operations for all sections
✅ **Authentication**: Login/logout system
✅ **Export/Import**: Bulk data export and import commands
✅ **Content Helpers**: Database to JSON conversion for templates

## Remaining Templates to Create

The following templates need to be created following the pattern shown in `seo_edit.html` and `hero_edit.html`:

- `about_edit.html`
- `stats_list.html` / `stat_edit.html`
- `services_section_edit.html` / `services_list.html` / `service_edit.html`
- `portfolio_edit.html` / `portfolio_projects_list.html` / `portfolio_project_edit.html`
- `testimonials_list.html` / `testimonial_edit.html`
- `faq_section_edit.html` / `faqs_list.html` / `faq_edit.html`
- `contact_edit.html` / `contact_info_list.html` / `contact_info_edit.html`
- `contact_form_fields_list.html` / `contact_form_field_edit.html`
- `social_links_list.html` / `social_link_edit.html`
- `footer_edit.html`

## Template Pattern

All edit templates should follow this pattern:

```html
{% extends "dashboard/base.html" %}
{% include "dashboard/image_picker_modal.html" %}

{% block title %}Section Name{% endblock %}

{% block content %}
<div class="max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold text-navy-900 mb-6">Section Name</h1>
    
    <form method="post" class="bg-white p-6 rounded-lg shadow">
        {% csrf_token %}
        
        <!-- Form fields with image picker buttons -->
        <div class="mb-6">
            <label class="block text-sm font-semibold text-gray-700 mb-2">Image URL</label>
            <input type="url" name="image_url" id="field_image_url" value="{{ object.image_url|default:'' }}" 
                   class="w-full px-4 py-3 border border-gray-300 rounded-xl">
            <p class="text-sm text-gray-500 mt-2">
                <button type="button" onclick="openImagePickerModal('field_image_url')" 
                        class="text-navy-900 hover:underline">
                    <i class="fa-solid fa-images mr-1"></i> Choose from gallery
                </button>
            </p>
        </div>
        
        <button type="submit" class="w-full bg-navy-900 text-white py-3 rounded-lg hover:bg-navy-800 font-semibold">
            <i class="fa-solid fa-save mr-2"></i> Save Changes
        </button>
    </form>
</div>
{% endblock %}
```

## Using the Image Picker

Every image URL field should include:
1. The image picker modal include: `{% include "dashboard/image_picker_modal.html" %}`
2. A button to open the modal: `onclick="openImagePickerModal('field_id')"`

## Export/Import Data

**Export all data:**
```bash
python manage.py export_all_data --output backup.json
```

**Import data:**
```bash
python manage.py import_homepage_data backup.json
```

## Using Content in Templates

Update your homepage view to use database content:

```python
from myApp.content_helpers import get_homepage_content_from_db

def home(request):
    content = get_homepage_content_from_db()
    return render(request, 'home.html', {'content': content})
```

Then in your template, access content like:
```html
{{ content.hero.title }}
{{ content.hero.image_url }}
{{ content.services }}
```

## Next Steps

1. Create remaining templates following the pattern
2. Test all CRUD operations
3. Customize colors/branding in `base.html`
4. Deploy to production

