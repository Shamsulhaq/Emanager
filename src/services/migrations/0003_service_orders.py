# Generated by Django 2.2.6 on 2019-11-01 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_category_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='orders',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=9),
        ),
    ]
