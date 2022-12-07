# Generated by Django 4.1.1 on 2022-12-07 19:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('track', '0003_project_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to=settings.AUTH_USER_MODEL),
        ),
    ]