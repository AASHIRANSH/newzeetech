# Generated by Django 4.2.1 on 2023-08-13 07:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spa', '0005_sale_grand_total'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sale',
            old_name='final',
            new_name='despatched',
        ),
    ]
