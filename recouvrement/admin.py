from django.contrib import admin
from .models import *
from dal import autocomplete
from data.models import *
from django.forms import TextInput





@admin.register(Unite)

class UniteAdmin(admin.ModelAdmin):
    search_fields = ['lib_unit']

@admin.register(MontantMensuel)

class MontantMensuelAdmin(admin.ModelAdmin):
    list_display = ('unite', 'mois', 'annee', 'total', 'total_of_month')
    list_filter = ['mois', 'annee']
    search_fields = ('unite__lib_unit__icontains',)
    form = autocomplete.FutureModelForm
    autocomplete_fields = ['unite']



admin.site.register(Notification_chef_service)
