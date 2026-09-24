from django.core.management import call_command
from django.db import migrations


def refresh_menu_asset_urls(apps, schema_editor):
    # Rebuild the catalog so existing rows point at the URL-safe filenames
    # shipped with this release.  This runs during deploy, before requests.
    call_command("import_menu_assets", verbosity=0)


class Migration(migrations.Migration):
    dependencies = [
        ("dabeli", "0014_import_menu_assets"),
    ]

    operations = [
        migrations.RunPython(refresh_menu_asset_urls, migrations.RunPython.noop),
    ]
