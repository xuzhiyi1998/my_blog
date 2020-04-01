from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from PIL import Image
# Create your models here.


class ArticleColum(models.Model):
    """文章标签"""
    tag=models.CharField(max_length=100,verbose_name="标签")
    created=models.DateTimeField(auto_now_add=True,verbose_name="创建日期")
    class Meta:
        verbose_name="文章标签"
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.tag

class Article(models.Model):
    """文章"""
    tag=models.ForeignKey(ArticleColum,on_delete=models.CASCADE,verbose_name="标签",
                          blank=True,null=True,related_name="article")
    avator=models.ImageField(upload_to="article/%Y%m%d/",blank=True,verbose_name="标题图片")
    author=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="作者")
    title=models.CharField(max_length=100,verbose_name="标题")
    body=models.TextField(verbose_name="正文")
    date_added=models.DateTimeField(auto_now_add=True,verbose_name="添加时间")
    data_updated=models.DateTimeField(auto_now_add=True,verbose_name="更新时间")
    total_view=models.PositiveIntegerField(default=0,verbose_name="文章浏览量")
    def save(self, *args,**kwargs):
        article=super(Article,self).save(*args,**kwargs)
        if self.avator and not kwargs.get("update_fields"):
            image=Image.open(self.avator)
            (x,y)=image.size
            new_x=400
            new_y=int(new_x*(y/x))
            resized_image=image.resize((new_x,new_y),Image.ANTIALIAS)
            resized_image.save(self.avator.path)
        return article
    def get_absolute_url(self):
        return reverse("article:detail" ,args=[self.id])
    class Meta:
        verbose_name="文章"
        verbose_name_plural=verbose_name
        unique_together=('author','title',)
        ordering=('-date_added',)
    def __str__(self):
        return self.title