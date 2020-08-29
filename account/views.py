from django.shortcuts import render
from django.contrib.auth.models import User
from .models import UserFollowing
from django.http import JsonResponse
import json

def profile(request, id):
    request_user = request.user
    user = User.objects.get(id=id)
    follows = user.followers.filter(following_user_id=request_user).exists()
    followers_count = user.followers.count()
    following_count = user.following.count()
    owner = False
    if request_user == user:
        owner = True
    if follows:
        action = 'Unfollow'
    else:
        action = 'Follow'
    return render(request, 'profile.html', {'user':user, 'owner':owner, 'following_count':following_count, 
        'followers_count':followers_count, 'action':action, 'request_user_id':request_user.id, 'follows':follows})

def follow_action(request):
    data = json.loads(request.body)
    following_user_id = data.get('request_user_id')
    user_id = data.get('user_id')
    action = data.get('action')
    following_user = User.objects.get(id=following_user_id)
    user = User.objects.get(id=user_id)
    follows = user.followers.filter(following_user_id=following_user).exists()
    print(follows)
    if action == 'Follow':
        if not follows:
            UserFollowing.objects.create(following_user_id=following_user,user_id=user)
        else:
             pass

    elif action == 'Unfollow':
        if follows:
            rel = UserFollowing.objects.get(following_user_id=following_user,user_id=user)
            print('yoooo')
            rel.delete()
        else:
             pass

    return JsonResponse({'status':'success'}, safe=False)


