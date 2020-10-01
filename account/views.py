from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, UpdateUserForm, ProfileUpdateForm
from django.contrib.auth.models import User
from .models import UserFollowing, Notifications
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


from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
# Create your views here.                                                                                                                                                                                                                                                                   

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
        return redirect('content')
    else:
        return HttpResponse('Activation link is invalid!')

def send_mail_activation(request):
    return render(request, 'account/sent.html')

def logout_view(request):
    logout(request)
    messages.info(request,"You have been logged out successfully, please come back next time 🙂")
    return redirect('login')

@login_required
def profile(request, id):
    request_user = request.user
    user = User.objects.get(id=id)
    follows = user.followers.filter(following_user_id=request_user, user_id=user).exists()
    followers_count = user.followers.count()
    following_count = user.following.count()
    owner = False
    print(request.user.content.count)
    if request_user == user:
        owner = True

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
        print(request.FILES)
        if u_form.is_valid():
            p_form.save()
            u_form.save()
            messages.success(request, f'Your Profile Has been Successfully Been Updated' )
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
    count = request.user.my_notifications.filter(read=False).count()
    return render(request, "account/home.html", {'count':count})


def follow_action(request):
    data = json.loads(request.body)
    following_user_id = data.get('request_user_id')
    user_id = data.get('user_id')
    action = data.get('action')
    following_user = User.objects.get(id=following_user_id)
    user = User.objects.get(id=user_id)
    follows = user.followers.filter(following_user_id=following_user).exists()
    print(action)
    if action == 'Follow':
        if not follows:
            UserFollowing.objects.create(following_user_id=following_user,user_id=user)
            notify_user = user # Getting current user
            channel_layer = get_channel_layer()
            try:
                count = Notifications.objects.filter(to_user=user).count() + 1
            except Notifications.DoesNotExist:
                count = 1

            data = {
                "status":"success",
                "count":count,
            }

            async_to_sync(channel_layer.group_send)(
                str('chat-%s'%(user.pk)),  # Group Name, Should always be string
                {
                    "type": "notify",   # Custom Function written in the consumers.py
                    "text": data,
                },
            )

            Notifications.objects.create(to_user=user,
             from_user=following_user,
             message_type="user_follow",
             message=f"{user.username} started following you"
            )
            return JsonResponse({'status':'success'}, safe=False)
        else:
             pass

    elif action == 'Unfollow':
        if follows:
            rel = UserFollowing.objects.get(following_user_id=following_user,user_id=user)
            print('yoooo')
            rel.delete()
            return JsonResponse({'status':'success'}, safe=False)
        else:
             pass

    return JsonResponse({'status':'failed'}, safe=False)

def notifications(request):
    if request.is_ajax():
        user_id = request.GET["user_id"]
        notifs_qs = Notifications.objects.filter(to_user__id=user_id).order_by('-timestamp')
        notifs = []

        for notif in notifs_qs:
            notifs.append({
                'user_id':notif.from_user.id,
                'from_user':notif.from_user.username,
                'message_type':notif.message_type,
                'message':notif.message,
                'read':notif.read,
                'pic':notif.from_user.profile.image.url,
                'time':notif.timestamp.strftime("%b. %d, %H:%M")
            })
            notif.read = True
            notif.save()
        print(notifs)
        return JsonResponse(notifs, safe=False)
