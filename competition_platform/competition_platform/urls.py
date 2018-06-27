"""competition_platform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from web import views

urlpatterns = [
    url('admin/', admin.site.urls),
    url('index/$', views.Homepage.as_view(), name="index"),

    url(r'^index/check_code.html$', views.CheckCodeView.as_view()),
    url(r'^register/check_code.html$', views.CheckCodeView.as_view()),
    url(r'^currentcompetiton/check_code.html$', views.CheckCodeView.as_view()),
    url(r'^relation/check_code.html$', views.CheckCodeView.as_view()),


    # 用户登录
    url(r'^login/$', views.LoginView.as_view()),

    # 用户登出
    url(r'^logout/$', views.LogoutView.as_view()),

    # 用户注册
    url(r'^register/$', views.RegisterView.as_view()),
    url(r'^user_protocol/$', views.UserProtocolView.as_view()),

    # 管理员登录
    url(r'^administratorlogin/$', views.administratorlogin),
    # 管理员管理界面
    url(r'^administrator/', views.administrator, name="administrator"),


    # 本届赛事
    url(r'^currentcompetiton/', views.currentcompetition, name="currentcompetiton"),

    # 联系我们
    url(r'^relation/', views.relation, name="relation"),

    # 关于我们
    url(r'^aboutus/', views.aboutus),

    # 辅导资料下载
    url(r'^tutorials/', views.tutorials,name="tutorials"),



    # 用户个人信息页面
    url(r'^personalinfo/', views.personalinfo),
    # 用户个人信息填写
    url(r'^adduserinfo/', views.userinfo),
    # 用户信息显示
    url(r'^showuserinfo/', views.showuserinfo),
    # 用户信息修改
    url(r'^edituserinfo/', views.edituserinfo),

    # 大赛报名页面
    url(r'^competitionregistration/', views.competitionregistration),
    # 大赛报名
    url(r'^addcompetitioninfo/',views.addcompetitioninfo),
    # 显示大赛信息
    url(r'^showcompetitioninfo/',views.showcompetitioninfo),


    # 添加新闻
    url(r'^addnews/', views.addnews),
    # 查询新闻
    url(r'^searchnews/', views.searchnews),
    # 修改新闻
    url(r'^editnews/', views.editnews),
    # 删除新闻
    url(r'^deletenews/', views.deletenews),
    # 显示具体新闻
    url(r'^newsdetail/', views.newsdetail, name="newsdetail"),


    # 通知类操作页面
    url(r'^noticeoperation/', views.noticeoperation, name="noticeoperation"),
    # 添加通知
    url(r'^addnotice/', views.addnotice),
    # 查询通知
    url(r'^searchnotice/', views.searchnotice),
    # 修改通知
    url(r'^editnotice/', views.editnotice),
    # 删除通知
    url(r'^deletenotice/', views.deletenotice),
    # 显示具体通知
    url(r'^noticedetail/',views.noticedetail,name="noticedetail"),


    # 用户信息类操作页面
    url(r'^useroperation/', views.useroperation, name="useroperation"),
    # 添加用户信息
    url(r'^adduserinfo/', views.adduserinfo),
    # 查询用户信息
    url(r'^searchuserinfo/', views.searchuserinfo),
    # 修改用户信息
    url(r'^edituserinfo/', views.edituserinfo),
    # 删除用户信息
    url(r'^deleteuserinfo/', views.deleteuserinfo),

    # 报名信息类操作页面
    url(r'^applyoperation/',views.applyoperation,name="applyoperation"),
]
