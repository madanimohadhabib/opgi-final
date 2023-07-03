from django.db import models  
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import connections
from channels.layers import  get_channel_layer
from asgiref.sync import async_to_sync
import json
class wilaya(models.Model):

   lib_wilaya = models.CharField(max_length=120)
   date_joined= models.DateTimeField(verbose_name='date joined', auto_now_add=True) 

   def __str__(self):
            return self.lib_wilaya

  
        
class Unite(models.Model):
        lib_unit = models.CharField(max_length=120)
        wilaya = models.ForeignKey(wilaya, on_delete=models.SET)
        date_joined= models.DateTimeField(verbose_name='date joined', auto_now_add=True) 

        def __str__(self):
            return self.lib_unit
        

class Cite(models.Model):
              lib_Cite = models.CharField(max_length=120)
              unite = models.ForeignKey(Unite, on_delete=models.SET)
              nb_logts = models.PositiveIntegerField()
              date_joined= models.DateTimeField(verbose_name='date joined', auto_now_add=True) 

              def __str__(self):
                 return self.lib_Cite
              

class Batiment (models.Model):
           lib_Batiment = models.CharField(max_length=120)
           Cite = models.ForeignKey(Cite, on_delete=models.SET)
           nb_logts = models.PositiveIntegerField()
           nb_etage = models.PositiveIntegerField()
           date_joined= models.DateTimeField(verbose_name='date joined', auto_now_add=True) 

           def __str__(self):
                 return self.lib_Batiment
          

class Occupant (models.Model):
       oc_id  = models.PositiveIntegerField(unique=True)
       nom_oc = models.CharField(max_length=120)
       prenom_oc = models.CharField(max_length=120)
       date_naiss = models.DateTimeField(null=True)
       lieu_naiss=models.CharField(max_length=120)

       created_at = models.DateTimeField(auto_now_add=True)

       def __str__(self):
                 return self.nom_oc
       

class Contrat(models.Model):
    occupant = models.ForeignKey(Occupant, on_delete=models.SET)
    date_cnt = models.DateTimeField(null=True)
    date_strt_loyer = models.DateTimeField(null=True)
    loyer = models.FloatField()
    charge = models.CharField(max_length=120)
    mnt_tva = models.FloatField()
    
   
    
    total_of_month = models.FloatField(default=0)
  #siglaler add to changer total 
    def __str__(self):
                 return self.occupant.nom_oc
 

 
@receiver(post_save, sender=Contrat)
def update_total_of_month(sender, instance, **kwargs):
       A = instance.loyer * (instance.mnt_tva/100)
       B = A * 1
       C = instance.loyer * 1
       D = B + C
       charges = float(instance.charge) * 1  # convert charge to float
       total = D + charges












       sender.objects.filter(id=instance.id).update(total_of_month=total)

class Logement (models.Model):
        batiment = models.ForeignKey(Batiment, on_delete=models.SET)
        contrat = models.ForeignKey(Contrat, on_delete=models.SET)
        surface=  models.FloatField( default='m2')
        prix_logement=  models.FloatField()
        type_logement=  models.CharField(max_length=120)

        created_at = models.DateTimeField(auto_now_add=True)
        def __str__(self):
                 return self.contrat.occupant.nom_oc
        

class Consultation (models.Model):
                logement = models.ForeignKey(Logement, on_delete=models.SET)
                occupant = models.ForeignKey(Occupant, on_delete=models.SET)
                unite = models.ForeignKey(Unite, on_delete=models.SET)

                mois=models.PositiveIntegerField()
                created_at = models.DateTimeField(auto_now_add=True)
                total =models.FloatField()
                
                def __str__(self):
                    return self.occupant.nom_oc
                
               
      

                def calculer_dette(self):
                        montant_dette = 0
                        contrat_values = Contrat.objects.values().get(id=self.occupant.id)
                        diff = self.created_at - contrat_values['date_strt_loyer']
                        mois_entiers = int(diff.total_seconds() / 2628000)
                        montant_dette = contrat_values['total_of_month'] * (mois_entiers)
                        paye = contrat_values['total_of_month'] * self.mois
                        montant_dette = paye - montant_dette
                        print("montant_dette::::::::",montant_dette)
                        if mois_entiers <= 0  or self.mois > mois_entiers:
                            mois_entiers = 0
                            montant_dette = 0
                        
                        self.montant_dette = abs(montant_dette)

                        if montant_dette == 0:
                                self.status = 'En règle'
                        elif montant_dette > contrat_values['total_of_month']:
                                 self.status = 'En dette'
                        else:
                                self.status = 'En dette'
                        

                        return montant_dette
     
               

        
       
     
                
               
                

        
     


        
       
     