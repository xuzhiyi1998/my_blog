from django.shortcuts import render,redirect,HttpResponse,reverse
from django.views import View
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate,logout
from .forms import LoginForm,RegisterForm,UserInform
from .models import UserProfile
# Create your views here.

class LoginView(View):
    def get(self,request):
        form=LoginForm()
        context={"form":form}
        return render(request,"userprofile/login.html",context)
    def post(self,request):
        form=LoginForm(data=request.POST)
        username=request.POST["username"]
        password=request.POST["password"]
        if form.is_valid():
            user=authenticate(username=username,password=password)
            if user:
                login(request,user)
                return redirect(reverse("article:list"))
            return HttpResponse("用户名或密码输入错误")
        else:
            return HttpResponse("表单填写有误")
@method_decorator(login_required(login_url="/user/login"),name="get")
class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect("user:login")

class RegisterView(View):
    "注册视图"
    def get(self,request):
        form=RegisterForm()
        context={"form":form}
        return render(request,"userprofile/register.html",context)
    def post(self,request):
        form=RegisterForm(data=request.POST)
        if form.is_valid():
            new_user=form.save(commit=False)
            new_user.set_password(form.cleaned_data.get("password"))
            new_user.save()
            login(request,new_user)
            return redirect(reverse("article:list"))
        else:
            return HttpResponse("表单填写有误，请重新填写")
@method_decorator(login_required(login_url="/user/login"),name="post")
class UserDeleteView(View):
    """删除用户视图"""
    def post(self,request,pk):
        user=User.objects.get(id=pk)
        if request.user==user:
            logout(request)
            user.delete()
            return redirect(reverse("user:login"))
        else:
            return HttpResponse("你没有权限删除此用户")

@method_decorator(login_required(login_url="/user/login"),name="get")
class EditUserView(View):
    """修改用户信息"""
    def get(self,request,pk):
        user=User.objects.get(id=pk)
        userprofile=UserProfile.objects.get(user_id=pk)
        form=UserInform()
        context={"form":form,"profile":userprofile,"user":user}
        return render(request,"userprofile/edit.html",context)
    def post(self,requeset,pk):
        user = User.objects.get(id=pk)
        if UserProfile.objects.filter(user_id=pk).exists():
            userprofile=UserProfile.objects.get(user_id=pk)
        else:
            userprofile=UserProfile.objects.create(user_id=pk)
        form=UserInform(requeset.POST,requeset.FILES)
        if form.is_valid():
            userprofile.phone=requeset.POST["phone"]
            userprofile.introd=requeset.POST["bio"]
            if "avator" in requeset.FILES:
                userprofile.avator=requeset.FILES["avator"]
            userprofile.save()
            return redirect("article:list")
        else:
            return HttpResponse("表单填写有误请重新填写")

