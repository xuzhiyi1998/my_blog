from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
import markdown
from django.db.models.query_utils import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View
from .models import Article,ArticleColum
from .forms import ArticleForm
from django.core.paginator import Paginator
from comment.models import Comment
from comment.forms import CommentForm
from django.db.models import Q
# Create your views here.
@method_decorator(login_required(login_url="/user/login"),name="get")
class ArticleView(View):
    def get(self,request):
        order=request.GET.get("order")
        search=request.GET.get("search")
        if search:
            if order=="total_view":
                article_list=Article.objects.filter(Q(title__icontains=search)
                                                    |Q(body__icontains=search)).order_by("-total_view" )
            else:
                article_list=Article.objects.filter(Q(title__icontains=search)|
                                                    Q(body__icontains=search))
                order="normal"
        else:
            search=""
            if order=="total_view":
                article_list=Article.objects.all().order_by("-total_view")
            else:
                article_list=Article.objects.all()
                order="normal"
        paginator=Paginator(article_list,3)
        page=request.GET.get("page")
        articles=paginator.get_page(page)
        context={"articles":articles,"order":order,"search":search}
        return render(request,"article/article_list.html",context)
@method_decorator(login_required(login_url="/user/login"),name="get")
class ArticelDetail(View):
    def get(self,request,pk):
        article=Article.objects.get(id=pk)
        article.total_view+=1
        comments=Comment.objects.filter(article_id=pk)
        article.save(update_fields=["total_view"])
        md = markdown.Markdown(
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ]
        )
        article.body = md.convert(article.body)
        comment_form=CommentForm()#评论表单
        context={"article":article,"toc":md.toc,"comments":comments,"comment_form":comment_form}
        return render(request,"article/detail.html",context)
@method_decorator(login_required(login_url="/user/login"),name="get")
class ArticleCreate(View):
    """添加文章"""
    def get(self,request):
        form=ArticleForm()
        columns = ArticleColum.objects.all()
        context={"form":form,"columns":columns}
        return render(request,'article/createarticle.html',context)
    def post(self,request):
        form=ArticleForm(request.POST,request.FILES)
        if form.is_valid():
            new_article=form.save(commit=False)
            new_article.author=request.user
            if request.POST["column"]!="none":
                new_article.tag=ArticleColum.objects.get(id=request.POST["column"])
            if request.FILES.get("avator"):
                new_article.avator=request.FILES.get("avator")
            new_article.save()
            return redirect("article:list")
        else:
            return HttpResponse("表单填写有误，请重新填写")
@method_decorator(login_required(login_url="/user/login"),name="post")
class ArticleDelete(View):
    """删除文章"""
    def post(self,request,pk):
        article=Article.objects.get(Q(id=pk)&Q(author=request.user))
        article.delete()
        return redirect("article:list")
@method_decorator(login_required(login_url="/user/login"),name="get")
class ArticleUpdate(View):
    """修改文章"""
    def get(self,request,pk):
        article=Article.objects.get(Q(id=pk)&Q(author=request.user))
        form=ArticleForm()
        columns=ArticleColum.objects.all()
        context={"article":article,"form":form,"columns":columns}
        return render(request,'article/update.html',context)
    def post(self,request,pk):
        form=ArticleForm(request.POST,request.FILES)
        article=Article.objects.get(Q(id=pk)&Q(author=request.user))
        if form.is_valid():
            article.title=request.POST["title"]
            article.body=request.POST["body"]
            if request.FILES.get("avator"):
                article.avator=request.FILES.get("avator")
            article.save()
            return redirect("article:detail",pk=pk)
        else:
            return HttpResponse("表单填写有误，请重新填写")

