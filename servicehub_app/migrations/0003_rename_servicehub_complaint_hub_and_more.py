# Generated by Django 4.2.2 on 2023-08-11 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servicehub_app', '0002_brand_complaint_servicehubreg_userreg_troubleshoot_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='complaint',
            old_name='servicehub',
            new_name='hub',
        ),
        migrations.RenameField(
            model_name='faq',
            old_name='servicehub',
            new_name='hub',
        ),
        migrations.RenameField(
            model_name='feedback',
            old_name='servicehub',
            new_name='hub',
        ),
        migrations.RenameField(
            model_name='servicehubreg',
            old_name='srvicehub_login',
            new_name='hub_login',
        ),
        migrations.RenameField(
            model_name='serviceproducts',
            old_name='servicehub',
            new_name='hub',
        ),
        migrations.RenameField(
            model_name='troubleshoot',
            old_name='servicehub',
            new_name='hub',
        ),
        migrations.AddField(
            model_name='servicehubreg',
            name='hub_email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='servicehubreg',
            name='hub_name',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='servicehubreg',
            name='hub_phone',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='servicehubreg',
            name='hub_pin',
            field=models.CharField(max_length=30, null=True),
        ),
    ]