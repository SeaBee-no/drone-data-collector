from django.urls import path

from .views import *

urlpatterns = [
path('', home, name='home'),
path('about', about, name='about'),
path('services', team, name='team'),
path('toolbox', toolbox, name='toolbox'),
path('geoviz', geoviz, name='geoviz'),
path('contact', contact, name='contact'),
path('disclaimer', disclaimer, name='disclaimer'),
 path('profile', ProfileCreate.as_view(), name='profileAdd'),
 path('profile/<int:pk>/', ProfileUpdate.as_view(), name='profileUpdate'),
]
