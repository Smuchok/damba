# Generated by Django 3.2.7 on 2021-10-24 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20211024_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='price',
            name='photo',
            field=models.ImageField(blank=True, upload_to='photos/%Y/%m/%d'),
        ),
    ]
