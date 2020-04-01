from  django.forms import ModelForm

from .models import Article

#文章表单
class ArticleForm(ModelForm):
    class Meta:
        model=Article
        fields=['title','body',"avator"]