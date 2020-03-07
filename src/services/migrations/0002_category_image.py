# Generated by Django 2.2.6 on 2019-10-29 15:55

from django.db import migrations, models
import services.models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, upload_to=services.models.upload_category_image_path),
        ),
    ]
