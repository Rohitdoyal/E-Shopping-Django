# Generated by Django 3.0.5 on 2021-07-17 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20210717_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='', null=True, upload_to='static/images'),
        ),
    ]
