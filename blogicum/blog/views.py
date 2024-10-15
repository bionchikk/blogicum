from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.utils import timezone
from django.http import Http404
# Create your views here.
from django.contrib.auth.models import User 
from django.core.paginator import Paginator
from blog.models import Post,Category,Location,Comment
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostForm,UserEditForm,CommentForm
from django.urls import reverse_lazy,reverse
from .forms import PostForm
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required






class PostListView(ListView):
    model = Post
    ordering = '-created_at'
    paginate_by =10 




class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserEditForm
    template_name = 'blog/user.html'  

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        form.save()
        return redirect('blog:profile', username=self.request.user.username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context




class PostDetailView(DetailView):
    model = Post

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (self.object.comments.select_related('author'))
        return context 
    


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=profile)  
    page_obj = posts  
    context = {
        'profile': profile,
        'page_obj': page_obj,
    }
    return render(request, 'blog/profile.html', context)


class CategoryPostsView(ListView):
    model = Post
    template_name = 'blog/category.html'  
    context_object_name = 'post_list'  
    paginate_by = 10  

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        category = get_object_or_404(Category, slug=category_slug)

        if not category.is_published:
            raise Http404("Категория не опубликована")

        current_time = timezone.now()

        return Post.objects.filter(
            category=category,
            is_published=True,
            pub_date__lte=current_time
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, slug=self.kwargs.get('category_slug'))
        return context



class PostCreateView(CreateView,LoginRequiredMixin):
    model = Post
    form_class = PostForm
  

    def form_valid(self, form):
        form.instance.author = self.request.user 
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user.username})



class PostDeleteView(DeleteView,LoginRequiredMixin):
    model = Post
    success_url= reverse_lazy('blog:index')

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Post,pk = kwargs['pk'])
        if instance.author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    


class PostUpdateView(UpdateView,LoginRequiredMixin):
    model = Post
    form_class = PostForm
    
    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Post,pk = kwargs['pk'])
        if instance.author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    post_object = None 

    def dispatch(self, request, *args, **kwargs):
        self.post_object = get_object_or_404(Post, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post_object
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.post_object.pk})


class CommentDeleteView(DeleteView, LoginRequiredMixin):
    model = Comment
    pk_url_kwarg = 'comment_id' 

    def dispatch(self, request, *args, **kwargs):
        
        self.comment = get_object_or_404(Comment, pk=kwargs['comment_id'], post_id=kwargs['post_id'])
        if self.comment.author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.comment.post_id})

class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    pk_url_kwarg = 'comment_id'

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Comment, pk=kwargs['comment_id'], post_id=kwargs['post_id'])
        if instance.author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    
