from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


#모델폼
#class SignupForm(forms.ModelForm):   # 
#    class Meta:
#        model = User
#        fields = ['username', 'password']
class SignupForm(UserCreationForm):   # views.py에서 requset.post로 받으니깐, 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    class Meta(UserCreationForm.Meta):
        model = User
        fields=["username", "email", "first_name", "last_name"]

    def clean_email(self):
        print("------ing clean_email----------------")
        email = self.cleaned_data.get('email')
        if email:
            qs = User.objects.filter(email=email)
            if qs.exists():
                raise forms.ValidationError("이미 등로된 이메일 주소입니다")
        
        return email
    
   
