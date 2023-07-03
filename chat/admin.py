from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Notification)
admin.site.register(Service_contentieux_settings)

admin.site.register(Service_contentieux_dossier)
admin.site.register(Service_contentieux_dossier_archive)
