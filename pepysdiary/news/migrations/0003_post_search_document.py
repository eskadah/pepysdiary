# Generated by Django 2.1.7 on 2019-04-06 16:32

import django.contrib.postgres.search
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_auto_20180115_1635'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='search_document',
            field=django.contrib.postgres.search.SearchVectorField(null=True),
        ),
    ]