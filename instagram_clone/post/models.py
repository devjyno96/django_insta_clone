from django.db import models
from django.contrib.auth.models import User
# Create your models here.

from django.db.models.signals import post_save
from django.utils.text import slugfy

