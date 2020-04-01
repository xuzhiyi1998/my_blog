from django.shortcuts import render,get_object_or_404,redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import Comment
from .forms import CommentForm
from article.models import Article
# Create your views here.

method_decorator(login_required(login_url="/user/login/"),name="post")
class CommentPostView(View):
    """用户添加评论"""
    def post(self,request,article_id,parent_comment_id=None):
        article=get_object_or_404(Article,id=article_id)
        commentform=CommentForm(data=request.POST)
        if commentform.is_valid():
            new_comment=commentform.save(commit=False)
            new_comment.article=article
            new_comment.owner=request.user
            if parent_comment_id:
                parent_comment=Comment.objects.get(id=parent_comment_id)
                new_comment.parent_id=parent_comment.get_root().id
                new_comment.reply_to=parent_comment.owner
                new_comment.save()
                return HttpResponse("200 OK")
            new_comment.save()
            return redirect(article)
        else:
            return HttpResponse("表单填写有误，请重新填写")
    def get(self,request,article_id,parent_comment_id):
        comment_form=CommentForm()
        context={
            "comment_form":comment_form,
            "article_id":article_id,
            "parent_comment_id":parent_comment_id,
        }
        return render(request,"comment/reply.html",context)


