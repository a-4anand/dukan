from django.contrib import admin
#
from .models import Contact, Rating, Category, MenuItem, HomePageContent, Offer
#
#
#
#
admin.site.register(Contact)
admin.site.register(Rating)
admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(HomePageContent)
admin.site.register(Offer)

# your_app/admin.py

from django.contrib import admin

# Customize admin site behavior, e.g., change the site header
admin.site.site_header = 'Admin Dashboard'

# admin.py
# from django.contrib import admin

# class YourModelAdmin(admin.ModelAdmin):
#     class Media:
#         css = {
#             'all': ('path/to/admin_custom.css',),
#         }
