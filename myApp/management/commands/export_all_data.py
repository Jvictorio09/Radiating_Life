"""
Management command to export all dashboard content to JSON.
"""

import json
from django.core.management.base import BaseCommand
from myApp.models import (
    SEO, Navigation, Hero, About, Stat, Service, ServicesSection,
    Portfolio, PortfolioProject, Testimonial, FAQ, FAQSection,
    Contact, ContactInfo, ContactFormField, SocialLink, Footer, MediaAsset
)


class Command(BaseCommand):
    help = 'Export all dashboard content to JSON file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            default='dashboard_export.json',
            help='Output file path (default: dashboard_export.json)'
        )

    def handle(self, *args, **options):
        output_file = options['output']
        
        data = {
            'seo': self.export_seo(),
            'navigation': self.export_navigation(),
            'hero': self.export_hero(),
            'about': self.export_about(),
            'stats': self.export_stats(),
            'services_section': self.export_services_section(),
            'services': self.export_services(),
            'portfolio': self.export_portfolio(),
            'portfolio_projects': self.export_portfolio_projects(),
            'testimonials': self.export_testimonials(),
            'faq_section': self.export_faq_section(),
            'faqs': self.export_faqs(),
            'contact': self.export_contact(),
            'contact_info': self.export_contact_info(),
            'contact_form_fields': self.export_contact_form_fields(),
            'social_links': self.export_social_links(),
            'footer': self.export_footer(),
            'media_assets': self.export_media_assets(),
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully exported all data to {output_file}')
        )

    def export_seo(self):
        seo = SEO.objects.first()
        if seo:
            return {
                'title': seo.title,
                'description': seo.description,
                'keywords': seo.keywords,
                'og_image': seo.og_image,
                'og_title': seo.og_title,
                'og_description': seo.og_description,
            }
        return {}

    def export_navigation(self):
        return [
            {
                'label': item.label,
                'url': item.url,
                'sort_order': item.sort_order,
                'is_active': item.is_active,
            }
            for item in Navigation.objects.all()
        ]

    def export_hero(self):
        hero = Hero.objects.first()
        if hero:
            return {
                'title': hero.title,
                'subtitle': hero.subtitle,
                'image_url': hero.image_url,
                'button_text': hero.button_text,
                'button_url': hero.button_url,
                'content': hero.content,
            }
        return {}

    def export_about(self):
        about = About.objects.first()
        if about:
            return {
                'title': about.title,
                'description': about.description,
                'image_url': about.image_url,
                'content': about.content,
            }
        return {}

    def export_stats(self):
        return [
            {
                'number': stat.number,
                'label': stat.label,
                'icon': stat.icon,
                'sort_order': stat.sort_order,
            }
            for stat in Stat.objects.all()
        ]

    def export_services_section(self):
        section = ServicesSection.objects.first()
        if section:
            return {
                'title': section.title,
                'subtitle': section.subtitle,
                'content': section.content,
            }
        return {}

    def export_services(self):
        return [
            {
                'title': service.title,
                'description': service.description,
                'image_url': service.image_url,
                'icon': service.icon,
                'sort_order': service.sort_order,
                'content': service.content,
            }
            for service in Service.objects.all()
        ]

    def export_portfolio(self):
        portfolio = Portfolio.objects.first()
        if portfolio:
            return {
                'title': portfolio.title,
                'subtitle': portfolio.subtitle,
                'content': portfolio.content,
            }
        return {}

    def export_portfolio_projects(self):
        return [
            {
                'title': project.title,
                'description': project.description,
                'image_url': project.image_url,
                'gallery': project.gallery,
                'category': project.category,
                'sort_order': project.sort_order,
                'content': project.content,
            }
            for project in PortfolioProject.objects.all()
        ]

    def export_testimonials(self):
        return [
            {
                'name': testimonial.name,
                'role': testimonial.role,
                'company': testimonial.company,
                'content': testimonial.content,
                'image_url': testimonial.image_url,
                'rating': testimonial.rating,
                'sort_order': testimonial.sort_order,
            }
            for testimonial in Testimonial.objects.all()
        ]

    def export_faq_section(self):
        section = FAQSection.objects.first()
        if section:
            return {
                'title': section.title,
                'subtitle': section.subtitle,
                'content': section.content,
            }
        return {}

    def export_faqs(self):
        return [
            {
                'question': faq.question,
                'answer': faq.answer,
                'category': faq.category,
                'sort_order': faq.sort_order,
            }
            for faq in FAQ.objects.all()
        ]

    def export_contact(self):
        contact = Contact.objects.first()
        if contact:
            return {
                'title': contact.title,
                'subtitle': contact.subtitle,
                'content': contact.content,
            }
        return {}

    def export_contact_info(self):
        return [
            {
                'type': info.type,
                'label': info.label,
                'value': info.value,
                'icon': info.icon,
                'sort_order': info.sort_order,
            }
            for info in ContactInfo.objects.all()
        ]

    def export_contact_form_fields(self):
        return [
            {
                'name': field.name,
                'label': field.label,
                'field_type': field.field_type,
                'required': field.required,
                'placeholder': field.placeholder,
                'sort_order': field.sort_order,
            }
            for field in ContactFormField.objects.all()
        ]

    def export_social_links(self):
        return [
            {
                'platform': link.platform,
                'url': link.url,
                'icon': link.icon,
                'sort_order': link.sort_order,
            }
            for link in SocialLink.objects.all()
        ]

    def export_footer(self):
        footer = Footer.objects.first()
        if footer:
            return {
                'copyright_text': footer.copyright_text,
                'content': footer.content,
            }
        return {}

    def export_media_assets(self):
        return [
            {
                'original_path': asset.original_path,
                'file_name': asset.file_name,
                'cloudinary_url': asset.cloudinary_url,
                'cloudinary_public_id': asset.cloudinary_public_id,
                'format': asset.format,
                'width': asset.width,
                'height': asset.height,
                'file_size': asset.file_size,
                'was_converted': asset.was_converted,
            }
            for asset in MediaAsset.objects.all()
        ]

