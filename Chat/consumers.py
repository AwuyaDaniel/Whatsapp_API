# chat/consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Code to handle WebSocket connection
        await self.accept()
        pass

    async def disconnect(self, close_code):
        # Code to handle WebSocket disconnection

        pass

    async def receive(self, text_data):
        # Code to handle receiving a message from WebSocket
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
        pass

    async def send_message(self, event):
        # Code to send a message to the WebSocket
        pass
