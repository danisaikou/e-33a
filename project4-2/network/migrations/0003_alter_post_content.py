# Generated by Django 4.1.1 on 2022-11-14 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_post_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.CharField(max_length=260, verbose_name='content'),
        ),
    ]
