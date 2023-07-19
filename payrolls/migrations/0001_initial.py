# Generated by Django 4.2.1 on 2023-07-19 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=50)),
                ('salary', models.IntegerField(default=0)),
                ('address', models.CharField(max_length=150)),
                ('date_joined', models.DateField()),
                ('date_resigned', models.DateField()),
            ],
        ),
    ]
