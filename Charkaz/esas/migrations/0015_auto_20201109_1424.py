# Generated by Django 3.1.2 on 2020-11-09 14:24

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('esas', '0014_auto_20201109_1357'),
    ]

    operations = [
        migrations.CreateModel(
            name='qaime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aciqlama', models.CharField(blank=True, max_length=250, null=True)),
                ('toplam_tutar', models.FloatField(null=True)),
                ('toplam_endrim', models.FloatField(null=True)),
                ('son_odenis_tarixi', models.DateField()),
                ('tarix', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='satis',
            name='Qaime',
        ),
        migrations.AddField(
            model_name='satis',
            name='tarix',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='satis',
            name='s_qaime',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='esas.qaime'),
        ),
    ]
