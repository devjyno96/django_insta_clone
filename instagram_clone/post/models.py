import uuid

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

from django.db.models.signals import post_save
from django.utils.text import slugify


def user_directory_path(instance, filename):
    # this file will be uploaded to MEDIA_ROOT / user(id)/ filename
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Tag(models.Model):
    title = models.CharField(max_length=75, verbose_name='Tag')
    slug = models.SlugField(null=False, unique=True)

    class Meta:
        verbose_name_plural = 'Tag'

    def get_absolute_url(self):
        return reversed('tags', arg=[self.slug])

    def __str__(self):
        return self.title

    # slug? - https://itmining.tistory.com/119
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    picture = models.ImageField(upload_to=user_directory_path, verbose_name='Picture', null=False)
    caption = models.TextField(max_length=1500, verbose_name='Caption')
    posted = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name='tags')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reversed('postdetails', args=[str(self.id)])

    def __str__(self):
        return str(self.posted)


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')


class Stream(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='stream_following')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField()

    def add_post(sender, instance, *args, **kwargs):
        post = instance
        user = post.user
        followers = Follow.objects.all().filter(following=user)
        for follower in followers:
            stream = Stream(post=post, user=follower.follower, date=post.posted, following=user)
            stream.save()


# https://docs.djangoproject.com/en/3.1/ref/signals/#post-save
# https://dgkim5360.tistory.com/entry/django-signal-example
# 이게 뭐냐? django signal
# 특정 행동을 수행할 때마다 알려줄것을 설정하고 그 때에 지정한 동작을 수행할 수 있게 하는 기능
# post_save => sender model이 저장된 후 Stream.add_post 수행 하라는 signal
post_save.connect(Stream.add_post, sender=Post)