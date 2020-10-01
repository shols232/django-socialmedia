from django.shortcuts import render,redirect, get_object_or_404
from .models import Content,Comment
from account.models import Profile
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from .forms import ContentForm,CommentForm
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def content_list(request):
    contents = Content.objects.all().order_by('-posted')

    
   # comments = Content.comments.all()
    paginator = Paginator(contents, 5)
    page = request.GET.get('page')
    if request.method == 'POST':
        print(request.POST)
        form = ContentForm(request.POST or None, request.FILES or None)
        if form.is_valid():           
            form.instance.author = request.user
            form.save()
        return redirect("content")
    else:
        form = ContentForm()
    try:
        contents = paginator.page(page)
    except PageNotAnInteger:
        contents = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse(" ")
        contents = paginator.page(paginator.num_pages)     
    if request.is_ajax():
        return render(request, 'post/list_content.html', {'contents':contents})
    return render(request, 'post/true_content.html', {'contents':contents, 'form':form})

def comment_post(request, content_id):
    content = get_object_or_404(Content, id= content_id)
    comments = Comment.objects.filter(post=content, reply=None).order_by('-created')

    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            reply_id = request.POST.get("comment_id")
            comment_qs = None
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)
            new_comment.reply = comment_qs
            new_comment = comment_form.save(commit=False)          
            
            new_comment.post = content
            
            comment_form.instance.author = request.user
            new_comment.save()
            return redirect(request.path)
    else:
        comment_form = CommentForm()
    return render(request, 'post/comment.html', {
            'content':content,
            'comments':comments,
            'new_comment':new_comment,
            'comment_form':comment_form,
        })


def like_post(request):
    if request.is_ajax():
        print(request.POST)
        post_id = request.POST['post_id']
        action = request.POST['action']
        react = request.POST['react']
        user = request.user
        post = Content.objects.get(id=post_id)
        exists = post.likes.filter(username=user.username).exists()

        if exists:
            if action == 'unlike':
                if react == 'like':
                    post.likes.remove(user)
                elif react == 'love':
                    post.loves.remove(user)
        else:
            if action == 'like':
                if react == 'like':
                    post.likes.add(user)
                elif react == 'love':
                    post.loves.remove(user)
        return JsonResponse({'success':True}, status=200)
    return HttpResponse({'message':'Sorry, You cannot perform that action'}, status=200)
    


            



# def modal_post(request):
#     print("iihh")
#     if request.method == 'POST':
#         form = ContentForm(request.POST or None, request.FILES or None)
#         if form.is_valid():           
#             form.instance.author = request.user
#             form.save()
#         return redirect("content")
#     else:
#         form = ContentForm()

#     return render(request, 'base.html', {'form':form})