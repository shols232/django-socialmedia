from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, UpdateUserForm, ProfileUpdateForm
from django.contrib.auth.models import User
from .models import UserFollowing
from django.urls import reverse
from django.http import JsonResponse
import json
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode,  urlsafe_base64_decode
from django.template.loader import render_to_string
from .email_tokens import account_activation_token
from django.contrib.auth import login
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import datetime


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user  = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate your Void account'
            message = render_to_string('account/activation_email.html', {
                'user':user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
                
            })
            user.email_user(subject,message)

            # if request.POST.has_key:
            #     request.session.set_expiry(1209600)
            return redirect('mail_sent')
        
    else:
        form = RegisterForm()
    return render(request, 'account/register.html',{'form':form})

def send_mail(request):
    return render(request, "account/sent.html")

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user,backend='django.contrib.auth.backends.ModelBackend')
        return redirect('home')
    else:
        return HttpResponse('Activation link is invalid!')

def send_mail_activation(request):
    return render(request, 'account/sent.html')

@login_required
def profile(request, id):
    request_user = request.user
    user = User.objects.get(id=id)
    follows = user.followers.filter(following_user_id=request_user, user_id=user).exists()
    followers_count = user.followers.count()
    following_count = user.following.count()
    owner = False
    if request_user == user:
        owner = True
    print(request_user)
    print(user.followers.all())
    print(follows)
    if follows:
        action = 'Unfollow'
    else:
        action = 'Follow'
    return render(request, 'profile.html', {'user':user, 'owner':owner, 'following_count':following_count, 
        'followers_count':followers_count, 'action':action, 'request_user_id':request_user.id, 'follows':follows})


@login_required
def edit_profile(request):
    user = request.user
    profile = request.user.profile
    if request.method == "POST":
        print(request.POST)
        u_form = UpdateUserForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid():
            p_form.save()
            u_form.save()
            messages.success(request, f'Your Profile Has Successfully Been Updated' )
            return redirect(reverse('profile', kwargs={'id':user.id}))
    # else:
    #     user = request.user
    #     profile = request.user.profile

    context = {

        "user": user,
        "profile": profile,
    }
    return render(request, "edit_profile.html", context)

@login_required
def home(request):
    return render(request, "account/home.html")


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
            # notify_user = user # Getting current user
            channel_layer = get_channel_layer()
            data = {
                "by":user.username,
                "pic":user.profile.image.url,
                "type":"user_follow",
                "message":f"{user.username} started following you",
                "time":str(datetime.datetime.now())
            }
            print(user.pk, channel_layer)
            # Trigger message sent to group
            async_to_sync(channel_layer.group_send)(
                str('chat-%s'%(user.pk)),  # Group Name, Should always be string
                {
                    "type": "notify",   # Custom Function written in the consumers.py
                    "text": data,
                },
            )
            print("yayyyyawwuuu")
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


