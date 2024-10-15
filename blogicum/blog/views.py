from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.utils import timezone
from django.http import Http404
# Create your views here.
from django.contrib.auth.models import User 
from django.core.paginator import Paginator
from blog.models import Post,Category,Location
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,DetailView
from .forms import PostForm,UserEditForm
from django.urls import reverse_lazy,reverse
from .forms import PostForm







class PostListView(ListView):
    model = Post
    ordering = 'id'
    paginate_by =10 



def edit_profile(request):
    user = request.user  

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('blog:profile', username=user.username) 
    else:
        form = UserEditForm(instance=user)  

    context = {'form': form}
    return render(request, 'blog/user.html', context)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/detail.html', {'post': post})



class PostDetailView(DetailView):
    model = Post

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
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


def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    if not category.is_published:
        raise Http404("Категория не опубликована")
    current_time = timezone.now()
    post_list = Post.objects.filter(
        category=category,
        is_published=True,
        pub_date__lte=current_time
    )

    context = {
        'category': category,
        'post_list': post_list
    }

    return render(request, 'blog/category.html', context)





class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
  

    def form_valid(self, form):
        form.instance.author = self.request.user 
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user.username})





class PostDeleteView(DeleteView):
    model = Post
    success_url= reverse_lazy('blog:index')



class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
