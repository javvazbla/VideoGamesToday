# Generated by Django 3.0.5 on 2020-05-05 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_noticia'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='noticia',
            name='plataforma',
        ),
        migrations.AddField(
            model_name='noticia',
            name='plataforma',
            field=models.ManyToManyField(to='main.Plataforma'),
        ),
    ]