from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from mptt.models import MPTTModel,TreeForeignKey
from ckeditor.fields import RichTextField
from article.models import Article
# Create your models here.

class Comment(MPTTModel):
    """用户评论模型"""
    article=models.ForeignKey(Article,on_delete=models.CASCADE,verbose_name="文章",related_name="comment")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户",related_name="comment")
    text=RichTextField(verbose_name="评论内容")
    dateadded=models.DateTimeField(auto_now_add=True,verbose_name="添加时间")
    parent=TreeForeignKey(
        "self",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="children",
    )
    reply_to=TreeForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="replyers",
    )
    class MPTTMeta:
        order_insertion_by=["dateadded"]
        verbose_name="评论"
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.title[:20]