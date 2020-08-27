from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import RegisterForm

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
    else:
        form = RegisterForm()
    return render(request, 'register.html',{'form':form})
    