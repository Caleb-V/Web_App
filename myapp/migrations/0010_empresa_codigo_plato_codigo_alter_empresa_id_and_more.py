# Generated by Django 5.2.1 on 2025-05-23 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_alter_empresa_cif'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='codigo',
            field=models.CharField(default='codigo123', max_length=50, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='plato',
            name='codigo',
            field=models.CharField(default='codigo123', max_length=50, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='empresa',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='plato',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
