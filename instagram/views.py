from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from .models import Tag, Post
from django.db.models import Q 
from django.utils import timezone
from datetime import timedelta
# Create your views here.

@login_required
def index(request):
    #timesince = timezone.now() - timedelta(day=3) #현재 시간에 3일뺀
    post_list = Post.objects.all()\
        .filter(Q(author__in = request.user.following_set.all())| Q(author = request.user))
        #\.filter(created-at__gte=timedelta)
   
    suggested_user_list = get_user_model().objects.all()\
        .exclude(pk=request.user.pk)\
        .exclude(pk__in = request.user.following_set.all())

    


    return render(request, "instagram/index.html",{
        "suggested_user_list" : suggested_user_list,
        "post_list" : post_list,
    })

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False) # 저장된 post를 반환
            post.author = request.user
            # TODO post.tag_set
            post.save() # 저장 후 pk 값을 얻는다.
            post.tag_set.add(*post.extract_tag_list()) #위에 pk값을 얻은 후 해야하기에 save뒤에 한다 # nm이니 리스트로 넣기
            messages.success(request, "새로운 포스팅이 작성되었습니다.")
            return redirect(post)     # TODO get_absolute_url 활용 작성시, 작성된 pk로 이동

    else: # get
        form = PostForm()

    return render(request, "instagram/post_form.html", {
        "form": form,
    })

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "instagram/post_detail.html", {
        "post" : post
    })

def user_page(request, username):
    #is_active 접근 허용된 사람이 아니면 404
    page_user = get_object_or_404(get_user_model(), username=username, is_active=True)
    post_list = Post.objects.filter(author=page_user)
    post_list_count = post_list.count() # 카운트 쿼리 DB에 던짐
    
    #request.user # 로그인했으면 user객체, 아니면 anoymous
    if request.user.is_authenticated:
        is_follow = request.user.following_set.filter(pk=page_user.pk).exists()
    else:
        is_follow = False

    
    page_user


    return render(request, "instagram/user_page.html", {
        "page_user" : page_user,
        'post_list' : post_list,
        "post_list_count" : post_list_count,
        "is_follow" : is_follow,
    })


@login_required
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.like_user_set.add(request.user)
    # TODO like 처리
    messages.success(request, f"포스팅 #{post.pk}를 좋아합니다.")
    redirect_url = request.META.get("HTTP_REFERER", "root" )
    return redirect(redirect_url)


@login_required
def post_unlike(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.like_user_set.remove(request.user)
    # TODO unlike 처리
    messages.success(request, f"포스팅 #{post.pk}를 좋아요를 취소합니다.")
    redirect_url = request.META.get("HTTP_REFERER", "root" )
    return redirect(redirect_url)
