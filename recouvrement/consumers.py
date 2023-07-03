import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MontantMensuel,Notification_chef_service
from asgiref.sync import async_to_sync,sync_to_async
from channels.db import database_sync_to_async
import datetime
from django.db.models import Sum
from asgiref.sync import sync_to_async

class MontantMensuelConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Ajouter le consommateur au groupe pour les mises à jour du modèle MontantMensuel
        await self.channel_layer.group_add(
            "montant_mensuel_updates",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Retirer le consommateur du groupe pour les mises à jour du modèle MontantMensuel
        await self.channel_layer.group_discard(
            "montant_mensuel_updates",
            self.channel_name
        )

    async def receive(self, text_data):
        # Rien à faire ici car nous n'écoutons pas les messages envoyés par le client
        pass

    async def notify_update(self, event):
    # Send a WebSocket message to all clients connected to the group for MontantMensuel model updates
       await self.send(text_data=json.dumps(event["message"]))
       print(event["message"])

    # Retrieve latest data from MontantMensuel model and calculate totals
       data = await self.get_data()

    # Send updated data to clients
       await self.send(text_data=json.dumps(data))
       print("Updated MontantMensuel data sent to clients:", data)

    @database_sync_to_async
    def get_data(self):
    # Retrieve latest data from MontantMensuel model and send it to client over WebSocket connection
      data_montant_mensuel_updates = []
      now = datetime.datetime.now()
      mois_actuel = now.month
      annee_actuelle = now.year

    # Get data for all MontantMensuel instances for current month and year
      for montant in MontantMensuel.objects.filter(mois=mois_actuel, annee=annee_actuelle):
        data_montant_mensuel_updates.append({
            "id": montant.id,
            "unite": montant.unite.lib_unit,
            
            "mois": montant.mois,
            "annee": montant.annee,
            "total": montant.total,
            "total_of_month": montant.total_of_month,
        })

    # Calculate total and total_of_month for each unit, as well as for all units together
      totals = {}
      for montant in data_montant_mensuel_updates:
        unite = montant["unite"]
        if unite not in totals:
            totals[unite] = {"total": 0, "total_of_month": 0, "percentage": 0}
        totals[unite]["total"] += montant["total"]
        totals[unite]["total_of_month"] += montant["total_of_month"]

      all_totals = {"total": sum(t["total"] for t in totals.values()), "total_of_month": sum(t["total_of_month"] for t in totals.values())}

    # Calculate percentage for each unit
      for unite in totals:
        total_of_month = totals[unite]["total_of_month"]
        total = totals[unite]["total"]
        percentage = round((total_of_month / total) * 100, 2)
        totals[unite]["percentage"] = percentage

    # Add totals to the MontantMensuel data and return it
      data_by_unit = {}
      for montant in data_montant_mensuel_updates:
        unite = montant["unite"]
        if unite not in data_by_unit:
            data_by_unit[unite] = []
        montant["total_for_unit"] = totals[unite]["total"]
        montant["total_of_month_for_unit"] = totals[unite]["total_of_month"]
        montant["percentage_for_unit"] = totals[unite]["percentage"]
        data_by_unit[unite].append(montant)

    # Return data and calculated totals for each unit
        return {"data_by_unit": data_by_unit, "totals": totals, "all_totals": all_totals}



    

class MontantMensuelConsumer_by_unite(AsyncWebsocketConsumer):
    async def connect(self):
        self.unit = self.scope['url_route']['kwargs'].get('unit')  # Get the unit from the URL parameters
        await self.channel_layer.group_add(
            f"montant_mensuel_updates_{self.unit}",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            f"montant_mensuel_updates_{self.unit}",
            self.channel_name
        )

    async def receive(self, text_data):
        pass

    async def notify_update(self, event):
       await self.send(text_data=json.dumps(event["message"]))
       print(event["message"])
       data_montant_mensuel_updates = await self.get_data()
       for montant in data_montant_mensuel_updates:
          montant["percentage"] = round((montant["total_of_month"] / montant["total"]) * 100, 2)
          data = {"type": "montant_mensuel_updates", "data_montant_mensuel_updates": data_montant_mensuel_updates}
          await self.send(text_data=json.dumps(data))
          print("DATA", montant["percentage"])


    @database_sync_to_async
    def get_data(self):
      data_montant_mensuel_updates = []
      now = datetime.datetime.now()
      mois_actuel = now.month
      annee_actuelle = now.year
    # Filter MontantMensuel objects by unit
      queryset = MontantMensuel.objects.filter(unite__lib_unit=self.unit,mois=mois_actuel, annee=annee_actuelle)
      for montant in queryset:
        data_montant_mensuel_updates.append({
            "id": montant.id,
            "unite": montant.unite.lib_unit,
            "mois": montant.mois,
            "annee": montant.annee,
            "total": montant.total,
            "total_of_month": montant.total_of_month,
        })
      return data_montant_mensuel_updates




class MontantMensuelConsumer_by_anne(AsyncWebsocketConsumer):

    async def connect(self):
        # Get the values of unite and anne from the URL route
        self.unit = self.scope['url_route']['kwargs']['unit']
        self.anne = self.scope['url_route']['kwargs']['anne']

        # Create a group name for this specific unite
        self.montant_mensuel_group_name = 'montant_mensuel_%s' % self.unit

        # Join the montant_mensuel group for this unite
        await self.channel_layer.group_add(
            self.montant_mensuel_group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the montant_mensuel group for this unite
        await self.channel_layer.group_discard(
            self.montant_mensuel_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Convert the incoming text data to JSON
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send a message to the montant_mensuel group for this unite
        await self.channel_layer.group_send(
            self.montant_mensuel_group_name,
            {
                'type': 'montant_mensuel_data',
                'message': message,
            }
        )

    @database_sync_to_async
    def get_data(self):
    # Filter MontantMensuel objects by unite and anne fields
      montants = MontantMensuel.objects.filter(unite__lib_unit=self.unit, annee=self.anne)

    # Group the MontantMensuel objects by the month field
      mois = montants.order_by('mois').values_list('mois', flat=True).distinct()

    # Calculate the total_of_month and total fields for each month
      data = []
      for mois_value in mois:
        montant_of_month = montants.filter(mois=mois_value).order_by('mois').aggregate(total_of_month=Sum('total_of_month'))['total_of_month']
        montant_total = montants.filter(mois=mois_value).order_by('mois').aggregate(total=Sum('total'))['total']
        if montant_total != 0:
            percentage = round((montant_of_month / montant_total) * 100, 2)
        else:
            percentage = 0
        mois_data = {
            'mois': mois_value,
            'total_of_month': montant_of_month,
            'total': montant_total,
            'percentage': percentage,
        }
        data.append(mois_data)

    # Calculate the total for all months
      total_of_all_months = montants.aggregate(total=Sum('total_of_month'))['total']
      total_all_months_data = {
        'mois': 'All',
        'total_of_month': total_of_all_months,
        'total': None,
        'percentage': None,
    }
      data.append(total_all_months_data)

      return data

    async def montant_mensuel_data(self, event):
        # Get the data for this unite and anne
        data = await self.get_data()
        print("111143333")
        # Send the data to the client
        await self.send(text_data=json.dumps({
            'type': 'montant_mensuel_data',
            'data_montant_mensuel': data,
        }))


class ChefServiceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        # Add the client to the "notifications" group
        await self.channel_layer.group_add(
            "notifications",
            self.channel_name,
        )
        self.send(text_data=json.dumps({'status' : 'connected from django channels'}))

    async def disconnect(self, close_code):
        # Remove the client from the "notifications" group
        await self.channel_layer.group_discard(
            "notifications",
            self.channel_name,
        )

    async def receive(self, text_data):
        # Do nothing when receiving a message from the client
        self.send(text_data=json.dumps({'status' : 'we got you'}))

# Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'order_status',
                'payload': text_data
            }
        )

    async def send_notification(self, event):
        count, notifications = await self.get_notifications()
        data = {"type": "chef_service", "count": count, "notifications": notifications}
        await self.send(text_data=json.dumps(data))
        print("chef_service",data)
        
    @sync_to_async
    def get_notifications(self):
        # Replace this with your own function to get the notifications
        notifications = Notification_chef_service.objects.filter(read=False).order_by('-created_at')
        count = notifications.count()
        serialized_notifications = []
        for notification in notifications:
            serialized_notifications.append({
                "unite": notification.unite.lib_unit,
                                      "id": notification.id,

                "created_at": notification.created_at.isoformat(),
            })
        return count, serialized_notifications

    

   