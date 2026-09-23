import os
import django
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dukan.settings')
django.setup()

from dabeli.models import Category, MenuItem

def run():
    print("Seeding Menu Items...")
    
    Category.objects.all().delete()
    MenuItem.objects.all().delete()
    
    cat_dabeli = Category.objects.create(name='Dabeli')
    cat_vadapav = Category.objects.create(name='Vadapav')
    cat_fries = Category.objects.create(name='Fries')
    
    items_to_create = [
        (cat_dabeli, 'Classic Dabeli', 'The original Surat taste.', 30.00, 'dabeli/static/dimage/img.png'),
        (cat_vadapav, 'Cheese Vadapav', 'Loaded with cheese.', 45.00, 'dabeli/static/dimage/img_1.png'),
        (cat_fries, 'Peri Peri Fries', 'Spicy and crispy.', 70.00, 'dabeli/static/dimage/WhatsApp Image 2024-01-04 at 00.28.47 (3).jpeg')
    ]
    
    for cat, name, desc, price, img_path in items_to_create:
        print(f"Creating {name}...")
        item = MenuItem(category=cat, name=name, description=desc, price=price, is_available=True)
        with open(img_path, 'rb') as f:
            item.image.save(os.path.basename(img_path), File(f))
        item.save()
        
    print("Done seeding menu items!")

if __name__ == '__main__':
    run()
