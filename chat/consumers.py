# myconsumer/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync,sync_to_async
import json
from .models import *
class MyConsumer(AsyncWebsocketConsumer):
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
        # Send the notification data to the client
        count, notifications = await self.get_notifications()
        data = {"type": "notifications", "count": count, "notifications": notifications}
        await self.send(text_data=json.dumps(data))
        print("yessss",data)

    @sync_to_async
    def get_notifications(self):
        # Replace this with your own function to get the notifications
        notifications = Notification.objects.filter(read=False).order_by('-created_at')
        count = notifications.count()
        serialized_notifications = []
        for notification in notifications:
            serialized_notifications.append({
                "message": notification.message,
                                "nom_oc": notification.nom_oc,
                "prenom_oc": notification.prenom_oc,

                "created_at": notification.created_at.isoformat(),
            })
        return count, serialized_notifications
