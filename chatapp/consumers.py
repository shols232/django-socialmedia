# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Messages, Contact, Chat
from .views import get_last_100_messages
import datetime

class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        print(data)
        messages = get_last_100_messages(data['id'])
        if messages['failed']:
                self.send_message({'command':'messages', 'status':'Chat with that id does not exist'})
        else:
            mesages_json = self.messages_to_json(messages['messages'])
            mesages_json.reverse()
            content = {
                'command':'messages',
                'messages':mesages_json
            }
            self.send_message(content)


    def new_message(self, data):
        user = self.scope['user']
        print(data, 'consumer')
        contact, created = Contact.objects.get_or_create(user=user)
        message = Messages.objects.create(contact=contact, content=data['message'])
        chat, created = Chat.objects.get_or_create(id=data["chatID"])
        chat.messages.add(message)
        chat.updated = datetime.datetime.now()
        chat.save()
        chat_id = chat.id
        content = {
            'command':'new_message',
            'chat_id':chat_id,
            'message':self.message_to_json(message)
        }
        self.send_message_to_channel(content)
        
    
    def messages_to_json(self, messages):
        serialized_messages = []
        for message in messages:
            serialized_messages.append(self.message_to_json(message))
        return serialized_messages

    def message_to_json(self, message):
        return {
                'author':message.contact.user.username,
                'content':message.content,
                "image_url":message.contact.user.profile.image.url,
                'date_posted':str(message.timestamp),
            }

    commands = {
        'fetch_messages':fetch_messages,
        'new_message':new_message
    }


    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data_json = json.loads(text_data)
        self.commands[data_json['command']](self, data_json)

        
    def send_message_to_channel(self, message):    
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps(message))