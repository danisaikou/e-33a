# Generated by Django 3.1.7 on 2022-12-12 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('track', '0014_auto_20221211_1905'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='customer_address1',
            new_name='customer_address',
        ),
        migrations.AlterField(
            model_name='project',
            name='invoice_status',
            field=models.CharField(choices=[('pending', 'pending'), ('paid', 'paid'), ('credit_memo', 'credit_memo')], default='pending', max_length=25),
        ),
        migrations.AlterField(
            model_name='projecttask',
            name='status',
            field=models.CharField(choices=[('todo', 'todo'), ('complete', 'complete'), ('canceled', 'canceled')], default='todo', max_length=25),
        ),
    ]