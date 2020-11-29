from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignupForm, ProfileForm, PasswordChangeForm
from django.contrib.auth.views import (LoginView, logout_then_login, PasswordChangeView as AuthPasswordChangeView,)
from django.contrib.auth import login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import User
# auth 기본적으로 인증은 auth에 있다 활용을 잘해보자

login = LoginView.as_view(template_name="accounts/login_form.html")


def logout(request):
    messages.success(request, "로그아웃되었습니다.")
    return logout_then_login(request)

def signup(request):
    if request.method == "POST":
        #form에 바인딩
        form = SignupForm(request.POST)
        print("--------POST--------------")
        print(request.POST)
        print("**POST**")
        
        print("------bf is_valid----------------")
        if form.is_valid():
            print("------af is_valid----------------")
            signed_user = form.save() # 해당 모델 호출
            auth_login(request,  signed_user)
            messages.success(request, "회원가입 환영합니다.")
            signed_user.send_welcom_email()  # 반응이 늦기 떄문에 비동기 사용할거임
            next_url = request.GET.get('next','/')
            return redirect(next_url)
    else :
        form = SignupForm()
        print("--------get--------------")
        print("get")
        print(form)
        print("----------------------")
    return render(request, 'accounts/signup_form.html', {
        'form' : form,
    })

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user) #이미지까지
        if form.is_valid():
            form.save()
            messages.success(request, "프로필을 수정/저장했습니다")
            return redirect("profile_edit")
    else:
        form = ProfileForm(instance=request.user)  # 빈칸이면 그냥 없는 새로운 걸 생성함, 즉 로그인 정보가 없음
                              #
    return render(request, "accounts/profile_edit_form.html", {
        "form" : form,
    })

@login_required
def password_change(request):
    pass


class PasswordChangeView(LoginRequiredMixin, AuthPasswordChangeView):
    success_url = reverse_lazy("password_change")
    template_name = "accounts/password_change_form.html"
    form_class = PasswordChangeForm
    def form_valid(self, form):
        messages.success(self.request, "암호를 변경했습니다.")
        return super().form_valid(form)
        
password_change = PasswordChangeView.as_view()

@login_required
def user_follow(request, username):
    follow_user = get_object_or_404(User, username=username, is_active=True)

    request.user.following_set.add(follow_user) # 내 입장에서 팔로잉 추가
    follow_user.follower_set.add(request.user) # 상대 입자에서 내가 추가

    messages.success(request, f"{follow_user.username}님을 팔로우 했습니다.")
    redirect_url = request.META.get("HTTP_REFERER", "root" )
    return redirect(redirect_url)

@login_required
def user_unfollow(request, username):
    unfollow_user = get_object_or_404(User, username=username, is_active=True)

    request.user.following_set.remove(unfollow_user) # 내 입장에서 팔로워
    unfollow_user.follower_set.remove(request.user) # 상대 입자에서 나 

    messages.success(request, f"{unfollow_user.username}님을 언팔 했습니다.")
    redirect_url = request.META.get("HTTP_REFERER", "root" )
    return redirect(redirect_url)