from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import SignupForm

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
            form.save()
            messages.success(request, "회원가입 환영합니다.")
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