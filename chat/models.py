from django.db import models

# Create your models here.
from django.db import models
import string
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import channels.layers
from django.dispatch import receiver
from asgiref.sync import async_to_sync
import json
import random
from channels.layers import get_channel_layer
from data.models import * 
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Create your models here.


class Service_contentieux_settings(models.Model):
     montant_fix_par_opgi=models.FloatField()
     
   
    
     
class Notification(models.Model):
    message = models.CharField(max_length=255)
    nom_oc = models.CharField(max_length=255)
    prenom_oc = models.CharField(max_length=120)

    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

  
        
    def __str__(self):
        return self.message
   
    
class Service_contentieux_dossier(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('terminer', 'Terminer'),
    )
    created_by = models.CharField(max_length=255)
    dossier = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)


class Service_contentieux_dossier_archive(models.Model):
         dossier = models.CharField(max_length=255)
         created_by = models.CharField(max_length=255)
         created_at = models.DateTimeField(auto_now_add=True)



@receiver(post_save, sender=Notification)
def send_notification(sender, instance, **kwargs):
 if instance:
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notifications",
        {
            "type": "send_notification",
            "data": {
                "message": instance.message,
                "created_at": instance.created_at.isoformat(),
            },
        },
    )


@receiver(post_save, sender=Consultation)
def my_model_post_save(sender, instance, created, **kwargs):
 now = datetime.now()
 service_settings = Service_contentieux_settings.objects.first()
 montant_fix_par_opgi = service_settings.montant_fix_par_opgi

 if created:
   # Get the current date and time

# Iterate over all Contrat objects
  for contrat in Contrat.objects.all():

    # Calculate the number of months since date_strt_loyer for this Contrat
    if contrat.date_strt_loyer is not None:
        months = (now.year - contrat.date_strt_loyer.year) * 12 + (now.month - contrat.date_strt_loyer.month)
    else:
        months = 0
    
    # Calculate the total difference between the number of months and the mois field for all associated Consultation objects
    consultation_months_sum = 0

    px=0
    for consultation in Consultation.objects.filter(occupant=contrat.occupant):
        consultation_months_sum += consultation.mois
    px = (  months - consultation_months_sum ) * contrat.total_of_month >= Service_contentieux_settings.objects.get().montant_fix_par_opgi
    if px:
          instances = []

          print("px is True",(  months - consultation_months_sum ) * contrat.total_of_month)
        # Display the occupant name if px is True
          print("Occupant name:", contrat.occupant.nom_oc)
          print("Number of months since date_strt_loyer:", months)
          print("Total difference between months and mois for associated Consultation objects:", consultation_months_sum)
          if not Notification.objects.filter(message=contrat.occupant.oc_id, read=False).exists() and not Service_contentieux_dossier.objects.filter(dossier=contrat.occupant.oc_id).exists():
            instances.append(Notification(message=contrat.occupant.oc_id,nom_oc=contrat.occupant.nom_oc,prenom_oc=contrat.occupant.prenom_oc))
            if instances:
                Notification.objects.bulk_create(instances)
            else:
                print("No instances created.")
          elif Notification.objects.filter(message=contrat.occupant.oc_id, read=False).exists() and Service_contentieux_dossier.objects.filter(dossier=contrat.occupant.oc_id, status='terminer').exists():
                    instances.append(Notification(message=contrat.occupant.oc_id,nom_oc=contrat.occupant.nom_oc,prenom_oc=contrat.occupant.prenom_oc))
                    if instances:
                        Notification.objects.bulk_create(instances)
                    else:
                       print("No instances created.")
        
    else:
        print("px is False",(  months - consultation_months_sum ) * contrat.total_of_month)
        print("Number of months since date_strt_loyer:", months)
        print("Total difference between months and mois for associated Consultation objects:", consultation_months_sum)
    # Print the results for this Contrat and display px
   