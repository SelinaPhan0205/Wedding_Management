# Generated by Django 5.2.1 on 2025-07-06 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_hoadon_tien_phat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hoadon',
            name='trang_thai',
            field=models.CharField(choices=[('Chưa thanh toán', 'Chưa thanh toán'), ('Đã thanh toán', 'Đã thanh toán')], default='Chưa thanh toán', max_length=30),
        ),
    ]
