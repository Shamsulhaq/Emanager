# Generated by Django 2.2.6 on 2019-10-29 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0003_skill'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='skill',
            options={'ordering': ['-timestamp']},
        ),
    ]