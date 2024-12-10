import json
from channels.generic.websocket import AsyncWebsocketConsumer

class MatchConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Récupérer l'ID du match depuis l'URL
        self.match_id = self.scope['url_route']['kwargs']['match_id']
        self.group_name = f"match_{self.match_id}"

        # Rejoindre le groupe correspondant au match
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Quitter le groupe du match
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        # Recevoir un message du client
        data = json.loads(text_data)

        # Répercuter le message à tout le groupe (contrôle et affichage)
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "broadcast_message",
                "data": data,
            }
        )

    async def broadcast_message(self, event):
        # Envoyer les données à tous les clients du groupe
        await self.send(text_data=json.dumps(event["data"]))
