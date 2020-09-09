from post.forms import ContentForm
from django.shortcuts import render, redirect
from django.contrib import messages

def modal_post(request):
    if request.method == 'POST':
        form = ContentForm(request.POST or None, request.FILES or None)
        if form.is_valid():           
            form.instance.author = request.user
            form.save()
            messages.success(request, 'Your content have been posted sucessfully' )
    else:
        form = ContentForm()
    return {'form':form}