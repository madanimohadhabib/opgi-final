from django.contrib import admin
from .models import *
from django.db.models import Count
from django.db.models.functions import TruncDate
from import_export.admin import ImportExportModelAdmin



 

    

class CiteAdmin(ImportExportModelAdmin, admin.ModelAdmin):
       pass
admin.site.register(Cite,CiteAdmin)

#####

class BatimentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
       pass
admin.site.register(Batiment,BatimentAdmin) 

####
class ContrattAdmin(ImportExportModelAdmin, admin.ModelAdmin):
       list_display = (
        'date_cnt',
        'date_strt_loyer',
        'loyer',
        'charge',
        'mnt_tva',
        'total_of_month',
        'occupant',
    )

       list_filter = ('date_cnt', 'date_strt_loyer', 'occupant')
admin.site.register(Contrat,ContrattAdmin) 

########
class OccupantAdmin(ImportExportModelAdmin, admin.ModelAdmin):
       list_display = (
        'oc_id',
        'nom_oc',
        'prenom_oc',
        'date_naiss',
        'lieu_naiss',
        'created_at',
    )
       list_filter = ('date_naiss', 'created_at')
       date_hierarchy = 'created_at'
admin.site.register(Occupant,OccupantAdmin) 
######
class LogementAdmin(ImportExportModelAdmin, admin.ModelAdmin):
       list_display = (
        'surface',
        'prix_logement',
        'type_logement',
        'created_at',
        'batiment',
        'contrat',
    )
       list_filter = ('created_at', 'batiment', 'contrat')
       date_hierarchy = 'created_at'
admin.site.register(Logement,LogementAdmin) 

######
class ConsultationAdmin(ImportExportModelAdmin, admin.ModelAdmin):
        list_display = (
        'mois',
        'created_at',
        'total',
        'logement',
        'occupant',
        'unite',
    )
        list_filter = ('created_at', 'logement', 'occupant', 'unite')
        date_hierarchy = 'created_at'
admin.site.register(Consultation,ConsultationAdmin) 
######

class WilayaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('lib_wilaya', 'date_joined')
    list_filter = ('date_joined',)

admin.site.register(wilaya,WilayaAdmin) 
####


