from django.db import models  
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import connections
from channels.layers import  get_channel_layer
from asgiref.sync import async_to_sync
import json
class wilaya(models.Model):

   lib_wilaya = models.CharField(max_length=120,db_column='lib_wilaya')
   date_joined= models.DateTimeField(verbose_name='date joined', auto_now_add=True,db_column='date_joined') 

   def __str__(self):
            return self.lib_wilaya

   class Meta:
        db_table = 'data_wilaya'
        managed = False 
        
class Unite(models.Model):
        lib_unit = models.CharField(max_length=120,db_column='lib_unit')
        wilaya = models.ForeignKey(wilaya, on_delete=models.SET,db_column='wilaya_id')
        date_joined= models.DateTimeField(verbose_name='date joined', auto_now_add=True,db_column='date_joined') 

        def __str__(self):
            return self.lib_unit
        class Meta:
           db_table = 'data_unite'
           managed = False 

class Cite(models.Model):
              lib_Cite = models.CharField(max_length=120,db_column='lib_Cite')
              unite = models.ForeignKey(Unite, on_delete=models.SET,db_column='unite_id')
              nb_logts = models.PositiveIntegerField(db_column='nb_logts')
              date_joined= models.DateTimeField(verbose_name='date joined', auto_now_add=True,db_column='date_joined') 

              def __str__(self):
                 return self.lib_Cite
              class Meta:
                  db_table = 'data_cite'
                  managed = False 

class Batiment (models.Model):
           lib_Batiment = models.CharField(max_length=120,db_column='lib_Batiment')
           Cite = models.ForeignKey(Cite, on_delete=models.SET,db_column='Cite_id')
           nb_logts = models.PositiveIntegerField(db_column='nb_logts')
           nb_etage = models.PositiveIntegerField(db_column='nb_etage')
           date_joined= models.DateTimeField(verbose_name='date joined', auto_now_add=True,db_column='date_joined') 

           def __str__(self):
                 return self.lib_Batiment
           class Meta:
                  db_table = 'data_batiment'
                  managed = False 
          
class Occupant (models.Model):
       oc_id  = models.PositiveIntegerField(unique=True,db_column='oc_id')
       nom_oc = models.CharField(max_length=120,db_column='nom_oc')
       prenom_oc = models.CharField(max_length=120,db_column='prenom_oc')
       date_naiss = models.DateTimeField(null=True,db_column='date_naiss')
       lieu_naiss=models.CharField(max_length=120,db_column='lieu_naiss')

       created_at = models.DateTimeField(auto_now_add=True,db_column='created_at')

       def __str__(self):
                 return self.nom_oc
       class Meta:
                  db_table = 'data_occupant'
                  managed = False 


class Contrat(models.Model):
    occupant = models.ForeignKey(Occupant, on_delete=models.SET,db_column='occupant_id')
    date_cnt = models.DateTimeField(null=True,db_column='date_cnt')
    date_strt_loyer = models.DateTimeField(null=True,db_column='date_strt_loyer')
    loyer = models.FloatField(db_column='loyer')
    charge = models.CharField(max_length=120,db_column='charge')
    mnt_tva = models.FloatField(db_column='mnt_tva')
    
   
    
    total_of_month = models.FloatField(default=0,db_column='total_of_month')
  #siglaler add to changer total 
    def __str__(self):
                 return self.occupant.nom_oc
    class Meta:
                  db_table = 'data_contrat'
                  managed = False 


 
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
        batiment = models.ForeignKey(Batiment, on_delete=models.SET,db_column='batiment_id')
        contrat = models.ForeignKey(Contrat, on_delete=models.SET,db_column='contrat_id')
        surface=  models.FloatField( default='m2',db_column='surface')
        prix_logement=  models.FloatField(db_column='prix_logement')
        type_logement=  models.CharField(max_length=120,db_column='type_logement')

        created_at = models.DateTimeField(auto_now_add=True,db_column='created_at')
        def __str__(self):
                 return self.contrat.occupant.nom_oc
        class Meta:
                  db_table = 'data_logement'
                  managed = False 

class Consultation (models.Model):
                logement = models.ForeignKey(Logement, on_delete=models.SET,db_column='logement_id')
                occupant = models.ForeignKey(Occupant, on_delete=models.SET,db_column='occupant_id')
                unite = models.ForeignKey(Unite, on_delete=models.SET,db_column='unite_id')

                mois=models.PositiveIntegerField(db_column='mois')
                created_at = models.DateTimeField(auto_now_add=True,db_column='created_at')
                total =models.FloatField(db_column='total')
                
                def __str__(self):
                    return self.occupant.nom_oc
                class Meta:
                  db_table = 'data_consultation'
                  managed = False 
               
                

                def calculer_dette(self):
                        contrat_values = Contrat.objects.values().get(id=self.occupant.id)
                        diff = self.created_at - contrat_values['date_strt_loyer']
                        mois_entiers = int(diff.total_seconds() / 2628000)
                        montant_dette = contrat_values['total_of_month'] * (mois_entiers)
                        paye = contrat_values['total_of_month'] * self.mois
                        montant_dette = paye - montant_dette
                        
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
     


        
       
     