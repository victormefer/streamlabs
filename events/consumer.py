from channels.generic.websocket import AsyncWebsocketConsumer
import json


class EventConsumer(AsyncWebsocketConsumer):
    async def websocket_connect(self):
        self.group_name = 'event-consumer'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def websocket_receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def send_message(self, event):
        message = event['text']
        # Send message to WebSocket
        await self.send(text_data=message)
