# Generated by Django 4.2.2 on 2023-08-20 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicehub_app', '0020_remove_serviceproducts_hub_serviceproducts_hubbrands'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='submitdate',
            field=models.DateField(null=True),
        ),
    ]
