from django.contrib import admin
from django.urls import path,include

from . import views

app_name = "blog"
urlpatterns = [
    path('',views.PostListView.as_view(), name = "index"),
    path('<int:pk>/',views.PostDetailView.as_view(), name = "post_detail"),
    path('create_post/',views.PostCreateView.as_view(),name='create_post'),
    path('edit_comment/<int:post_id>/<int:comment_id>/', views.CommentUpdateView.as_view(), name='edit_comment'),
    path('edit_post/<int:pk>/', views.PostUpdateView.as_view(), name='edit_post'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('edit_profile/', views.UserProfileUpdateView.as_view(), name='edit_profile'),
    path('delete_post/<int:pk>/', views.PostDeleteView.as_view(), name='delete_post'),
    path('<slug:category_slug>/',views.CategoryPostsView.as_view(), name = "category_posts"),
    path('<int:pk>/comment/', views.CommentCreateView.as_view(), name='add_comment'),
    path('delete_commet/<int:post_id>/<int:comment_id>/',views.CommentDeleteView.as_view(),name = 'delete_comment')
    
    
    
]
