"""
Management command to import homepage data from JSON file.
"""

import json
from django.core.management.base import BaseCommand
from myApp.models import (
    SEO, Navigation, Hero, About, Stat, Service, ServicesSection,
    Portfolio, PortfolioProject, Testimonial, FAQ, FAQSection,
    Contact, ContactInfo, ContactFormField, SocialLink, Footer, MediaAsset
)


class Command(BaseCommand):
    help = 'Import homepage data from JSON file'

    def add_arguments(self, parser):
        parser.add_argument(
            'file',
            type=str,
            help='JSON file path to import'
        )

    def handle(self, *args, **options):
        file_path = options['file']
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'File not found: {file_path}')
            )
            return
        except json.JSONDecodeError:
            self.stdout.write(
                self.style.ERROR(f'Invalid JSON file: {file_path}')
            )
            return
        
        # Import each section
        if 'seo' in data:
            self.import_seo(data['seo'])
        
        if 'navigation' in data:
            self.import_navigation(data['navigation'])
        
        if 'hero' in data:
            self.import_hero(data['hero'])
        
        if 'about' in data:
            self.import_about(data['about'])
        
        if 'stats' in data:
            self.import_stats(data['stats'])
        
        if 'services_section' in data:
            self.import_services_section(data['services_section'])
        
        if 'services' in data:
            self.import_services(data['services'])
        
        if 'portfolio' in data:
            self.import_portfolio(data['portfolio'])
        
        if 'portfolio_projects' in data:
            self.import_portfolio_projects(data['portfolio_projects'])
        
        if 'testimonials' in data:
            self.import_testimonials(data['testimonials'])
        
        if 'faq_section' in data:
            self.import_faq_section(data['faq_section'])
        
        if 'faqs' in data:
            self.import_faqs(data['faqs'])
        
        if 'contact' in data:
            self.import_contact(data['contact'])
        
        if 'contact_info' in data:
            self.import_contact_info(data['contact_info'])
        
        if 'contact_form_fields' in data:
            self.import_contact_form_fields(data['contact_form_fields'])
        
        if 'social_links' in data:
            self.import_social_links(data['social_links'])
        
        if 'footer' in data:
            self.import_footer(data['footer'])
        
        if 'media_assets' in data:
            self.import_media_assets(data['media_assets'])
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully imported data from {file_path}')
        )

    def import_seo(self, data):
        seo, created = SEO.objects.get_or_create(pk=1)
        for key, value in data.items():
            setattr(seo, key, value)
        seo.save()

    def import_navigation(self, data):
        Navigation.objects.all().delete()
        for item_data in data:
            Navigation.objects.create(**item_data)

    def import_hero(self, data):
        hero, created = Hero.objects.get_or_create(pk=1)
        for key, value in data.items():
            setattr(hero, key, value)
        hero.save()

    def import_about(self, data):
        about, created = About.objects.get_or_create(pk=1)
        for key, value in data.items():
            setattr(about, key, value)
        about.save()

    def import_stats(self, data):
        Stat.objects.all().delete()
        for stat_data in data:
            Stat.objects.create(**stat_data)

    def import_services_section(self, data):
        section, created = ServicesSection.objects.get_or_create(pk=1)
        for key, value in data.items():
            setattr(section, key, value)
        section.save()

    def import_services(self, data):
        Service.objects.all().delete()
        for service_data in data:
            Service.objects.create(**service_data)

    def import_portfolio(self, data):
        portfolio, created = Portfolio.objects.get_or_create(pk=1)
        for key, value in data.items():
            setattr(portfolio, key, value)
        portfolio.save()

    def import_portfolio_projects(self, data):
        PortfolioProject.objects.all().delete()
        for project_data in data:
            PortfolioProject.objects.create(**project_data)

    def import_testimonials(self, data):
        Testimonial.objects.all().delete()
        for testimonial_data in data:
            Testimonial.objects.create(**testimonial_data)

    def import_faq_section(self, data):
        section, created = FAQSection.objects.get_or_create(pk=1)
        for key, value in data.items():
            setattr(section, key, value)
        section.save()

    def import_faqs(self, data):
        FAQ.objects.all().delete()
        for faq_data in data:
            FAQ.objects.create(**faq_data)

    def import_contact(self, data):
        contact, created = Contact.objects.get_or_create(pk=1)
        for key, value in data.items():
            setattr(contact, key, value)
        contact.save()

    def import_contact_info(self, data):
        ContactInfo.objects.all().delete()
        for info_data in data:
            ContactInfo.objects.create(**info_data)

    def import_contact_form_fields(self, data):
        ContactFormField.objects.all().delete()
        for field_data in data:
            ContactFormField.objects.create(**field_data)

    def import_social_links(self, data):
        SocialLink.objects.all().delete()
        for link_data in data:
            SocialLink.objects.create(**link_data)

    def import_footer(self, data):
        footer, created = Footer.objects.get_or_create(pk=1)
        for key, value in data.items():
            setattr(footer, key, value)
        footer.save()

    def import_media_assets(self, data):
        # Only import if they don't exist (to avoid duplicates)
        for asset_data in data:
            if not MediaAsset.objects.filter(cloudinary_public_id=asset_data.get('cloudinary_public_id')).exists():
                MediaAsset.objects.create(**asset_data)

