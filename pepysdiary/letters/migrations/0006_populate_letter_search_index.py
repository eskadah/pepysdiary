# Generated by Django 2.1.7 on 2019-03-23 16:29

from django.db import migrations
from django.contrib.postgres.search import SearchVector


def populate_search_index(apps, schema_editor):
    Letter = apps.get_model('letters', 'Letter')

    Letter.objects.update(
        search_document=(
            SearchVector('title', weight='A') \
            + SearchVector('text', weight='B') \
            + SearchVector('footnotes', weight='C')
        )
    )


class Migration(migrations.Migration):

    dependencies = [
        ('letters', '0005_auto_20190323_1625'),
    ]

    operations = [
        migrations.RunPython(populate_search_index, reverse_code=migrations.RunPython.noop),
    ]
