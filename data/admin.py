from django.contrib import admin
from .models import *
from django.db.models import Count
from django.db.models.functions import TruncDate






admin.site.register(wilaya) 

admin.site.register(Cite) 
admin.site.register(Batiment) 
admin.site.register(Contrat) 
admin.site.register(Occupant) 
admin.site.register(Logement) 
admin.site.register(Consultation) 