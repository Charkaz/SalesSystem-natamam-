# Generated by Django 3.1.2 on 2020-11-13 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('esas', '0022_remove_satis_tutar'),
    ]

    operations = [
        migrations.AddField(
            model_name='qaime',
            name='odenis',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
