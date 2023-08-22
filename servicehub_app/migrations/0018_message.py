# Generated by Django 4.2.2 on 2023-08-16 05:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('servicehub_app', '0017_alter_complaint_feedback_desc_alter_complaint_rating'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=30, null=True)),
                ('sendby', models.CharField(default='admin', max_length=30, null=True)),
                ('chatdate', models.DateTimeField(null=True)),
                ('hub', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='servicehub_app.servicehubreg')),
            ],
        ),
    ]
