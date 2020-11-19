# Generated by Django 3.1.2 on 2020-11-09 18:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('esas', '0018_auto_20201109_1728'),
    ]

    operations = [
        migrations.AddField(
            model_name='qaime',
            name='musteri',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='esas.musteri'),
        ),
        migrations.AddField(
            model_name='qaime',
            name='useri',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='satis',
            name='useri',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]