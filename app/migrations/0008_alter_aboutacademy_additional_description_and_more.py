# Placeholder merge-compatible migration.
# The production/main branch already contains a migration with this name.
# Keeping this no-op locally lets the CMS cleanup migration depend on that leaf
# and removes the multiple-0008 leaf conflict when the branches are combined.

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_announcement_date_alter_contact_map_url_and_more'),
    ]

    operations = []
