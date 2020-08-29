# Generated by Django 2.2 on 2020-08-28 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doorstop_api', '0008_auto_20200828_0833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]