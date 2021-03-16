from django.contrib import admin
from .models import Post, Tag, Follow, Stream, Likes

# Register your models here.
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(Stream)
admin.site.register(Likes)
