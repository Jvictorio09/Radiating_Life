"""
Dashboard views for content management.
"""

import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from .models import (
    MediaAsset, SEO, Navigation, Hero, About, Stat, Service, ServicesSection,
    Portfolio, PortfolioProject, Testimonial, FAQ, FAQSection,
    Contact, ContactInfo, ContactFormField, SocialLink, Footer
)
from .utils.cloudinary_utils import upload_to_cloudinary


# Authentication Views
def dashboard_login(request):
    """Dashboard login view."""
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard:index')
        else:
            return render(request, 'dashboard/login.html', {
                'error': 'Invalid username or password'
            })
    
    return render(request, 'dashboard/login.html')


@login_required
def dashboard_logout(request):
    """Dashboard logout view."""
    logout(request)
    return redirect('dashboard:login')


@login_required
def dashboard_home(request):
    """Main dashboard page."""
    return render(request, 'dashboard/index.html')


# Image Upload and Gallery
@login_required
@require_http_methods(["POST"])
def upload_image(request):
    """Upload image to Cloudinary."""
    try:
        if 'image' not in request.FILES:
            return JsonResponse({'error': 'No image file provided'}, status=400)
        
        image_file = request.FILES['image']
        folder = request.POST.get('folder', 'uploads')
        
        # Upload to Cloudinary
        result = upload_to_cloudinary(
            image_file,
            folder=folder,
            compress=True,
            convert_to_webp=True
        )
        
        # Save to database
        media_asset = MediaAsset.objects.create(
            original_path=request.POST.get('original_path', ''),
            file_name=image_file.name,
            cloudinary_url=result.get('secure_url', result.get('url', '')),
            cloudinary_public_id=result.get('public_id', ''),
            format=result.get('format', ''),
            width=result.get('width'),
            height=result.get('height'),
            file_size=result.get('bytes'),
            was_converted=True
        )
        
        return JsonResponse({
            'success': True,
            'url': result.get('secure_url', result.get('url', '')),
            'web_url': result.get('web_url', ''),
            'thumb_url': result.get('thumb_url', ''),
            'public_id': result.get('public_id', ''),
            'width': result.get('width'),
            'height': result.get('height'),
            'format': result.get('format', ''),
            'id': media_asset.id,
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def gallery(request):
    """Image gallery view."""
    images = MediaAsset.objects.all()
    search_query = request.GET.get('search', '')
    
    if search_query:
        images = images.filter(file_name__icontains=search_query)
    
    # Support JSON format for AJAX requests
    if request.GET.get('format') == 'json':
        from .utils.cloudinary_utils import get_cloudinary_urls
        image_list = []
        for img in images:
            urls = get_cloudinary_urls(img.cloudinary_public_id or '') if img.cloudinary_public_id else {}
            image_list.append({
                'id': img.id,
                'file_name': img.file_name,
                'cloudinary_url': img.cloudinary_url,
                'web_url': urls.get('web_optimized', img.cloudinary_url),
                'thumb_url': urls.get('thumbnail', img.cloudinary_url),
                'width': img.width,
                'height': img.height,
                'format': img.format,
            })
        return JsonResponse({'images': image_list})
    
    return render(request, 'dashboard/gallery.html', {
        'images': images,
        'search_query': search_query,
    })


# SEO Views
@login_required
def seo_edit(request):
    """Edit SEO settings."""
    seo, created = SEO.objects.get_or_create(pk=1)
    
    if request.method == 'POST':
        seo.title = request.POST.get('title', '')
        seo.description = request.POST.get('description', '')
        seo.keywords = request.POST.get('keywords', '')
        seo.og_image = request.POST.get('og_image', '')
        seo.og_title = request.POST.get('og_title', '')
        seo.og_description = request.POST.get('og_description', '')
        seo.save()
        return redirect('dashboard:seo_edit')
    
    return render(request, 'dashboard/seo_edit.html', {'seo': seo})


# Navigation Views
@login_required
def navigation_edit(request):
    """Edit navigation items."""
    items = Navigation.objects.all()
    
    if request.method == 'POST':
        # Handle delete
        if 'delete_id' in request.POST:
            Navigation.objects.filter(id=request.POST['delete_id']).delete()
            return redirect('dashboard:navigation_edit')
        
        # Handle add/edit
        item_id = request.POST.get('item_id')
        if item_id:
            item = get_object_or_404(Navigation, id=item_id)
        else:
            item = Navigation()
        
        item.label = request.POST.get('label', '')
        item.url = request.POST.get('url', '')
        item.sort_order = int(request.POST.get('sort_order', 0))
        item.is_active = request.POST.get('is_active') == 'on'
        item.save()
        return redirect('dashboard:navigation_edit')
    
    return render(request, 'dashboard/navigation_edit.html', {'items': items})


# Hero Views
@login_required
def hero_edit(request):
    """Edit hero section."""
    hero, created = Hero.objects.get_or_create(pk=1)
    
    if request.method == 'POST':
        hero.title = request.POST.get('title', '')
        hero.subtitle = request.POST.get('subtitle', '')
        hero.image_url = request.POST.get('image_url', '')
        hero.button_text = request.POST.get('button_text', '')
        hero.button_url = request.POST.get('button_url', '')
        
        # Handle JSON content
        content = {}
        for key, value in request.POST.items():
            if key.startswith('content_'):
                content[key.replace('content_', '')] = value
        hero.content = content
        hero.save()
        return redirect('dashboard:hero_edit')
    
    return render(request, 'dashboard/hero_edit.html', {'hero': hero})


# About Views
@login_required
def about_edit(request):
    """Edit about section."""
    about, created = About.objects.get_or_create(pk=1)
    
    if request.method == 'POST':
        about.title = request.POST.get('title', '')
        about.description = request.POST.get('description', '')
        about.image_url = request.POST.get('image_url', '')
        
        content = {}
        for key, value in request.POST.items():
            if key.startswith('content_'):
                content[key.replace('content_', '')] = value
        about.content = content
        about.save()
        return redirect('dashboard:about_edit')
    
    return render(request, 'dashboard/about_edit.html', {'about': about})


# Stats Views
@login_required
def stats_list(request):
    """List all statistics."""
    stats = Stat.objects.all()
    
    if request.method == 'POST':
        if 'delete_id' in request.POST:
            Stat.objects.filter(id=request.POST['delete_id']).delete()
            return redirect('dashboard:stats_list')
        
        stat_id = request.POST.get('stat_id')
        if stat_id:
            stat = get_object_or_404(Stat, id=stat_id)
        else:
            stat = Stat()
        
        stat.number = request.POST.get('number', '')
        stat.label = request.POST.get('label', '')
        stat.icon = request.POST.get('icon', '')
        stat.sort_order = int(request.POST.get('sort_order', 0))
        stat.save()
        return redirect('dashboard:stats_list')
    
    return render(request, 'dashboard/stats_list.html', {'stats': stats})


@login_required
def stat_edit(request, stat_id=None):
    """Edit a single statistic."""
    if stat_id:
        stat = get_object_or_404(Stat, id=stat_id)
    else:
        stat = None
    
    if request.method == 'POST':
        if not stat:
            stat = Stat()
        stat.number = request.POST.get('number', '')
        stat.label = request.POST.get('label', '')
        stat.icon = request.POST.get('icon', '')
        stat.sort_order = int(request.POST.get('sort_order', 0))
        stat.save()
        return redirect('dashboard:stats_list')
    
    return render(request, 'dashboard/stat_edit.html', {'stat': stat})


# Services Views
@login_required
def services_section_edit(request):
    """Edit services section header."""
    section, created = ServicesSection.objects.get_or_create(pk=1)
    
    if request.method == 'POST':
        section.title = request.POST.get('title', '')
        section.subtitle = request.POST.get('subtitle', '')
        
        content = {}
        for key, value in request.POST.items():
            if key.startswith('content_'):
                content[key.replace('content_', '')] = value
        section.content = content
        section.save()
        return redirect('dashboard:services_section_edit')
    
    return render(request, 'dashboard/services_section_edit.html', {'section': section})


@login_required
def services_list(request):
    """List all services."""
    services = Service.objects.all()
    
    if request.method == 'POST':
        if 'delete_id' in request.POST:
            Service.objects.filter(id=request.POST['delete_id']).delete()
            return redirect('dashboard:services_list')
        
        service_id = request.POST.get('service_id')
        if service_id:
            service = get_object_or_404(Service, id=service_id)
        else:
            service = Service()
        
        service.title = request.POST.get('title', '')
        service.description = request.POST.get('description', '')
        service.image_url = request.POST.get('image_url', '')
        service.icon = request.POST.get('icon', '')
        service.sort_order = int(request.POST.get('sort_order', 0))
        
        content = {}
        for key, value in request.POST.items():
            if key.startswith('content_'):
                content[key.replace('content_', '')] = value
        service.content = content
        service.save()
        return redirect('dashboard:services_list')
    
    return render(request, 'dashboard/services_list.html', {'services': services})


@login_required
def service_edit(request, service_id=None):
    """Edit a single service."""
    if service_id:
        service = get_object_or_404(Service, id=service_id)
    else:
        service = None
    
    if request.method == 'POST':
        if not service:
            service = Service()
        service.title = request.POST.get('title', '')
        service.description = request.POST.get('description', '')
        service.image_url = request.POST.get('image_url', '')
        service.icon = request.POST.get('icon', '')
        service.sort_order = int(request.POST.get('sort_order', 0))
        
        content = {}
        for key, value in request.POST.items():
            if key.startswith('content_'):
                content[key.replace('content_', '')] = value
        service.content = content
        service.save()
        return redirect('dashboard:services_list')
    
    return render(request, 'dashboard/service_edit.html', {'service': service})


# Portfolio Views
@login_required
def portfolio_edit(request):
    """Edit portfolio section header."""
    portfolio, created = Portfolio.objects.get_or_create(pk=1)
    
    if request.method == 'POST':
        portfolio.title = request.POST.get('title', '')
        portfolio.subtitle = request.POST.get('subtitle', '')
        
        content = {}
        for key, value in request.POST.items():
            if key.startswith('content_'):
                content[key.replace('content_', '')] = value
        portfolio.content = content
        portfolio.save()
        return redirect('dashboard:portfolio_edit')
    
    return render(request, 'dashboard/portfolio_edit.html', {'portfolio': portfolio})


@login_required
def portfolio_projects_list(request):
    """List all portfolio projects."""
    projects = PortfolioProject.objects.all()
    
    if request.method == 'POST':
        if 'delete_id' in request.POST:
            PortfolioProject.objects.filter(id=request.POST['delete_id']).delete()
            return redirect('dashboard:portfolio_projects_list')
        
        project_id = request.POST.get('project_id')
        if project_id:
            project = get_object_or_404(PortfolioProject, id=project_id)
        else:
            project = PortfolioProject()
        
        project.title = request.POST.get('title', '')
        project.description = request.POST.get('description', '')
        project.image_url = request.POST.get('image_url', '')
        project.category = request.POST.get('category', '')
        project.sort_order = int(request.POST.get('sort_order', 0))
        
        # Handle gallery JSON array
        gallery_str = request.POST.get('gallery', '[]')
        try:
            project.gallery = json.loads(gallery_str) if isinstance(gallery_str, str) else gallery_str
        except:
            project.gallery = []
        
        content = {}
        for key, value in request.POST.items():
            if key.startswith('content_'):
                content[key.replace('content_', '')] = value
        project.content = content
        project.save()
        return redirect('dashboard:portfolio_projects_list')
    
    return render(request, 'dashboard/portfolio_projects_list.html', {'projects': projects})


@login_required
def portfolio_project_edit(request, project_id=None):
    """Edit a single portfolio project."""
    if project_id:
        project = get_object_or_404(PortfolioProject, id=project_id)
    else:
        project = None
    
    if request.method == 'POST':
        if not project:
            project = PortfolioProject()
        project.title = request.POST.get('title', '')
        project.description = request.POST.get('description', '')
        project.image_url = request.POST.get('image_url', '')
        project.category = request.POST.get('category', '')
        project.sort_order = int(request.POST.get('sort_order', 0))
        
        gallery_str = request.POST.get('gallery', '[]')
        try:
            project.gallery = json.loads(gallery_str) if isinstance(gallery_str, str) else gallery_str
        except:
            project.gallery = []
        
        content = {}
        for key, value in request.POST.items():
            if key.startswith('content_'):
                content[key.replace('content_', '')] = value
        project.content = content
        project.save()
        return redirect('dashboard:portfolio_projects_list')
    
    return render(request, 'dashboard/portfolio_project_edit.html', {'project': project})


# Testimonials Views
@login_required
def testimonials_list(request):
    """List all testimonials."""
    testimonials = Testimonial.objects.all()
    
    if request.method == 'POST':
        if 'delete_id' in request.POST:
            Testimonial.objects.filter(id=request.POST['delete_id']).delete()
            return redirect('dashboard:testimonials_list')
        
        testimonial_id = request.POST.get('testimonial_id')
        if testimonial_id:
            testimonial = get_object_or_404(Testimonial, id=testimonial_id)
        else:
            testimonial = Testimonial()
        
        testimonial.name = request.POST.get('name', '')
        testimonial.role = request.POST.get('role', '')
        testimonial.company = request.POST.get('company', '')
        testimonial.content = request.POST.get('content', '')
        testimonial.image_url = request.POST.get('image_url', '')
        testimonial.rating = int(request.POST.get('rating', 5))
        testimonial.sort_order = int(request.POST.get('sort_order', 0))
        testimonial.save()
        return redirect('dashboard:testimonials_list')
    
    return render(request, 'dashboard/testimonials_list.html', {'testimonials': testimonials})


@login_required
def testimonial_edit(request, testimonial_id=None):
    """Edit a single testimonial."""
    if testimonial_id:
        testimonial = get_object_or_404(Testimonial, id=testimonial_id)
    else:
        testimonial = None
    
    if request.method == 'POST':
        if not testimonial:
            testimonial = Testimonial()
        testimonial.name = request.POST.get('name', '')
        testimonial.role = request.POST.get('role', '')
        testimonial.company = request.POST.get('company', '')
        testimonial.content = request.POST.get('content', '')
        testimonial.image_url = request.POST.get('image_url', '')
        testimonial.rating = int(request.POST.get('rating', 5))
        testimonial.sort_order = int(request.POST.get('sort_order', 0))
        testimonial.save()
        return redirect('dashboard:testimonials_list')
    
    return render(request, 'dashboard/testimonial_edit.html', {'testimonial': testimonial})


# FAQ Views
@login_required
def faq_section_edit(request):
    """Edit FAQ section header."""
    section, created = FAQSection.objects.get_or_create(pk=1)
    
    if request.method == 'POST':
        section.title = request.POST.get('title', '')
        section.subtitle = request.POST.get('subtitle', '')
        
        content = {}
        for key, value in request.POST.items():
            if key.startswith('content_'):
                content[key.replace('content_', '')] = value
        section.content = content
        section.save()
        return redirect('dashboard:faq_section_edit')
    
    return render(request, 'dashboard/faq_section_edit.html', {'section': section})


@login_required
def faqs_list(request):
    """List all FAQs."""
    faqs = FAQ.objects.all()
    
    if request.method == 'POST':
        if 'delete_id' in request.POST:
            FAQ.objects.filter(id=request.POST['delete_id']).delete()
            return redirect('dashboard:faqs_list')
        
        faq_id = request.POST.get('faq_id')
        if faq_id:
            faq = get_object_or_404(FAQ, id=faq_id)
        else:
            faq = FAQ()
        
        faq.question = request.POST.get('question', '')
        faq.answer = request.POST.get('answer', '')
        faq.category = request.POST.get('category', '')
        faq.sort_order = int(request.POST.get('sort_order', 0))
        faq.save()
        return redirect('dashboard:faqs_list')
    
    return render(request, 'dashboard/faqs_list.html', {'faqs': faqs})


@login_required
def faq_edit(request, faq_id=None):
    """Edit a single FAQ."""
    if faq_id:
        faq = get_object_or_404(FAQ, id=faq_id)
    else:
        faq = None
    
    if request.method == 'POST':
        if not faq:
            faq = FAQ()
        faq.question = request.POST.get('question', '')
        faq.answer = request.POST.get('answer', '')
        faq.category = request.POST.get('category', '')
        faq.sort_order = int(request.POST.get('sort_order', 0))
        faq.save()
        return redirect('dashboard:faqs_list')
    
    return render(request, 'dashboard/faq_edit.html', {'faq': faq})


# Contact Views
@login_required
def contact_edit(request):
    """Edit contact section."""
    contact, created = Contact.objects.get_or_create(pk=1)
    
    if request.method == 'POST':
        contact.title = request.POST.get('title', '')
        contact.subtitle = request.POST.get('subtitle', '')
        
        content = {}
        for key, value in request.POST.items():
            if key.startswith('content_'):
                content[key.replace('content_', '')] = value
        contact.content = content
        contact.save()
        return redirect('dashboard:contact_edit')
    
    return render(request, 'dashboard/contact_edit.html', {'contact': contact})


@login_required
def contact_info_list(request):
    """List all contact info items."""
    contact_info = ContactInfo.objects.all()
    
    if request.method == 'POST':
        if 'delete_id' in request.POST:
            ContactInfo.objects.filter(id=request.POST['delete_id']).delete()
            return redirect('dashboard:contact_info_list')
        
        info_id = request.POST.get('info_id')
        if info_id:
            info = get_object_or_404(ContactInfo, id=info_id)
        else:
            info = ContactInfo()
        
        info.type = request.POST.get('type', '')
        info.label = request.POST.get('label', '')
        info.value = request.POST.get('value', '')
        info.icon = request.POST.get('icon', '')
        info.sort_order = int(request.POST.get('sort_order', 0))
        info.save()
        return redirect('dashboard:contact_info_list')
    
    return render(request, 'dashboard/contact_info_list.html', {'contact_info': contact_info})


@login_required
def contact_info_edit(request, info_id=None):
    """Edit a single contact info item."""
    if info_id:
        info = get_object_or_404(ContactInfo, id=info_id)
    else:
        info = None
    
    if request.method == 'POST':
        if not info:
            info = ContactInfo()
        info.type = request.POST.get('type', '')
        info.label = request.POST.get('label', '')
        info.value = request.POST.get('value', '')
        info.icon = request.POST.get('icon', '')
        info.sort_order = int(request.POST.get('sort_order', 0))
        info.save()
        return redirect('dashboard:contact_info_list')
    
    return render(request, 'dashboard/contact_info_edit.html', {'info': info})


@login_required
def contact_form_fields_list(request):
    """List all contact form fields."""
    fields = ContactFormField.objects.all()
    
    if request.method == 'POST':
        if 'delete_id' in request.POST:
            ContactFormField.objects.filter(id=request.POST['delete_id']).delete()
            return redirect('dashboard:contact_form_fields_list')
        
        field_id = request.POST.get('field_id')
        if field_id:
            field = get_object_or_404(ContactFormField, id=field_id)
        else:
            field = ContactFormField()
        
        field.name = request.POST.get('name', '')
        field.label = request.POST.get('label', '')
        field.field_type = request.POST.get('field_type', 'text')
        field.required = request.POST.get('required') == 'on'
        field.placeholder = request.POST.get('placeholder', '')
        field.sort_order = int(request.POST.get('sort_order', 0))
        field.save()
        return redirect('dashboard:contact_form_fields_list')
    
    return render(request, 'dashboard/contact_form_fields_list.html', {'fields': fields})


@login_required
def contact_form_field_edit(request, field_id=None):
    """Edit a single contact form field."""
    if field_id:
        field = get_object_or_404(ContactFormField, id=field_id)
    else:
        field = None
    
    if request.method == 'POST':
        if not field:
            field = ContactFormField()
        field.name = request.POST.get('name', '')
        field.label = request.POST.get('label', '')
        field.field_type = request.POST.get('field_type', 'text')
        field.required = request.POST.get('required') == 'on'
        field.placeholder = request.POST.get('placeholder', '')
        field.sort_order = int(request.POST.get('sort_order', 0))
        field.save()
        return redirect('dashboard:contact_form_fields_list')
    
    return render(request, 'dashboard/contact_form_field_edit.html', {'field': field})


# Social Links Views
@login_required
def social_links_list(request):
    """List all social links."""
    links = SocialLink.objects.all()
    
    if request.method == 'POST':
        if 'delete_id' in request.POST:
            SocialLink.objects.filter(id=request.POST['delete_id']).delete()
            return redirect('dashboard:social_links_list')
        
        link_id = request.POST.get('link_id')
        if link_id:
            link = get_object_or_404(SocialLink, id=link_id)
        else:
            link = SocialLink()
        
        link.platform = request.POST.get('platform', '')
        link.url = request.POST.get('url', '')
        link.icon = request.POST.get('icon', '')
        link.sort_order = int(request.POST.get('sort_order', 0))
        link.save()
        return redirect('dashboard:social_links_list')
    
    return render(request, 'dashboard/social_links_list.html', {'links': links})


@login_required
def social_link_edit(request, link_id=None):
    """Edit a single social link."""
    if link_id:
        link = get_object_or_404(SocialLink, id=link_id)
    else:
        link = None
    
    if request.method == 'POST':
        if not link:
            link = SocialLink()
        link.platform = request.POST.get('platform', '')
        link.url = request.POST.get('url', '')
        link.icon = request.POST.get('icon', '')
        link.sort_order = int(request.POST.get('sort_order', 0))
        link.save()
        return redirect('dashboard:social_links_list')
    
    return render(request, 'dashboard/social_link_edit.html', {'link': link})


# Footer Views
@login_required
def footer_edit(request):
    """Edit footer."""
    footer, created = Footer.objects.get_or_create(pk=1)
    
    if request.method == 'POST':
        footer.copyright_text = request.POST.get('copyright_text', '')
        
        content = {}
        for key, value in request.POST.items():
            if key.startswith('content_'):
                content[key.replace('content_', '')] = value
        footer.content = content
        footer.save()
        return redirect('dashboard:footer_edit')
    
    return render(request, 'dashboard/footer_edit.html', {'footer': footer})

