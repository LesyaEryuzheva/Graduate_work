# Generated by Django 4.1.1 on 2022-10-01 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_wallet', '0006_transfer_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='title',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
