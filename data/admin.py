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
       pass
admin.site.register(Contrat,ContrattAdmin) 

########
class OccupantAdmin(ImportExportModelAdmin, admin.ModelAdmin):
       pass
admin.site.register(Occupant,OccupantAdmin) 
######
class LogementAdmin(ImportExportModelAdmin, admin.ModelAdmin):
       pass
admin.site.register(Logement,LogementAdmin) 

######
class ConsultationAdmin(ImportExportModelAdmin, admin.ModelAdmin):
       pass
admin.site.register(Consultation,ConsultationAdmin) 
######

class WilayaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
       pass

admin.site.register(wilaya,WilayaAdmin) 
####


