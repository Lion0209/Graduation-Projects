from django.db import models
from django.contrib.auth.models import  User
# Create your models here.

class UserProfile(models.Model):
    '''
    用户信息
    '''
    username = models.CharField(max_length=32,unique=True)
    password = models.CharField(max_length=32,blank=True,null=True)

    class Meta:
        verbose_name_plural = "用户表"

    def __str__(self):
        return self.username

# 管理员表
class AdministratorInfo(models.Model):
    nid = models.AutoField(primary_key=True)
    ad_phone = models.CharField(max_length=32)
    ad_password = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = "管理员表"

    def __unicode__(self):
        return self.ad_password


# 用户信息表
class UserInfo(models.Model):

    user_name = models.CharField(max_length=32)
    user_phone = models.CharField(max_length=32, primary_key=True)
    user_sex = models.CharField(max_length=4)
    user_type = models.CharField(max_length=10)
    user_number = models.CharField(max_length=32)
    user_birth = models.DateField(max_length=16)

    class Meta:
        verbose_name_plural = "用户信息表"

# 大赛新闻表
class NewsInfo(models.Model):
    news_id = models.AutoField(primary_key=True)
    news_title = models.CharField(max_length=120)
    news_details = models.CharField(max_length=600)
    news_time = models.DateField(max_length=20)

    class Meta:
        verbose_name_plural = "大赛新闻表表"

# 大赛新闻表
class NoticeInfo(models.Model):
    notice_id = models.AutoField(primary_key=True)
    notice_title = models.CharField(max_length=120)
    notice_details = models.CharField(max_length=600)
    notice_time = models.DateField(max_length=20)

    class Meta:
        verbose_name_plural = "大赛新闻表"

# 大赛报名表
class CompetitionInfo(models.Model):
    competition_username = models.CharField(max_length=12, primary_key=True)
    competition_userphone = models.CharField(max_length=32)
    competition_type = models.CharField(max_length=32)
    competition_details = models.CharField(max_length=32)
    competition_time = models.DateField(max_length=20)

    class Meta:
        verbose_name_plural = "大赛报名表"