from django.urls import path,re_path
from . import views

urlpatterns = [
   path("logout/", views.logout,  name='logout'),  #/accounts/login/ ==>> settings.LOGIN_URL  # login_required는 이 설정값을 바라봄
   path("login/", views.login,  name='login'),  #/accounts/login/ ==>> settings.LOGIN_URL  # login_required는 이 설정값을 바라봄
   path("signup/", views.signup,  name='signup'),
   path("edit/", views.profile_edit,  name='profile_edit'),
   path('password_change/', views.password_change, name='password_change'),

   re_path(r'(?P<username>[\w.@+-]+)/follow/$' , views.user_follow, name='user_follow'),
   re_path(r'(?P<username>[\w.@+-]+)/unfollow/$' , views.user_unfollow, name='user_unfollow'),
    
   
]