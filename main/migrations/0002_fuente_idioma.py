# Generated by Django 3.0.5 on 2020-05-05 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fuente',
            name='idioma',
            field=models.CharField(default='esp', max_length=3, verbose_name='Idioma'),
            preserve_default=False,
        ),
    ]