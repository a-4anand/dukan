from django.core.management import call_command
from django.db import migrations


def import_menu_catalog(apps, schema_editor):
    call_command('import_menu_assets', verbosity=0)


class Migration(migrations.Migration):
    dependencies = [
        ('dabeli', '0013_franchiseinquiry_locality'),
    ]

    operations = [
        migrations.RunPython(import_menu_catalog, migrations.RunPython.noop),
    ]
