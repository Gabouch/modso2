# Generated by Django 2.2 on 2019-04-17 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionMachines', '0005_machine_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machine',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='machines'),
        ),
    ]