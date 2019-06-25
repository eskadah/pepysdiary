# Generated by Django 2.1.8 on 2019-05-11 16:52

from django.db import migrations
from django.contrib.postgres.search import SearchVector


def populate_search_index(apps, schema_editor):
    Annotation = apps.get_model("annotations", "Annotation")

    Annotation.objects.update(search_document=(SearchVector("comment", weight="A")))


class Migration(migrations.Migration):

    dependencies = [("annotations", "0005_auto_20190511_1651")]

    operations = [
        migrations.RunPython(
            populate_search_index, reverse_code=migrations.RunPython.noop
        )
    ]
