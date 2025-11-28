from django.contrib import admin
from .models import (
    MediaAsset, SEO, Navigation, Hero, About, Stat, Service, ServicesSection,
    Portfolio, PortfolioProject, Testimonial, FAQ, FAQSection,
    Contact, ContactInfo, ContactFormField, SocialLink, Footer
)

# Register your models here.

@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'format', 'width', 'height', 'uploaded_at']
    list_filter = ['format', 'was_converted', 'uploaded_at']
    search_fields = ['file_name', 'cloudinary_public_id']
    readonly_fields = ['uploaded_at']

@admin.register(SEO)
class SEOAdmin(admin.ModelAdmin):
    pass

@admin.register(Navigation)
class NavigationAdmin(admin.ModelAdmin):
    list_display = ['label', 'url', 'sort_order', 'is_active']
    list_editable = ['sort_order', 'is_active']
    list_filter = ['is_active']

@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    pass

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    pass

@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ['number', 'label', 'sort_order']
    list_editable = ['sort_order']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'sort_order']
    list_editable = ['sort_order']
    search_fields = ['title', 'description']

@admin.register(ServicesSection)
class ServicesSectionAdmin(admin.ModelAdmin):
    pass

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    pass

@admin.register(PortfolioProject)
class PortfolioProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'sort_order']
    list_editable = ['sort_order']
    list_filter = ['category']
    search_fields = ['title', 'description']

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'rating', 'sort_order']
    list_editable = ['sort_order']
    list_filter = ['rating']
    search_fields = ['name', 'company', 'content']

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'sort_order']
    list_editable = ['sort_order']
    list_filter = ['category']
    search_fields = ['question', 'answer']

@admin.register(FAQSection)
class FAQSectionAdmin(admin.ModelAdmin):
    pass

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['type', 'label', 'value', 'sort_order']
    list_editable = ['sort_order']
    list_filter = ['type']

@admin.register(ContactFormField)
class ContactFormFieldAdmin(admin.ModelAdmin):
    list_display = ['name', 'label', 'field_type', 'required', 'sort_order']
    list_editable = ['sort_order', 'required']
    list_filter = ['field_type', 'required']

@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ['platform', 'url', 'sort_order']
    list_editable = ['sort_order']
    list_filter = ['platform']

@admin.register(Footer)
class FooterAdmin(admin.ModelAdmin):
    pass
