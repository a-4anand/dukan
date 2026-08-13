import os
import django
from bs4 import BeautifulSoup
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dukan.settings')
django.setup()

from dabeli.models import Category, MenuItem

def run():
    print("Deleting old records...")
    Category.objects.all().delete()
    MenuItem.objects.all().delete()

    html_file = 'dabeli/templates/menu.html'
    with open(html_file, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    
    # First, create categories from filters
    filters = soup.select('.filters_menu li')
    for f in filters:
        filter_data = f.get('data-filter')
        if filter_data and filter_data != '*':
            css_class = filter_data.replace('.', '')
            name = f.text.strip()
            Category.objects.get_or_create(name=name, css_class=css_class)
    
    categories = {c.css_class: c for c in Category.objects.all()}

    # Then parse the items
    items = soup.select('.filters-content .col-sm-6')
    for item in items:
        # Find category class
        classes = item.get('class', [])
        cat = None
        for cls in classes:
            if cls in categories:
                cat = categories[cls]
                break
        
        if not cat:
            print(f"Skipping item, unknown category classes: {classes}")
            continue

        name_tag = item.find('h5')
        name = name_tag.text.strip() if name_tag else "Unknown"

        desc_tag = item.find('p')
        desc = desc_tag.text.strip() if desc_tag else ""

        img_tag = item.find('img')
        img_url = img_tag.get('src') if img_tag else ""
        
        # fix the src if it has ../
        img_url = img_url.replace('../', '/')

        link_tag = item.find('a')
        order_link = link_tag.get('href') if link_tag else ""

        print(f"Adding: {name} in {cat.name}")
        MenuItem.objects.create(
            category=cat,
            name=name,
            description=desc,
            image_url=img_url,
            order_link=order_link
        )
    
    print("Done!")

if __name__ == '__main__':
    run()
