# Generated by Django 2.0.1 on 2018-01-15 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20160329_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='config',
            name='registration_answer',
            field=models.CharField(blank=True, default='', help_text='Not case-sensitive.', max_length=255),
        ),
        migrations.AlterField(
            model_name='config',
            name='registration_question',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='config',
            name='use_registration_captcha',
            field=models.BooleanField(default=False, help_text='If checked, people must complete a Captcha field when registering.'),
        ),
        migrations.AlterField(
            model_name='config',
            name='use_registration_question',
            field=models.BooleanField(default=False, help_text='If checked, people must successfully answer the question below when registering.'),
        ),
    ]
