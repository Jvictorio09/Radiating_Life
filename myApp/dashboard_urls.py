"""
Dashboard URL configuration.
"""

from django.urls import path
from . import dashboard_views

app_name = 'dashboard'

urlpatterns = [
    # Authentication
    path('login/', dashboard_views.dashboard_login, name='login'),
    path('logout/', dashboard_views.dashboard_logout, name='logout'),
    
    # Dashboard Home
    path('', dashboard_views.dashboard_home, name='index'),
    
    # Image Upload and Gallery
    path('upload-image/', dashboard_views.upload_image, name='upload_image'),
    path('gallery/', dashboard_views.gallery, name='gallery'),
    
    # SEO
    path('seo/', dashboard_views.seo_edit, name='seo_edit'),
    
    # Navigation
    path('navigation/', dashboard_views.navigation_edit, name='navigation_edit'),
    
    # Hero
    path('hero/', dashboard_views.hero_edit, name='hero_edit'),
    
    # About
    path('about/', dashboard_views.about_edit, name='about_edit'),
    
    # Stats
    path('stats/', dashboard_views.stats_list, name='stats_list'),
    path('stats/add/', dashboard_views.stat_edit, name='stat_add'),
    path('stats/<int:stat_id>/', dashboard_views.stat_edit, name='stat_edit'),
    
    # Services
    path('services-section/', dashboard_views.services_section_edit, name='services_section_edit'),
    path('services/', dashboard_views.services_list, name='services_list'),
    path('services/add/', dashboard_views.service_edit, name='service_add'),
    path('services/<int:service_id>/', dashboard_views.service_edit, name='service_edit'),
    
    # Portfolio
    path('portfolio/', dashboard_views.portfolio_edit, name='portfolio_edit'),
    path('portfolio-projects/', dashboard_views.portfolio_projects_list, name='portfolio_projects_list'),
    path('portfolio-projects/add/', dashboard_views.portfolio_project_edit, name='portfolio_project_add'),
    path('portfolio-projects/<int:project_id>/', dashboard_views.portfolio_project_edit, name='portfolio_project_edit'),
    
    # Testimonials
    path('testimonials/', dashboard_views.testimonials_list, name='testimonials_list'),
    path('testimonials/add/', dashboard_views.testimonial_edit, name='testimonial_add'),
    path('testimonials/<int:testimonial_id>/', dashboard_views.testimonial_edit, name='testimonial_edit'),
    
    # FAQs
    path('faq-section/', dashboard_views.faq_section_edit, name='faq_section_edit'),
    path('faqs/', dashboard_views.faqs_list, name='faqs_list'),
    path('faqs/add/', dashboard_views.faq_edit, name='faq_add'),
    path('faqs/<int:faq_id>/', dashboard_views.faq_edit, name='faq_edit'),
    
    # Contact
    path('contact/', dashboard_views.contact_edit, name='contact_edit'),
    path('contact-info/', dashboard_views.contact_info_list, name='contact_info_list'),
    path('contact-info/add/', dashboard_views.contact_info_edit, name='contact_info_add'),
    path('contact-info/<int:info_id>/', dashboard_views.contact_info_edit, name='contact_info_edit'),
    path('contact-form-fields/', dashboard_views.contact_form_fields_list, name='contact_form_fields_list'),
    path('contact-form-fields/add/', dashboard_views.contact_form_field_edit, name='contact_form_field_add'),
    path('contact-form-fields/<int:field_id>/', dashboard_views.contact_form_field_edit, name='contact_form_field_edit'),
    
    # Social Links
    path('social-links/', dashboard_views.social_links_list, name='social_links_list'),
    path('social-links/add/', dashboard_views.social_link_edit, name='social_link_add'),
    path('social-links/<int:link_id>/', dashboard_views.social_link_edit, name='social_link_edit'),
    
    # Footer
    path('footer/', dashboard_views.footer_edit, name='footer_edit'),
]

