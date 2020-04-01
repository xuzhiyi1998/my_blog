from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class UserProfile(models.Model):
    """扩展用户模型"""
    user=models.OneToOneField(User,on_delete=models.CASCADE,verbose_name="用户",related_name="profile")
    phone=models.CharField(max_length=20,blank=True,verbose_name="电话")
    avator=models.ImageField(upload_to="avatar/%Y%m%d/",verbose_name="头像",blank=True)
    introd=models.TextField(verbose_name="用户简介",blank=True)
    class Meta:
        verbose_name="用户信息"
        verbose_name_plural=verbose_name
    def __str__(self):
        return "%s"%self.user.username


"""@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save,sender=User)
def update_user_profile(sender,instance,**kwargs):
    instance.profile.save()"""