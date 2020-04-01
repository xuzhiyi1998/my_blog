from django.contrib.auth.models import User
from django.forms import Form
from django import  forms
from .models import UserProfile

class LoginForm(Form):
    """用户表单"""
    username=forms.CharField(max_length=20)
    password=forms.CharField(max_length=50)
    class Meta:
        model=User
        fields=["username","password"]

class RegisterForm(forms.ModelForm):
    "注册表单"
    password=forms.CharField()
    password2=forms.CharField()
    class Meta:
        model=User
        fields=["username","email"]
    def clean_password2(self):
        #clean_字段方法django会自动调用
        data=self.cleaned_data
        if data.get("password")==data.get("password2"):
            return data["password"]
        else:
            raise forms.ValidationError("两次密码输入不一致")

class UserInform(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=["phone","introd","avator"]
