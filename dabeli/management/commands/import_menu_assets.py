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
    value = value.lower().replace("vadapav", "vada pav")
    return {token for token in re.findall(r"[a-z]+", value) if token not in STOP_WORDS}


def image_score(item_name, category_name, image_name):
    item_tokens = tokens(item_name) | tokens(category_name)
    image_tokens = tokens(image_name)
    overlap = len(item_tokens & image_tokens)
    category_match = 1 if tokens(category_name) & image_tokens else 0
    similarity = SequenceMatcher(None, item_name.lower(), image_name.lower()).ratio()
    return overlap * 3 + category_match + similarity


class Command(BaseCommand):
    help = "Replace the live menu with the verified priced catalog and static menu images."

    def handle(self, *args, **options):
        base_dir = Path(__file__).resolve().parents[2]
        data_path = base_dir / "menu_assets" / "menu.json"
        image_dir = base_dir / "static" / "menu_assets"

        with data_path.open(encoding="utf-8") as menu_file:
            records = json.load(menu_file)["items"]

        records = [record for record in records if record.get("price") is not None]
        image_names = sorted(path.stem for path in image_dir.glob("*.jpg"))
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
                ranked_images = sorted(
                    image_names,
                    key=lambda image_name: image_score(record["name"], category_name, image_name),
                    reverse=True,
                )
                image_name = next((name for name in ranked_images if name not in used_images), None)
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
