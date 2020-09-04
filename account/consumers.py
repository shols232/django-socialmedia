import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User
import datetime


class NotificationsConsumer(WebsocketConsumer):


    def connect(self):
        if self.scope["user"].is_anonymous:
            self.close()
        else:
            self.user = self.scope["user"]
            self.group_name = str('chat-%s'%(self.scope["user"].pk))
            async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
            print('my group name', self.group_name)
            self.accept()

    def disconnect(self, close_code):
        self.close()

    def receive(self):
        pass

    def notify(self, event):
        print("yoloooooo")
        self.send(text_data=json.dumps(event["text"]))