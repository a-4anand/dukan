from django.contrib import admin
from django.utils.html import format_html
from .models import Contact, Rating, Category, MenuItem, HomePageContent, Offer

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_available', 'image_preview')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description')
    list_editable = ('price', 'is_available')
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 5px; object-fit: cover;"/>', obj.image.url)
        elif obj.image_url:
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 5px; object-fit: cover;"/>', obj.image_url)
        return "No Image"
    image_preview.short_description = 'Preview'

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'discount_text', 'is_active', 'image_preview')
    list_editable = ('is_active',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 5px; object-fit: cover;"/>', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'

@admin.register(HomePageContent)
class HomePageContentAdmin(admin.ModelAdmin):
    list_display = ('hero_title', 'about_title')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'message', 'phone')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'submitted_at')
    list_filter = ('rating', 'submitted_at')
    search_fields = ('name', 'comments')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'css_class')
