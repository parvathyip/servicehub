# Generated by Django 4.2.2 on 2023-08-11 10:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('servicehub_app', '0003_rename_servicehub_complaint_hub_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='complaint',
            name='expected_returndate',
        ),
    ]
