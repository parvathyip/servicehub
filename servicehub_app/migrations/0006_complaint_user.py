# Generated by Django 4.2.2 on 2023-08-12 05:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('servicehub_app', '0005_userreg_first_name_userreg_last_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='servicehub_app.userreg'),
        ),
    ]