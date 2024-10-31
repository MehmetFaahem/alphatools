from django.urls import path
from . import views

urlpatterns = [
    path('generate-card/', views.generate_card, name='generate_card'),
    path('card-generated/', views.card_generated, name='card_generated'),
]
