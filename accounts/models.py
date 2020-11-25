from django.contrib.auth.models import AbstractUser # 유저 전용 모델(추상화)
from django.db import models

# Create your models here.
class User(AbstractUser):
    #필드 추가
    website_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    


class Profile(models.Model):
    pass