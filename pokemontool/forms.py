from django import forms
from .models import PokemonCard

class PokemonCardForm(forms.ModelForm):
    class Meta:
        model = PokemonCard
        fields = ['name','image', 'hp', 'type', 'specialty', 'length', 'weight', 'evolution_stage', 'evolution_name', 
                  'evolution_photo', 'attack1_name', 'attack1_damage', 'attack1_info', 'attack1_amount', 
                  'attack1_type', 'attack2_name', 'attack2_damage', 'attack2_info', 'attack2_amount', 
                  'attack2_type', 'weakness_element', 'weakness_amount', 'resistance_element', 
                  'resistance_amount', 'retreat_cost', 'description', 'illustrator', 'collection_number', 'rarity' ]
        widgets = {
            'type': forms.Select(attrs={'class': 'form-select'})
        }
