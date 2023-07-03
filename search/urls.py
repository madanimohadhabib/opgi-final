from django.urls import path
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from .views import *
from search.views import *


app_name = 'search'

urlpatterns = [
    path('', recherche, name='recherche'),
    path('occupant_detail/<int:pk>/', occupant_detail, name='occupant_detail'),
    path('get_batiments/', get_batiments, name='get_batiments'),
    path('get_cites/', get_cites, name='get_cites'),

]