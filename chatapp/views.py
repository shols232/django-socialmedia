
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe
import json
from django.http import JsonResponse
from .models import Chat, Contact, Messages
from django.contrib.auth.models import User

@login_required
def room(request, room_name=None):
        if request.is_ajax():
            return JsonResponse({
            'room_name_json': mark_safe(json.dumps(room_name)),
            'username': mark_safe(json.dumps(request.user.username)),
            })
        username = request.user.username
        if username:
            print(username)
            contact = Contact.objects.filter(user__username=username).first()
            print(contact)
            chats = contact.chats_2.all()
            chats_2 = contact.chats.all()
            total_chats = chats | chats_2
            print('1')
            for chat in total_chats.order_by('updated'):
                print(chat.updated)
            print('2')
            for chat in total_chats.order_by('-updated'):
                print(chat.updated)
            total_chats = total_chats.order_by('-updated')
            print(total_chats, 'data1')
            # data = total_chats.order_by('updated')
            # print(data)
            # print(reversed(total_chats))
            # print(total_chats, chats, chats_2)
            if room_name:
                return render(request, 'room.html', {
                    'chats':total_chats,
                    'room_name_json': mark_safe(json.dumps(room_name)),
                    'username': mark_safe(json.dumps(request.user.username)),
                })
            else:
                return render(request, 'room.html', {
                    'chats':total_chats,
                    # 'room_name_json': mark_safe(json.dumps('')),
                    'username': mark_safe(json.dumps(request.user.username)),
                })

# def serialize_contacts(username):
#     data = Contact.objects.filter(user__username=username).first()
#     serialized_contacts = []
#     for contact in data:


def get_last_100_messages(chat_id, request=None):
    try:
        chat = Chat.objects.get(id=chat_id)
    except (Chat.DoesNotExist, ValueError):
        return {'failed':True, 'message':'Chat Does Not Exist'}
    return {'failed':False, 'messages':chat.messages.order_by('-timestamp')[:100]}


# def chat_list_view(request):
#     username = request.query_params.get('username', None)
#     if username:
#         contact = Contact.objects.filter(user__username=username).first()
#         chats = contact.chats.all()
#         serailized_chats = []
#         for chat in chats:
#             serailized_chats.append({
#                 user:[{}]
#             })
#         return render(chat)
        
def list_user(request):
    if request.is_ajax():
        suggestion = request.GET["suggestion"]
        users = User.objects.filter(username__startswith=suggestion).exclude(username=request.user.username)
        ser_users = []
        for user in users:
            ser_users.append({
                'id':user.id,
                'username':user.username,
                'image_url':user.profile.image.url,
                'bio':user.profile.bio
            })

        return JsonResponse(ser_users, safe=False)


def chat_create_view(request):
    if request.is_ajax():
        print(request, request.GET, 'ylllll')
        chat_id = request.GET["userid"]
        user = User.objects.get(id=chat_id)
        contact, created = Contact.objects.get_or_create(user=user)
        req_contact, created = Contact.objects.get_or_create(user=request.user)
        chat, created = Chat.objects.get_or_create(user_one=req_contact, user_two=contact)
        return JsonResponse({'success':True})

def chat_delete_view(request):
    pass

def chat_update_view(request):
    pass

def chat_detail_view(request):
    pass



