from django.shortcuts import render,redirect
from .models import Content
from account.models import Profile
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from .forms import ContentForm
# Create your views here.

class ContentCreateListView(LoginRequiredMixin,CreateView, ListView):
    model = Content
    context_object_name = 'contents'
    paginate_by = 5
    fields = ['content','image_content']
    success_url = '/post'
   # ordering = ["-posted"]
    template_name = 'post/content.html'

    def get_queryset(self):
        return Content.objects.order_by("-posted")

    def form_valid(self, form):
        print(form.instance)
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_line'] = 'Add a new post'
        return context

class ContentCreateView(LoginRequiredMixin,CreateView):
    model = Content
    fields = ['content']
    context_object_name = 'contents'
    success_url = '/post'
    template_name = 'post/create.html'
    oo = Content.objects.filter(author=1)
    # for hii in oo:
    #     print(hii.author.user)
    def form_valid(self, form):
        print(form.instance)
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tag_line'] = 'Add a new post'
        return data


def content_list(request):
    contents = Content.objects.all().order_by('-posted')
    paginator = Paginator(contents, 5)
    page = request.GET.get('page')
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES)
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
        return render(request, 'post/list_content.html', {'section':'contents', 'contents':contents})

    return render(request, 'post/true_content.html', {'section':'contents', 'contents':contents, 'form':form})
