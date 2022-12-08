# Generated by Django 4.1.1 on 2022-12-08 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('track', '0002_alter_projecttask_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projecttask',
            name='status',
            field=models.CharField(choices=[('complete', 'complete'), ('canceled', 'canceled'), ('todo', 'todo')], default='todo', max_length=25),
        ),
    ]