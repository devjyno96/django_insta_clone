from django.urls import path
from .views import index, NewPost, PostDetails, tags

urlpatterns = [
    path('', index, name='index'),
    path('newpost/', NewPost, name='newpost'),
    path('<uuid:post_id>', PostDetails, name='postdetails'),
    # path('<uuid:post_id>/like', like, name='postlike'),
    # path('<uuid:post_id>/favorite', favorite, name='postfavorite'),
    path('tag/<slug:tag_slug>', tags, name='tags'),
]
