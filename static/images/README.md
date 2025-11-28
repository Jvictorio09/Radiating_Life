# Images Directory

Place your local image files here.

## How to Use Local Images in Templates

1. **Place your image file** in this directory (e.g., `yoga-pose.jpg`)

2. **In your template**, make sure you have `{% load static %}` at the top:
   ```django
   {% load static %}
   ```

3. **Reference the image** using the static tag:
   ```django
   <img src="{% static 'images/yoga-pose.jpg' %}" alt="Yoga Pose">
   ```

   Or in CSS:
   ```django
   background: url('{% static "images/yoga-pose.jpg" %}') center/cover;
   ```

## Example Usage

### In HTML:
```html
{% load static %}
<img src="{% static 'images/hero-image.jpg' %}" alt="Hero Image" class="w-full">
```

### In CSS (inline style):
```html
<div style="background-image: url('{% static 'images/background.jpg' %}');">
```

### In CSS (style block):
```django
{% block extra_head %}
<style>
    .hero-section {
        background: url('{% static "images/hero-bg.jpg" %}') center/cover;
    }
</style>
{% endblock %}
```

## File Structure
```
myProject/
├── static/
│   ├── images/          ← Place your images here
│   ├── css/             ← Place your CSS files here
│   └── js/              ← Place your JavaScript files here
```

## Required Images

### About Page
- **`about-portrait.jpg`** - Portrait image of Myroslava Grygorachyk for the About page
  - This image should be placed in `static/images/about-portrait.jpg`
  - Used in: `myApp/templates/myApp/about.html`


