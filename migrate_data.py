import os
import django
import sqlite3
import urllib.parse
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dukan.settings')
django.setup()

from dabeli.models import Category, MenuItem

def get_improved_description(name, old_desc):
    improvements = {
        'Cheese VadaPav': "Experience the perfect fusion of bold street-food flavors with a generous, melting core of premium cheese that will instantly win your heart.",
        'Mayonese Dabeli': "A scrumptious twist on a classic favorite! Enjoy a creamy, indulgent layer of mayonnaise perfectly balanced with our signature spicy Dabeli filling.",
        'Mayo Vadapav': "Elevate your taste buds with our Mayo Vadapav—a delightful symphony of creamy mayonnaise and our perfectly spiced, golden-fried potato vada.",
        'Mayo Masala Samosa': "The ultimate flavor fusion: our classic, extra-crunchy masala samosa served with a rich and creamy mayo twist for a truly delightful sensation.",
        'Cheese Masala Samosa': "Indulge in a crispy, golden sensation packed with an aromatic blend of secret spices and oozing, gooey cheese in every bite.",
        'Amul Butter Masala Dabeli': "An explosion of authentic flavors! A spicy, tangy, and sweet delight wrapped in a soft bun, roasted to perfection in rich Amul Butter.",
        'Sp. Dabeli': "Our best-selling icon! Savor the legendary medley of spicy, sweet, and tangy goodness, packed with crunch and served in a butter-toasted bun.",
        'Sp. TimePass': "The ultimate cheesy craving! A symphony of luscious cheese, creamy mayonnaise, and mouth-watering spices that you simply won't be able to put down.",
        'Sp. Solid Masti Pav': "A true feast for the senses! The irresistible crunch of Kurkure meets luscious Solid Masti cheese, spicy masala, and rich butter to steal your heart."
    }
    return improvements.get(name, old_desc)

def get_realistic_price(name, old_price):
    if old_price and float(old_price) > 0:
        return old_price
    prices = {
        'Cheese VadaPav': 45.00,
        'Mayonese Dabeli': 35.00,
        'Mayo Vadapav': 40.00,
        'Mayo Masala Samosa': 30.00,
        'Cheese Masala Samosa': 40.00,
        'Amul Butter Masala Dabeli': 50.00,
        'Sp. Dabeli': 40.00,
        'Sp. TimePass': 60.00,
        'Sp. Solid Masti Pav': 80.00,
    }
    return prices.get(name, 50.00)

def run():
    print("Migrating data from SQLite to Neon Postgres with Cloudinary...")
    
    # Clear existing
    Category.objects.all().delete()
    MenuItem.objects.all().delete()
    
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    # Migrate Categories
    cursor.execute("SELECT id, name FROM dabeli_category")
    categories = cursor.fetchall()
    cat_map = {}
    for cat_id, name in categories:
        cat = Category.objects.create(name=name)
        cat_map[cat_id] = cat
        print(f"Created category: {name}")
        
    # Migrate Menu Items
    cursor.execute("SELECT id, name, description, price, category_id, image, image_url FROM dabeli_menuitem")
    items = cursor.fetchall()
    
    for row in items:
        item_id, name, desc, price, cat_id, image_field, image_url = row
        cat = cat_map.get(cat_id)
        if not cat:
            continue
            
        improved_desc = get_improved_description(name, desc)
        new_price = get_realistic_price(name, price)
        
        item = MenuItem(category=cat, name=name, description=improved_desc, price=new_price, is_available=True)
        
        # Handle Image Upload to Cloudinary
        image_path_to_use = None
        if image_url:
            # e.g., /static/dimage/img.png
            decoded_url = urllib.parse.unquote(image_url)
            local_path = os.path.join('dabeli', decoded_url.lstrip('/'))
            if os.path.exists(local_path):
                image_path_to_use = local_path
                
        if image_path_to_use:
            print(f"Uploading image for {name} from {image_path_to_use}...")
            with open(image_path_to_use, 'rb') as f:
                item.image.save(os.path.basename(image_path_to_use), File(f), save=False)
        else:
            print(f"No valid local image found for {name}.")
            
        item.save()
        print(f"Created {name}!")

    conn.close()
    print("Migration complete!")

if __name__ == '__main__':
    run()
