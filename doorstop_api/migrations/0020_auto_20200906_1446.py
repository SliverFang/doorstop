# Generated by Django 2.2 on 2020-09-06 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doorstop_api', '0019_auto_20200906_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resturantfood',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
