from django.core.management import call_command
from django.db import migrations


def rebuild_menu_image_mapping(apps, schema_editor):
    # Reapply the category-aware/explicit mapping to databases that already
    # ran the initial catalog import migration.
    call_command("import_menu_assets", verbosity=0)


class Migration(migrations.Migration):
    dependencies = [
        ("dabeli", "0015_refresh_menu_asset_urls"),
    ]

    operations = [
        migrations.RunPython(rebuild_menu_image_mapping, migrations.RunPython.noop),
    ]
