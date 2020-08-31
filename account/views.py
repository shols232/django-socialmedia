from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, UpdateUserForm, ProfileUpdateForm
from django.contrib.auth.models import User
from .models import UserFollowing
from django.urls import reverse
from django.http import JsonResponse
import json
# Create your views here.

def register(request):
    if request.method == 'POST':
        if request.POST.has_key:
            request.session.set_expiry(1209600)
        form = RegisterForm(request.POST)
    else:
        form = RegisterForm()
    return render(request, 'account/register.html',{'form':form})


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


