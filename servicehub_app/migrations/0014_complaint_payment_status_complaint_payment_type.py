# Generated by Django 4.2.2 on 2023-08-13 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicehub_app', '0013_complaint_completed_on_complaint_paid_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='payment_status',
            field=models.CharField(default='Unpaid', max_length=30),
        ),
        migrations.AddField(
            model_name='complaint',
            name='payment_type',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
