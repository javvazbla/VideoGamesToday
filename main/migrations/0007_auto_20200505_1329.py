# Generated by Django 3.0.5 on 2020-05-05 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20200505_1323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticia',
            name='plataforma',
            field=models.ManyToManyField(blank=True, to='main.Plataforma'),
        ),
    ]