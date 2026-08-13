import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dukan.settings')
django.setup()

from dabeli.models import HomePageContent

def run():
    print("Seeding HomePageContent...")
    
    # We will use the exact text from the original index.html
    HomePageContent.objects.all().delete()
    
    about_text = """Dinesh Dabeli embarked on its journey in 2011 as a humble roadside fast-food stall adjacent to DRB College in New City Light, Udhana, Gujarat. Operating initially on the footpath, the establishment was a family endeavor with the dedicated efforts of the Dubey family members, who worked tirelessly to transform their dream into reality. Overcoming challenges through unwavering determination and continuous hard work, we witnessed substantial growth.

In 2016, a new milestone was achieved as we proudly inaugurated our second branch in Bhimrad, Surat. Alongside our renowned Dabeli, we introduced the popular Vadapav to our menu, catering to diverse palates. The year 2023 marked a significant transition from a stall to a permanent shop, reflecting our commitment to excellence.

Building upon our success, we proudly inaugurated our third branch in a new location in the same year. Presently, Dinesh Dabeli boasts three thriving branches, a dedicated team of six skilled workers, and the leadership of Dinesh Dubey along with his father, Shyam Murari Dubey. Our journey is a testament to passion, hard work, and the enduring commitment to providing delightful culinary experiences. Welcome to the world of Dinesh Dabeli, where each bite tells about a story of our rich heritage and culinary expertise."""

    HomePageContent.objects.create(
        hero_title="TASTY",
        hero_subtitle="Treat Yourself: Relish Surat's tastiest Fast Food at Wallet-Friendly Prices!",
        hero_image_url="/static/dimage/WhatsApp%20Image%202024-01-04%20at%2000.28.47%20(3).jpeg",
        about_title="We Are Dinesh Dabeli",
        about_text=about_text,
        about_image_url="/static/images/kid.png"
    )
    print("Done!")

if __name__ == '__main__':
    run()
