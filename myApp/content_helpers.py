"""
Content helpers for converting database models to JSON format for templates.
"""

from .models import (
    SEO, Navigation, Hero, About, Stat, Service, ServicesSection,
    Portfolio, PortfolioProject, Testimonial, FAQ, FAQSection,
    Contact, ContactInfo, ContactFormField, SocialLink, Footer
)


def get_homepage_content_from_db():
    """
    Get all homepage content from database and convert to JSON format.
    
    Returns:
        Dictionary with all homepage content sections
    """
    content = {}
    
    # SEO
    try:
        seo = SEO.objects.first()
        if seo:
            content['seo'] = {
                'title': seo.title,
                'description': seo.description,
                'keywords': seo.keywords,
                'og_image': seo.og_image,
                'og_title': seo.og_title,
                'og_description': seo.og_description,
            }
    except:
        content['seo'] = {}
    
    # Navigation
    try:
        nav_items = Navigation.objects.filter(is_active=True)
        content['navigation'] = [
            {
                'label': item.label,
                'url': item.url,
            }
            for item in nav_items
        ]
    except:
        content['navigation'] = []
    
    # Hero
    try:
        hero = Hero.objects.first()
        if hero:
            hero_data = {
                'title': hero.title,
                'subtitle': hero.subtitle,
                'image_url': hero.image_url,
                'button_text': hero.button_text,
                'button_url': hero.button_url,
            }
            # Merge with JSON content
            if hero.content:
                hero_data.update(hero.content)
            content['hero'] = hero_data
    except:
        content['hero'] = {}
    
    # About
    try:
        about = About.objects.first()
        if about:
            about_data = {
                'title': about.title,
                'description': about.description,
                'image_url': about.image_url,
            }
            if about.content:
                about_data.update(about.content)
            content['about'] = about_data
    except:
        content['about'] = {}
    
    # Stats
    try:
        stats = Stat.objects.all()
        content['stats'] = [
            {
                'number': stat.number,
                'label': stat.label,
                'icon': stat.icon,
            }
            for stat in stats
        ]
    except:
        content['stats'] = []
    
    # Services Section
    try:
        services_section = ServicesSection.objects.first()
        if services_section:
            services_data = {
                'title': services_section.title,
                'subtitle': services_section.subtitle,
            }
            if services_section.content:
                services_data.update(services_section.content)
            content['services_section'] = services_data
    except:
        content['services_section'] = {}
    
    # Services
    try:
        services = Service.objects.all()
        content['services'] = [
            {
                'title': service.title,
                'description': service.description,
                'image_url': service.image_url,
                'icon': service.icon,
            }
            for service in services
        ]
    except:
        content['services'] = []
    
    # Portfolio
    try:
        portfolio = Portfolio.objects.first()
        if portfolio:
            portfolio_data = {
                'title': portfolio.title,
                'subtitle': portfolio.subtitle,
            }
            if portfolio.content:
                portfolio_data.update(portfolio.content)
            content['portfolio'] = portfolio_data
    except:
        content['portfolio'] = {}
    
    # Portfolio Projects
    try:
        projects = PortfolioProject.objects.all()
        content['portfolio_projects'] = [
            {
                'title': project.title,
                'description': project.description,
                'image_url': project.image_url,
                'gallery': project.gallery if isinstance(project.gallery, list) else [],
                'category': project.category,
            }
            for project in projects
        ]
    except:
        content['portfolio_projects'] = []
    
    # Testimonials
    try:
        testimonials = Testimonial.objects.all()
        content['testimonials'] = [
            {
                'name': testimonial.name,
                'role': testimonial.role,
                'company': testimonial.company,
                'content': testimonial.content,
                'image_url': testimonial.image_url,
                'rating': testimonial.rating,
            }
            for testimonial in testimonials
        ]
    except:
        content['testimonials'] = []
    
    # FAQ Section
    try:
        faq_section = FAQSection.objects.first()
        if faq_section:
            faq_data = {
                'title': faq_section.title,
                'subtitle': faq_section.subtitle,
            }
            if faq_section.content:
                faq_data.update(faq_section.content)
            content['faq_section'] = faq_data
    except:
        content['faq_section'] = {}
    
    # FAQs
    try:
        faqs = FAQ.objects.all()
        content['faqs'] = [
            {
                'question': faq.question,
                'answer': faq.answer,
                'category': faq.category,
            }
            for faq in faqs
        ]
    except:
        content['faqs'] = []
    
    # Contact
    try:
        contact = Contact.objects.first()
        if contact:
            contact_data = {
                'title': contact.title,
                'subtitle': contact.subtitle,
            }
            if contact.content:
                contact_data.update(contact.content)
            content['contact'] = contact_data
    except:
        content['contact'] = {}
    
    # Contact Info
    try:
        contact_info = ContactInfo.objects.all()
        content['contact_info'] = [
            {
                'type': info.type,
                'label': info.label,
                'value': info.value,
                'icon': info.icon,
            }
            for info in contact_info
        ]
    except:
        content['contact_info'] = []
    
    # Contact Form Fields
    try:
        form_fields = ContactFormField.objects.all()
        content['contact_form_fields'] = [
            {
                'name': field.name,
                'label': field.label,
                'type': field.field_type,
                'required': field.required,
                'placeholder': field.placeholder,
            }
            for field in form_fields
        ]
    except:
        content['contact_form_fields'] = []
    
    # Social Links
    try:
        social_links = SocialLink.objects.all()
        content['social_links'] = [
            {
                'platform': link.platform,
                'url': link.url,
                'icon': link.icon,
            }
            for link in social_links
        ]
    except:
        content['social_links'] = []
    
    # Footer
    try:
        footer = Footer.objects.first()
        if footer:
            footer_data = {
                'copyright_text': footer.copyright_text,
            }
            if footer.content:
                footer_data.update(footer.content)
            content['footer'] = footer_data
    except:
        content['footer'] = {}
    
    return content

