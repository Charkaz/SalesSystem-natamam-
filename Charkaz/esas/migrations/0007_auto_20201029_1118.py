# Generated by Django 3.1.2 on 2020-10-29 11:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('esas', '0006_auto_20201029_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mehsul',
            name='kateqoriya',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='esas.mehsulkat', unique=True),
        ),
    ]
