import json

from django.contrib.auth.models import AnonymousUser
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from video.utils import process_bytes, process_text
from recogniter.recogniter import Recogniter


class StreamerConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.user = self.scope["user"]
        self.group_name = 'stream'

        if self.user == AnonymousUser():
            await self.close(code=403)

        print("connection established")

        self.recognizer = Recogniter()

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, disconnect):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        file = ''
        if bytes_data is not None:
            file = process_bytes(bytes_data)
            result = self.recognizer.process_image(file)
            await self.channel_layer.group_send(self.group_name, {
                'type': 'send_message',
                'message': result
            })

        if text_data is not None:
            event = process_text(text_data)
            await self.channel_layer.group_send(self.group_name, event)

    async def send_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({'message': message}))
