# Merge migration for the two app 0008 leaves.
# The CMS schema/data cleanup lives in 0008_adminpage_pageblock_delete_aboutacademy_and_more.
# This file only joins that migration with the main-branch 0008 migration so Django has a single leaf.

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_adminpage_pageblock_delete_aboutacademy_and_more'),
        ('app', '0008_alter_aboutacademy_additional_description_and_more'),
    ]

    operations = []
