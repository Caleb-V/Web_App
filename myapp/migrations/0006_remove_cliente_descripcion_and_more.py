# Generated by Django 5.2.1 on 2025-05-23 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_alter_plato_estado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='descripcion',
        ),
        migrations.AddField(
            model_name='cliente',
            name='direccion_particular',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='es_particular',
            field=models.BooleanField(default=False),
        ),
    ]
