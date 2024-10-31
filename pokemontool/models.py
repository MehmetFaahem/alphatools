from django.db import models
from django.utils import timezone
class PokemonCard(models.Model):
    TYPE_CHOICES = [
        ('electric', 'Electric'),
        ('fighting', 'Fighting'),
        ('fire', 'Fire'),
        ('grass', 'Grass'),
        ('normal', 'Normal'),
        ('psychic', 'Psychic'),
        ('water', 'Water'),
    ]
    
    # General Information
    name = models.CharField(max_length=100, blank=True, null=True, default='')
    hp = models.IntegerField(blank=True, null=True, default=0)
    image = models.ImageField(upload_to='images/', blank=True, null=True, default=None)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, blank=True, null=True, default='normal')
    specialty = models.CharField(max_length=100, blank=True, null=True, default='')
    length = models.CharField(max_length=50, blank=True, null=True, default='')
    weight = models.CharField(max_length=50, blank=True, null=True, default='')

    # Evolution Information
    evolution_stage = models.CharField(max_length=50, blank=True, null=True, default='')
    evolution_name = models.CharField(max_length=100, blank=True, null=True, default='')
    evolution_photo = models.ImageField(upload_to='evolutions/', blank=True, null=True, default=None)

    # Attack Information
    attack1_name = models.CharField(max_length=100, blank=True, null=True, default='')
    attack1_damage = models.IntegerField(blank=True, null=True, default=0)
    attack1_info = models.TextField(blank=True, null=True, default='')
    attack1_amount = models.IntegerField(blank=True, null=True, default=0)
    attack1_type = models.CharField(max_length=50, blank=True, null=True, default='')

    attack2_name = models.CharField(max_length=100, blank=True, null=True, default='')
    attack2_damage = models.IntegerField(blank=True, null=True, default=0)
    attack2_info = models.TextField(blank=True, null=True, default='')
    attack2_amount = models.IntegerField(blank=True, null=True, default=0)
    attack2_type = models.CharField(max_length=50, blank=True, null=True, default='')

    # Weakness and Resistance
    weakness_element = models.CharField(max_length=50, blank=True, null=True, default='')
    weakness_amount = models.IntegerField(blank=True, null=True, default=0)
    resistance_element = models.CharField(max_length=50, blank=True, null=True, default='')
    resistance_amount = models.IntegerField(blank=True, null=True, default=0)

    # Retreat Cost
    retreat_cost = models.IntegerField(blank=True, null=True, default=0)

    # Card Footer
    description = models.TextField(blank=True, null=True, default='')
    illustrator = models.CharField(max_length=100, blank=True, null=True, default='')
    collection_number = models.CharField(max_length=10, blank=True, null=True, default='')
    rarity = models.CharField(max_length=50, blank=True, null=True, default='')
    created_at = models.DateTimeField(blank=True, null=True, default=timezone.now)

    def __str__(self):
        return self.name
