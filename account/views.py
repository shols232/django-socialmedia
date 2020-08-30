from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.models import User
from .models import UserFollowing
from django.http import JsonResponse
import json
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode,  urlsafe_base64_decode
from django.template.loader import render_to_string
from .email_tokens import account_activation_token
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
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
        return redirect('home')
    else:
        return HttpResponse('Activation link is invalid!')

def send_mail_activation(request):
    return render(request, 'account/sent.html')

@login_required
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


