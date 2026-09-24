import os

from django import template
from django.utils.text import slugify


register = template.Library()


CATEGORY_NAME_OVERRIDES = {
    ("Frankie", "Cheese Frankie"): "cheesy-street-style-frankie-wrap",
    ("Frankie", "Mayo Frankie"): "creamy-mayo-frankie-wrap-cut-open",
    ("Frankie", "Cheese Mayo Frankie"): "street-style-cheesy-mayo-frankie",
    ("Dabeli", "Sp. Masala Dabeli"): "cheesy-gujarati-dabeli-on-steel-plate",
    ("Dabeli", "Sp. Delicious Sev Dabeli"): "gujarati-sev-dabeli-with-pomegranate",
    ("Dabeli", "Sp. Amul Butter Masala Dabeli"): "buttery-gujarati-dabeli-with-sev",
    ("Dabeli", "Sp. Mayo Dabeli"): "golden-toasted-dabeli-with-creamy-mayo",
    ("Dabeli", "Sp. Amul Butter Mayo Dabeli"): "creamy-gujarati-mayo-dabeli",
    ("Dabeli", "Sp. Amul Cheese Dabeli"): "cheesy-street-style-gujarati-dabeli",
    ("Dabeli", "Sp. Cheese Masala Dabeli"): "cheesy-gujarati-dabeli-on-steel-plate",
    ("Pavbhaji", "Sp. Dabeli Pavbhaji"): "street-style-dabeli-bhaji-with-toasted-pav",
    ("Pavbhaji", "Sp. Paneer Pavbhaji"): "paneer-pav-bhaji-with-buttered-pav",
    ("Pavbhaji", "Sp. Solid Masti"): "simple-griddled-masala-pav",
    ("Pavbhaji", "Sp. Peri Peri Solid Masti"): "creamy-peri-peri-pasta-pav",
    ("Pavbhaji", "Sp. Paneer Solid Masti"): "creamy-paneer-pasta-pav",
    ("Mayo Pav", "Sp. Butter Pav (Simple)"): "soft-golden-butter-pav-rolls",
    ("Mayo Pav", "Sp. Amul Butter Pav"): "golden-butter-toasted-vadapav",
    ("Mayo Pav", "Sp. Mayo Pav"): "toasted-corn-puff-mayo-pav",
    ("Mayo Pav", "Sp. Mayo Wafer"): "crisp-golden-potato-wafers",
    ("Mayo Pav", "Sp. Cheese Mayo Wafer"): "crispy-cheese-mayo-potato-wafers",
    ("Mayo Pav", "Masala Pav (Simple)"): "simple-griddled-masala-pav",
    ("Mayo Pav", "Sp. Solid Masti Mayo Pav"): "creamy-mayo-pav-with-cabbage",
    ("Mayo Pav", "Sp. Masala Pav"): "griddled-masala-pav-with-peanut-crunch",
    ("Grill Sandwich", "Veggies Cheese Grill Sandwich"): "golden-grilled-veggie-cheese-sandwich",
    ("Grill Sandwich", "Sp. Paneer Cheese Grill Sandwich"): "golden-paneer-cheese-grill-sandwich",
    ("Grill Sandwich", "Sp. Mayo Cheese Grill Sandwich"): "golden-mayo-cheese-grill-sandwich",
    ("Grill Sandwich", "Cheese Burst Sandwich"): "golden-molten-cheese-sandwich",
    ("Grill Sandwich", "Sp. Cheese Corn Sandwich"): "golden-grilled-cheese-corn-sandwich",
    ("Grill Sandwich", "Sp. Mexican Cheese Sandwich"): "golden-grilled-mexican-cheese-sandwich",
    ("Bread Butter", "Bread Butter Grill (Simple)"): "golden-butter-grilled-bread-triangles",
    ("Bread Butter", "Bread Butter Chatni (Simple)"): "buttery-green-chutney-bread-sandwich",
    ("Bread Butter", "Bread Butter Cheese (Simple)"): "simple-bread-butter-cheese-sandwich",
    ("Bread Butter", "Bread Butter (Jam Butter)"): "street-style-jam-butter-bread",
    ("Special Combo", "Veg Cheese Burger + Coke + French Fries (R)"): "veggie-cheese-burger-with-fries-and-cola",
    ("Special Combo", "Cheese Burst Burger + Coke + French Fries (R)"): "cheesy-veg-burger-with-fries-and-cola",
    ("Special Combo", "Sp. DD Burger + Coke + French Fries (R)"): "paneer-burger-combo-with-fries-and-cola",
}


@register.filter
def menu_image_url(value):
    """Return the canonical URL for both legacy and current menu records."""
    if not value:
        return ""

    if hasattr(value, "category") and hasattr(value, "name"):
        override = CATEGORY_NAME_OVERRIDES.get((str(value.category.name), str(value.name)))
        if override:
            return f"/static/menu_assets/{override}.jpg"
        value = getattr(value, "image_url", "")

    filename = str(value).split("?", 1)[0].rsplit("/", 1)[-1]
    stem, _extension = os.path.splitext(filename)
    return f"/static/menu_assets/{slugify(stem)}.jpg"
