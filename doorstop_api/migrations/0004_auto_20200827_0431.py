# Generated by Django 2.2 on 2020-08-27 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doorstop_api', '0003_auto_20200827_0425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]