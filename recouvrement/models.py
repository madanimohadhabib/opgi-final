from django.db import models
from data.models import * 
from django.db import models
import string
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import channels.layers
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from django.db.models import Sum
from datetime import datetime
from django.db.models import Sum
from django.utils import timezone
from data.models import Consultation, Unite
import calendar
from datetime import datetime, date, timedelta
from django.core.validators import MinValueValidator, RegexValidator
from django.core.exceptions import ValidationError

# Create your models here.
class MontantMensuel(models.Model):
    unite = models.ForeignKey(Unite, on_delete=models.SET)
    mois = models.PositiveIntegerField()
    annee = models.PositiveIntegerField()
    total = models.FloatField(default=100, validators=[MinValueValidator(0, message="La valeur doit être supérieure ou égale à 0")])
    total_of_month = models.FloatField(default=0, validators=[MinValueValidator(0, message="La valeur doit être supérieure ou égale à 0")])

    def clean(self):
        if self.total <= self.total_of_month:
            raise ValidationError("Le total doit être supérieur à total_of_month.")

    def __str__(self):
        return f"MontantMensuel {self.unite.lib_unit} - {self.mois}/{self.annee}"
    
    class Meta:
      
        unique_together = ('unite','annee', 'mois')
    
class Notification_chef_service(models.Model):
    unite = models.ForeignKey(Unite, on_delete=models.SET)


    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

  
        
    def __str__(self):
        return f"MontantMensuel {self.unite.lib_unit} "
    
    

@receiver(post_save, sender=Consultation)
def my_model_post_save(sender, instance, created, **kwargs):
    if created:
        current_month = datetime.now().month
        current_year = datetime.now().year
        # Calculer le total des consultations pour chaque mois et chaque unité
        consultations_totals = Consultation.objects.values('unite', 'created_at__month').annotate(total=Sum('total'))

        # Boucler sur les résultats pour créer les instances MontantMensuel correspondantes
        for c in consultations_totals:
            # Vérifier si l'unité correspondante a un MontantMensuel pour le mois et l'année en question
            
            if not MontantMensuel.objects.filter(unite=c['unite'], mois=current_month, annee=current_year).exists():
                # Si le MontantMensuel n'existe pas, créer une nouvelle instance avec le total de consultations correspondant
                print("hhhhotz")
            else:
                # Sinon, mettre à jour le total du MontantMensuel avec le total de consultations correspondant
                montant_mensuel = MontantMensuel.objects.get(unite=c['unite'], mois=current_month, annee=current_year)
                montant_mensuel.total_of_month = c['total']
                montant_mensuel.save()

@receiver(post_save, sender=MontantMensuel)
def montant_mensuel_saved(sender, instance, **kwargs):
    if instance.pk is None:
        # l'instance est nouvelle
        print("Une nouvelle instance de MontantMensuel a été créée.")
    else:
        # l'instance a été mise à jour
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "montant_mensuel_updates",
            {
                "type": "notify_update",
                "message": {
                    "type": "update",
                    "id": instance.id,
                    "total": instance.total,
                    "total_of_month": instance.total_of_month,
                }
            }
        )
        print("L'instance de MontantMensuel a été mise à jour.")      

@receiver(post_save, sender=MontantMensuel)
def update_montant_mensuel_data(sender, instance, **kwargs):
    # Create a group name for this specific unite
    montant_mensuel_group_name = 'montant_mensuel_%s' % instance.unite.lib_unit
    channel_layer = get_channel_layer()

    # Send a message to the montant_mensuel group for this unite
    async_to_sync(channel_layer.group_send)(
        montant_mensuel_group_name,
        {
            'type': 'montant_mensuel_data',
        }
    )
@receiver(post_save, sender=MontantMensuel)
def send_montant_mensuel_update(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    unit = instance.unite.lib_unit
    data = {
        "id": instance.id,
        "unite": instance.unite.lib_unit,
        "mois": instance.mois,
        "annee": instance.annee,
        "total": instance.total,
        "total_of_month": instance.total_of_month,
    }
    async_to_sync(channel_layer.group_send)(
        f"montant_mensuel_updates_{unit}",
        {
            "type": "notify_update",
            "message": data
        }
    )    
@receiver(post_save, sender=Consultation)
def check_consultations_totals(sender, instance, created, **kwargs):
    if created:
        # Get the current date
            current_date = date.today()
            current_month = datetime.now().month
            current_year = datetime.now().year
            
# Get the last day of the current month
            last_day_of_month = datetime(current_date.year, current_date.month, 1) + timedelta(days=32) - timedelta(days=1)

# Convert the current date to a datetime object
            current_datetime = datetime.combine(current_date, datetime.min.time())
            consultations_totals = Consultation.objects.values('unite', 'created_at__month').annotate(total=Sum('total'))
            for c in consultations_totals:
                montant_mensuel_exists = MontantMensuel.objects.filter(unite=c['unite'], mois=current_month, annee=current_year).exists()
                if not montant_mensuel_exists:
                    print('hhhh')

                else:
                # Vérifier si la date actuelle est dans les 10 derniers jours du mois
                #if (last_day_of_month - current_datetime).days < 10:

                    # Obtenir la liste des unités dans la base de données
                    units = MontantMensuel.objects.values_list('unite', flat=True).distinct()
                    # Boucler sur chaque unité
                    for unit in units:
                        # Obtenir le total des consultations pour cette unité pour le mois actuel
                        consultations_total_for_unit = Consultation.objects.filter(unite=unit, created_at__month=current_date.month).aggregate(total=Sum('total'))['total'] or 0
                        montant_mensuel = MontantMensuel.objects.get(unite=unit, mois=current_date.month)  # Récupérer l'objet MontantMensuel correspondant
                        total_fixe = montant_mensuel.total  # Accéder à l'attribut total_fixe de l'objet MontantMensuel
                        unite = Unite.objects.get(id=unit)
                        lib_unit = unite.lib_unit  # Accéder à l'attribut total_fixe de l'objet MontantMensuel
                        instances = []

                        # Récupérer l'objet MontantMensuel correspondant

                        # Vérifier si le total des consultations pour chaque unité est inférieur à 60% du total_fixe
                        if consultations_total_for_unit < (total_fixe): #* 0.6):
                            # Si le total des consultations pour une unité est inférieur à 60% du total_fixe, créer une instance de Signal avec les détails appropriés
                            if not Notification_chef_service.objects.filter(unite=unite,read =False).exists()  :

                                instances.append(Notification_chef_service(unite=unite))
                                if instances:
                                    Notification_chef_service.objects.bulk_create(instances)
                                else:
                                    print("No instances created.")
                            else:
                                print("Signal min:",lib_unit)
                            
                        else:
                            # Sinon, supprimer toute instance existante de Signal pour cette unité
                            print("Signal max:",lib_unit)
            # else:
                    # La date actuelle n'est pas dans les 10 derniers jours du mois
                #   print("Current date is not within the last 10 days of the month")



@receiver(post_save, sender=Notification_chef_service)
def send_notification(sender, instance, **kwargs):
 if instance:
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "chef_service",
        {
            "type": "send_notification",
            "data": {
                                     "unite": instance.unite.lib_unit,

            },
        },
    )