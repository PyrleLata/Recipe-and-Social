# Generated by Django 3.2.3 on 2021-06-11 17:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipeandsocial_app', '0002_comment_recipe'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='recipe',
        ),
    ]
