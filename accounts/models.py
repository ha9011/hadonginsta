from django.contrib.auth.models import AbstractUser # 유저 전용 모델(추상화)
from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string  # 템플릿을 스트링으로 변경해줌
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.shortcuts import resolve_url

# Create your models here.
class User(AbstractUser):
    #objects = models.Manager()
    class GenderChoices(models.TextChoices):
        MALE = "M", "남성"   # DB에 저장되는 값 , 보여지는 값 주의
        FEMALE = "F", "여성"

    follower_set = models.ManyToManyField("self", blank=True)  #" self 자기자신, 유저들과 관계"
    following_set = models.ManyToManyField("self", blank=True)

    #필드 추가
    website_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    phone_number = models.CharField(max_length=13, validators=[RegexValidator(r"^010-?[1-9]\d{3}-?\d{4}$")], blank=True )
    gender = models.CharField(max_length=1,choices = GenderChoices.choices, blank=True)
    avatar = models.ImageField(blank=True, upload_to="accounts/avatar/%y/%m/%d")
    
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return resolve_url("pydenticon_image", self.username)
            



    def send_welcome_email(self):
        # render_to_string (render랑 같다, 1- 템플릿, 2- 넘길값)
        title = render_to_string("accounts/welcome_email_subject.txt", {
            "user" : self,
        })
        content = render_to_string("accounts/welcome_email_content.txt", {
            "user" : self,
        })
        sender_email = settings.WELCOME_EMAIL_SENDER
        send_mail(title, content, sender_email, [self.email], 
        fail_silently=False)

class Profile(models.Model):
   pass