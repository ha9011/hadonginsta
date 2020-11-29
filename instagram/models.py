from django.db import models
from django.conf import settings   # 여기서 URL 받기
from django.urls import reverse
import re

# user 
# -> post.objects.filter(author=user)
# -> user.post_set.all()  <- reated_name으로 변경 ,, 지금은 2개 에서 겹치기 떄문에 이름 변경해야함
class Post(models.Model):
    objects = models.Manager()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, 
                                related_name="my_post_set",
                                on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="instagram/post/%y/%m/%d")
    caption = models.CharField(max_length=500)
    tag_set = models.ManyToManyField('Tag', blank=True)
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL, 
                                            related_name="like_post_set",
                                            blank=True)
    
    
    
    def __str__(self):
        return self.caption

    
    def extract_tag_list(self):
        tag_name_list = re.findall(r"#([a-zA-Z/dㄱ-힣]+)", self.caption)
        tag_list = []
        for tag_name in tag_name_list:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            tag_list.append(tag)
        return tag_list
    
    def get_absolute_url(self): #detail view에서는 가추
        return reverse("instagram:post_detail",  args=[self.pk])   # detail view가 반드시 구현되야함
    

    def is_like_user(self, user):
        return self.like_user_set.filter(pk = user.pk).exists()

    class Meta:
        ordering = ['-id']

class Tag(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
