from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import RegisterForm

# Create your views here.

def register(request):
    if request.method == 'POST':
        if request.POST.has_key:
            request.session.set_expiry(1209600)
        form = RegisterForm(request.POST)
    else:
        form = RegisterForm()
    return render(request, 'account/register.html',{'form':form})
    