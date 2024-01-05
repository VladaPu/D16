from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import auth
from django.urls import reverse_lazy
from datetime import datetime
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Posts, Response
from .filters import PostFilter, ResponseFilter
from .forms import PostForm, ResponseForm
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from django.template.context_processors import csrf
from django.contrib.auth.models import User, Group
from django.db.models import Exists, OuterRef
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from django.views import View
# from .tasks import hello, printer
from django.utils.translation import gettext as _
from ckeditor_uploader.fields import RichTextUploadingField


class PostsList(ListView):
    raise_exception = True
    model = Posts
    ordering = '-time_in'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now', 'is_reg'] = datetime.utcnow(), \
            self.request.user.groups.filter(name='Зарегистрированные пользователи').exists()
        return context


class ResponseList(LoginRequiredMixin, ListView):
    raise_exception = True
    model = Response
    ordering = '-time_in'
    template_name = 'responses.html'
    context_object_name = 'responses'
    paginate_by = 20

    def get_queryset(self):
        queryset = Response.objects.filter(res_post__to_reg_user=self.request.user.id).order_by('-time_in')
        self.filterset = ResponseFilter(self.request.GET, queryset, request=self.request.user.id)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['time_in'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context


class SearchResults(ListView):
    raise_exception = True
    model = Posts
    template_name = 'search.html'
    context_object_name = 'search'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    raise_exception = True
    model = Posts
    template_name = 'post_detail.html'
    context_object_name = 'post'
    response_form = ResponseForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        form = ResponseForm()
        post = get_object_or_404(Posts, pk=pk)
        responses = post.reply.all()
        context['post'] = post
        context['responses'] = responses
        context['form'] = form
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    permission_required = ('PostBoard_main.add_post')
    raise_exception = True
    form_class = PostForm
    model = Posts
    template_name = 'post_create.html'

    def post(self, request):
        if request.method == 'POST':
            form = PostForm(request.POST or None)
            if form.is_valid():
                f = form.save(commit=False)
                f.to_reg_user_id = self.request.user.id
                form.save()
                return redirect(f'/posts/')
            else:
                return render(request, 'posts/post_create.html', {'form': form})
        else:
            form = PostForm()
            return render(request, 'posts/post_create.html', {'form': form})


class ResponseCreate(LoginRequiredMixin, CreateView):
    permission_required = ('PostBoard_main.add_response')
    raise_exception = True
    form_class = ResponseForm
    model = Response
    template_name = 'response_create.html'
    # success_url = res_post.get_absolute_url()

    def post(self, request, pk, **kwargs):
        if request.method == 'POST':
            form = ResponseForm(request.POST or None)
            post_to_res = get_object_or_404(Posts, id=pk)
            if form.is_valid():
                f = form.save(commit=False)
                f.res_user_id = self.request.user.id
                f.res_post_id = post_to_res.id
                form.save()
                return super().form_valid(form)
            else:
                return render(request, 'posts/response_create.html', {'form': form})
        else:
            form = ResponseForm()
            return render(request, 'posts/response_create.html', {'form': form})


class ResponseDelete(LoginRequiredMixin, DeleteView):
    raise_exception = True
    model = Response
    template_name = 'response_delete.html'
    success_url = reverse_lazy('responses')
# def to_response_delete(request, pk):
#     # response = get_object_or_404(Response, pk=id)
#     response = Response.objects.filter(id=request.POST.get('id'))
#     response.delete()
#     return redirect('responses')


class PostUpdate(LoginRequiredMixin, UpdateView):
    permission_required = ('PostBoard_main.change_post')
    raise_exception = True
    form_class = PostForm
    model = Posts
    template_name = 'post_edit.html'


class PostDelete(LoginRequiredMixin, DeleteView):
    raise_exception = True
    model = Posts
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts')
