# Generated by Django 5.1.2 on 2024-10-31 06:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemontool', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pokemoncard',
            old_name='card_image',
            new_name='image',
        ),
    ]
