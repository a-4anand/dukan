import json
import re
from decimal import Decimal
from difflib import SequenceMatcher
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import transaction

from dabeli.models import Category, MenuItem


STOP_WORDS = {
    "a", "an", "and", "cheesy", "crispy", "fresh", "fried", "golden", "griddled",
    "on", "of", "simple", "sliced", "street", "style", "the", "toasted", "with",
}


def tokens(value):
    value = value.lower().replace("vadapav", "vada pav").replace("pavbhaji", "pav bhaji")
    return {token for token in re.findall(r"[a-z]+", value) if token not in STOP_WORDS}


def image_score(item_name, category_name, image_name):
    item_tokens = tokens(item_name) | tokens(category_name)
    image_tokens = tokens(image_name)
    overlap = len(item_tokens & image_tokens)
    category_match = 1 if tokens(category_name) & image_tokens else 0
    similarity = SequenceMatcher(None, item_name.lower(), image_name.lower()).ratio()
    return overlap * 3 + category_match + similarity


# The asset library contains enough category-specific photos for the catalog,
# but a global fuzzy match can spend a sandwich photo on an unrelated item and
# then fall back to chillies or a samosa. Keep matching inside the right food
# family first, with a small amount of deliberate overlap for generic items.
IMAGE_FAMILY_PATTERNS = {
    "Frankie": ("frankie", "chatgpt-image"),
    "Dabeli": ("dabeli",),
    "Vadapav": ("vadapav", "vada-pav"),
    "Samosa": ("samosa",),
    "Time Pass": ("time-pass", "chaat", "wafers", "chips"),
    "Pavbhaji": ("pav-bhaji", "pasta-pav", "masala-pav"),
    "Mayo Pav": ("mayo-pav", "wafer", "butter-pav", "pav-rolls", "masala-pav"),
    "French Fries": ("fries",),
    "Veg Burger": ("burger",),
    "Grill Sandwich": ("sandwich",),
    "Bread Butter": (
        "buttery-green-chutney-bread-sandwich",
        "golden-butter-grilled-bread-triangles",
        "simple-bread-butter-cheese-sandwich",
        "street-style-jam-butter-bread",
    ),
    "Special Combo": ("combo", "with-fries-and-cola"),
}


IMAGE_OVERRIDES = {
    "frankie__cheese-frankie": "cheesy-street-style-frankie-wrap",
    "frankie__mayo-frankie": "creamy-mayo-frankie-wrap-cut-open",
    "frankie__cheese-mayo-frankie": "street-style-cheesy-mayo-frankie",
    "dabeli__sp-masala-dabeli": "cheesy-gujarati-dabeli-on-steel-plate",
    "dabeli__sp-delicious-sev-dabeli": "gujarati-sev-dabeli-with-pomegranate",
    "dabeli__sp-amul-butter-masala-dabeli": "buttery-gujarati-dabeli-with-sev",
    "dabeli__sp-mayo-dabeli": "golden-toasted-dabeli-with-creamy-mayo",
    "dabeli__sp-amul-butter-mayo-dabeli": "creamy-gujarati-mayo-dabeli",
    "dabeli__sp-amul-cheese-dabeli": "cheesy-street-style-gujarati-dabeli",
    "dabeli__sp-cheese-masala-dabeli": "cheesy-gujarati-dabeli-on-steel-plate",
    "vadapav__sp-delicious-jumbo-vadapav": "golden-butter-toasted-vada-pav",
    "vadapav__sp-amul-cheese-vadapav": "golden-street-style-cheese-vada-pav",
    "vadapav__sp-peri-peri-vadapav": "fiery-peri-peri-vada-pav",
    "vadapav__sp-tadka-vadapav": "street-style-tadka-vada-pav",
    # Sandwiches have near-identical names, so use the matching generated
    # sandwich photo rather than letting fuzzy matching consume another family.
    "sandwich__veggies-cheese-grill-sandwich-2-slice": "golden-grilled-veggie-cheese-sandwich",
    "sandwich__veggies-cheese-grill-sandwich-3-slice": "golden-grilled-veggie-cheese-sandwich",
    "sandwich__sp-paneer-cheese-grill-sandwich-2-slice": "golden-paneer-cheese-grill-sandwich",
    "sandwich__sp-paneer-cheese-grill-sandwich-3-slice": "golden-paneer-cheese-grill-sandwich",
    "sandwich__sp-mayo-cheese-grill-sandwich-2-slice": "golden-mayo-cheese-grill-sandwich",
    "sandwich__sp-mayo-cheese-grill-sandwich-3-slice": "golden-mayo-cheese-grill-sandwich",
    "sandwich__cheese-burst-sandwich-2-slice": "golden-molten-cheese-sandwich",
    "sandwich__cheese-burst-sandwich-3-slice": "golden-molten-cheese-sandwich",
    "sandwich__sp-cheese-corn-sandwich-2-slice": "golden-grilled-cheese-corn-sandwich",
    "sandwich__sp-cheese-corn-sandwich-3-slice": "golden-grilled-cheese-corn-sandwich",
    "sandwich__sp-mexican-cheese-sandwich-2-slice": "golden-grilled-mexican-cheese-sandwich",
    "sandwich__sp-mexican-cheese-sandwich-3-slice": "golden-grilled-mexican-cheese-sandwich",
    "bread-butter__bread-butter-grill-simple": "golden-butter-grilled-bread-triangles",
    "bread-butter__bread-butter-chatni-simple": "buttery-green-chutney-bread-sandwich",
    "bread-butter__bread-butter-cheese-simple": "simple-bread-butter-cheese-sandwich",
    "bread-butter__bread-butter-jam-butter": "street-style-jam-butter-bread",
    "combos__veg-cheese-burger-coke-french-fries-r": "veggie-cheese-burger-with-fries-and-cola",
    "combos__cheese-burst-burger-coke-french-fries-r": "cheesy-veg-burger-with-fries-and-cola",
    "combos__sp-dd-burger-coke-french-fries-r": "paneer-burger-combo-with-fries-and-cola",
    "mayo-pav__sp-butter-pav-simple": "soft-golden-butter-pav-rolls",
    "mayo-pav__sp-amul-butter-pav": "golden-butter-toasted-vadapav",
    "mayo-pav__sp-mayo-pav": "toasted-corn-puff-mayo-pav",
    "mayo-pav__sp-mayo-wafer": "crisp-golden-potato-wafers",
    "mayo-pav__sp-cheese-mayo-wafer": "crispy-cheese-mayo-potato-wafers",
    "mayo-pav__masala-pav-simple": "simple-griddled-masala-pav",
    "mayo-pav__sp-solid-masti-mayo-pav": "creamy-mayo-pav-with-cabbage",
    "mayo-pav__sp-masala-pav": "griddled-masala-pav-with-peanut-crunch",
    "pav-bhaji__sp-dabeli-pavbhaji": "street-style-dabeli-bhaji-with-toasted-pav",
    "pav-bhaji__sp-paneer-pavbhaji": "paneer-pav-bhaji-with-buttered-pav",
    "pav-bhaji__sp-solid-masti": "simple-griddled-masala-pav",
    "pav-bhaji__sp-peri-peri-solid-masti": "creamy-peri-peri-pasta-pav",
    "pav-bhaji__sp-paneer-solid-masti": "creamy-paneer-pasta-pav",
}


def family_images(category_name, image_names):
    patterns = IMAGE_FAMILY_PATTERNS.get(category_name, ())
    candidates = [
        image_name for image_name in image_names
        if any(pattern in image_name for pattern in patterns)
    ]
    if category_name == "Mayo Pav":
        candidates = [
            image_name for image_name in candidates
            if not any(token in image_name for token in ("vada", "vadapav", "burger", "frankie"))
        ]
    return candidates


class Command(BaseCommand):
    help = "Replace the live menu with the verified priced catalog and static menu images."

    def handle(self, *args, **options):
        base_dir = Path(__file__).resolve().parents[2]
        data_path = base_dir / "menu_assets" / "menu.json"
        image_dir = base_dir / "static" / "menu_assets"

        with data_path.open(encoding="utf-8") as menu_file:
            records = json.load(menu_file)["items"]

        records = [record for record in records if record.get("price") is not None]
        # image-2.jpg is a screenshot accidentally included in the source zip,
        # not a food photo; never allow it to be selected for a menu item.
        image_names = sorted(
            path.stem for path in image_dir.glob("*.jpg") if path.stem != "image-2"
        )
        if not records:
            raise RuntimeError("The menu asset catalog contains no priced items")

        with transaction.atomic():
            MenuItem.objects.all().delete()
            Category.objects.all().delete()
            categories = {}
            used_images = set()

            for record in records:
                category_name = record["category"].strip()
                if category_name not in categories:
                    categories[category_name] = Category.objects.create(name=category_name)
                category = categories[category_name]
                image_name = IMAGE_OVERRIDES.get(record["id"])
                if image_name not in image_names:
                    category_images = family_images(category_name, image_names)
                    ranked_images = sorted(
                        category_images or image_names,
                        key=lambda candidate: image_score(record["name"], category_name, candidate),
                        reverse=True,
                    )
                    image_name = next((name for name in ranked_images if name not in used_images), None)
                    # Reuse a relevant family image when the supplied library
                    # has fewer variants than the printed menu, rather than
                    # assigning an unrelated food photo.
                    if image_name is None and ranked_images:
                        image_name = ranked_images[0]
                if image_name:
                    used_images.add(image_name)

                MenuItem.objects.create(
                    category=category,
                    name=record["name"].strip(),
                    description=f"Freshly prepared {record['name'].strip()} from Dinesh Dabeli.",
                    price=Decimal(str(record["price"])),
                    image_url=f"/static/menu_assets/{image_name}.jpg" if image_name else "",
                    is_available=True,
                )

        self.stdout.write(self.style.SUCCESS(
            f"Imported {len(records)} priced menu items across {len(categories)} categories with {len(used_images)} images."
        ))
