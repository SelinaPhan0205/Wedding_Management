# Generated by Django 5.2.1 on 2025-06-07 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dichvu',
            name='ten_dich_vu',
            field=models.CharField(max_length=255),
        ),
    ]
