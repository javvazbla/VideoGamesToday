# Generated by Django 3.2 on 2021-04-29 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_alter_actualizacion_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fuente',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='noticia',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='plataforma',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
