from django.views import View
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, render_to_response
from django.contrib.auth import login, logout, authenticate
from repository.models import AdministratorInfo
from web.utils import check_code
from io import BytesIO
import json

from django.forms import Form
from django.forms import widgets
from django.forms import fields
from repository import models
from django.core.exceptions import ValidationError


# Create your views here.


class Homepage(View):
    def get(self, request, *args, **kwargs):
        notice_list = models.NoticeInfo.objects.all()
        news_list = models.NewsInfo.objects.all()

        return render(request, 'index.html', {"news_list": news_list, 'notice_list': notice_list})


# 用户登录
class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        result = {'err_msg': {}, 'status': 'False'}
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if request.session['CheckCode'].upper() == request.POST.get('check_code').upper():
            pass
        else:
            result['err_msg']['error'] = '验证码错误'
            return HttpResponse(json.dumps(result))
        if user:
            login(request, user)
            result['status'] = 'True'
        else:
            result['err_msg']['error'] = '用户名密码错误!'
        return HttpResponse(json.dumps(result))


# 用户登出
class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("/index/")


# 验证码模块
class CheckCodeView(View):
    def get(self, request, *args, **kwargs):
        stream = BytesIO()
        img, code = check_code.create_validate_code()
        img.save(stream, 'PNG')
        request.session['CheckCode'] = code
        return HttpResponse(stream.getvalue())


# class RegisterView(View):
#     def get(self,request,*args,**kwargs):
#         return render(request,'UserRegister.html')

class UserProtocolView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'user_protocol.html')


class RegisterForm(Form):
    username = fields.CharField(
        error_messages={"required": "用户名不能为空"},
        widget=widgets.TextInput(attrs={'id': 'username', 'class': 'username', 'placeholder': '请输入用户名'})
    )
    pwd = fields.CharField(
        min_length=6,
        max_length=12,
        error_messages={'required': '密码不能为空', 'min_length': '密码长度不能小于6', 'max_length': '密码长度不能大于12'},
        widget=widgets.PasswordInput(attrs={'class': 'pwd', 'id': 'pwd', 'placeholder': '密码长度6-16位，数字、字母'},
                                     render_value=True)
    )
    repwd = fields.CharField(
        min_length=6,
        max_length=12,
        error_messages={'required': '密码不能为空', 'min_length': '密码长度不能小于6', 'max_length': '密码长度不能大于12'},
        widget=widgets.PasswordInput(attrs={'class': 'repwd', 'id': 'repwd', 'placeholder': '请再次输入您的密码'},
                                     render_value=True)
    )
    vcode = fields.CharField(
        error_messages={'required': '验证码不能为空'},
        widget=widgets.PasswordInput(attrs={'class': 'code-input fl', 'id': 'vcode', 'placeholder': '请输入验证码'},
                                     render_value=True)
    )

    def clean_username(self):
        c = models.UserProfile.objects.filter(username=self.cleaned_data['username']).count()
        if not c:
            return self.cleaned_data['username']
        else:
            raise ValidationError('用户名已经存在', code='xxx')

    def clean_repwd(self):
        if self.cleaned_data['repwd'] == self.cleaned_data['pwd']:
            return self.cleaned_data['repwd']
        else:
            raise ValidationError('两次密码输入不一致', code='xxx')

    def clean(self):
        return self.cleaned_data


# 用户注册
class RegisterView(View):
    def get(self, request, *args, **kwargs):
        obj = RegisterForm()
        return render(request, 'UserRegister.html', {'form': obj})

    def post(self, request, *args, **kwargs):
        obj = RegisterForm(request.POST)
        print(obj.errors)
        if request.session['CheckCode'].upper() == request.POST.get('vcode').upper():
            pass
        elif request.POST.get('vcode'):

            obj.errors['vcode'] = ['验证码不正确']
        # return render(request, 'UserRegister.html', {'form': obj})
        if obj.is_valid():
            values = obj.clean()
            name = values['username']
            pwd = values['pwd']
            django_user = models.User.objects.create_user(name, name, pwd)
            django_user.save()
            models.UserProfile.objects.create(username=name, password=pwd)
        else:
            return render(request, 'UserRegister.html', {'form': obj})
        return render(request, 'index.html')


# 管理员登录
def administratorlogin(request):
    print("ffffffffffffffff")
    if request.method == 'GET':
        return render(request, 'index.html')
    elif request.method == 'POST':
        result = {'err_msg': {}, 'status': 'False'}
        phone = request.POST.get('ad_phone')
        password = request.POST.get('ad_password')
        user = models.AdministratorInfo.objects.filter(ad_phone__exact=phone, ad_password__exact=password)
        # if request.session['CheckCode'].upper() == request.POST.get('check_code').upper():
        #     pass
        # else:
        #     result['err_msg']['error'] = '验证码错误'
        #     return HttpResponse(json.dumps(result))
        if user:
            response = HttpResponseRedirect('/administrator/')

            return response
        else:
            errmessage = "用户名或密码错误";
            return render(request, 'index.html', {'message': errmessage})


# 首页
def index(request):
    return render(request, 'index.html')


# 本届赛事
def currentcompetition(request):
    return render(request, 'CurrentCompetition.html')


# 辅导资料
def tutorials(request):
    return render(request, 'tutorials.html')


# def downloadfile(request):
#     the_file_name = '1'
#     filename = 'DownloadFiles/2.jpg'
#     response = FileResponse(readfile(filename))
#     response['Content-Type'] = 'application/octet-stream'
#     response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
#     return response
#
#
# def readfile(filename, buf_size=262144):
#     with open(filename, 'rb') as f:
#         while True:
#             c = f.read(buf_size)
#             if c:
#                 yield c
#             else:
#                 break


# 联系我们
def relation(request):
    return render(request, 'relation.html')


# 关于我们
def aboutus(request):
    return render(request, 'AboutUs.html')


# 用户信息页
def personalinfo(request):
    return render(request, 'PersonalInfo.html')


# 用户信息录入
def userinfo(request):
    if request.method == 'GET':
        return render(request, 'PersonalInfo.html')
    elif request.method == 'POST':
        name = request.POST.get('username')
        phone = request.POST.get('userphone')
        sex = request.POST.get('usersex')
        type = request.POST.get('usertype')
        number = request.POST.get('usernumber')
        birth = request.POST.get('userbirth')
        user = models.UserInfo(user_name=name,
                               user_phone=phone,
                               user_sex=sex,
                               user_type=type,
                               user_number=number,
                               user_birth=birth)
        user.save()
        response = {'status': 'True'}
        return HttpResponse(json.dumps(response))


# 用户信息显示
def showuserinfo(request):
    username = request.POST.get('user')
    userinfo_obj = models.UserInfo.objects.filter(user_name=username).first()
    print(userinfo_obj.user_birth)
    if not userinfo_obj:
        result = {'status': 'False'}
    elif userinfo_obj:
        result = {'status': 'True',
              'username': userinfo_obj.user_name,
              'userphone': userinfo_obj.user_phone,
              'usersex': userinfo_obj.user_sex,
              'usertype': userinfo_obj.user_type,
              'usernumber': userinfo_obj.user_number,
              'userbirth': userinfo_obj.user_birth.strftime('%Y-%m-%d'),
              }
    return HttpResponse(json.dumps(result))


# 修改用户信息
def edituserinfo(request):
    if request.method == 'GET':
        return render(request, 'PersonalInfo.html')
    elif request.method == 'POST':
        name = request.POST.get('editname')
        phone = request.POST.get('editphone')
        sex = request.POST.get('editsex')
        type = request.POST.get('edittype')
        number = request.POST.get('editnumber')
        birth = request.POST.get('editbirth')
        user = models.UserInfo(user_name=name,
                               user_phone=phone,
                               user_sex=sex,
                               user_type=type,
                               user_number=number,
                               user_birth=birth)
        user.save()
        response = {'status': 'True'}
        return HttpResponse(json.dumps(response))


# 大赛报名页面
def competitionregistration(request):
    return render(request, 'CompetitionRegistration.html')


# 大赛报名
def addcompetitioninfo(request):
    if request.method == 'GET':
        return render(request, 'CompetitionRegistration.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        userphone = request.POST.get('userphone')
        type = request.POST.get('competitiontype')
        details = request.POST.get('competitiondetail')
        time = request.POST.get('competitiontime')
        competition = models.CompetitionInfo(competition_username=username,
                                             competition_userphone=userphone,
                                             competition_type=type,
                                             competition_details=details,
                                             competition_time=time)
        competition.save()
        response = {'status': 'True'}
        return HttpResponse(json.dumps(response))

# 查看报名信息
def showcompetitioninfo(request):
    if request.method == 'GET':
        return render(request, 'CompetitionRegistration.html')
    elif request.method == 'POST':
        username = request.POST.get('user')
        obj = models.CompetitionInfo.objects.filter(competition_username=username).first()
        if not obj:
            result = {'status': 'False'}
        elif obj:
            result = {'status': 'True',
                      'username': obj.competition_username,
                      'userphone': obj.competition_userphone,
                      }
        print(result)
        return HttpResponse(json.dumps(result))


############################## 管理员操作 ############################
########################各类信息增、删、改、查#########################


################################新闻类#################################
# 显示具体新闻
def newsdetail(request):
    news_list = models.NewsInfo.objects.all()
    return render(request, 'NewsDetail.html', {'news_list':news_list})


# 获取新闻信息
def administrator(request):
    news_list = models.NewsInfo.objects.all()
    return render(request, 'administrator.html', {'news_list': news_list})


# 添加新闻信息
def addnews(request):
    if request.method == 'GET':
        return render(request, 'administrator.html')
    elif request.method == 'POST':
        print("跑到这边")
        title = request.POST.get('newstitle')
        print(title)
        details = request.POST.get('newsdetails')
        time = request.POST.get('newstime')
        # 将数据添加到数据库
        obj = models.NewsInfo(news_title=title,
                              news_details=details,
                              news_time=time)
        print(obj)
        obj.save()
        print(obj)
        response = {'status': 'True'}
        return HttpResponse(json.dumps(response))


# 删除新闻
def deletenews(request):
    newsid = request.GET.get('news_id')
    models.NewsInfo.objects.filter(news_id=newsid).delete()
    return redirect('/administrator/')


# 修改（编辑）新闻
def editnews(request):
    if request.method == 'GET':
        return render(request, 'administrator.html')
    elif request.method == 'POST':
        id = request.POST.get('newsid')
        title = request.POST.get('newstitle')
        details = request.POST.get('newsdetails')
        time = request.POST.get('newstime')
        obj = models.NewsInfo.objects.get(news_id=id)
        obj.news_title = title
        obj.news_details = details
        obj.news_time = time
        obj.save()
        response = {'status': 'True'}
        return HttpResponse(json.dumps(response))


# 查询新闻
def searchnews(request):
    if request.method == 'GET':
        return render(request, 'administrator.html')
    elif request.method == 'POST':
        id = request.POST.get('newsid')
        title = request.POST.get('newstitle')
        time = request.POST.get('newstime')
        obj = models.NewsInfo.objects.filter(news_id=id,
                                             news_title=title,
                                             news_time=time)
        return render(request, 'administrator.html', {'news_list': obj})


#################################通知类###################################
# 显示具体新闻
def noticedetail(request):
    notice_list = models.NoticeInfo.objects.all()
    return render(request, 'NoticeDetail.html', {'notice_list':notice_list})


# 获取通知信息
def noticeoperation(request):
    notice_list = models.NoticeInfo.objects.all()
    return render(request, 'NoticeOperation.html', {'notice_list': notice_list, })


# 添加通知信息
def addnotice(request):
    if request.method == 'GET':
        return render(request, 'administrator.html')
    elif request.method == 'POST':
        title = request.POST.get('noticetitle')
        print(title)
        details = request.POST.get('noticedetails')
        time = request.POST.get('noticetime')
        # 将数据添加到数据库
        obj = models.NoticeInfo(notice_title=title,
                                notice_details=details,
                                notice_time=time)
        obj.save()
        print(obj)
        response = {'status': 'True'}
        return HttpResponse(json.dumps(response))


# 查询通知信息
def searchnotice(request):
    if request.method == 'GET':
        return render(request, 'NoticeOperation.html')
    elif request.method == 'POST':
        id = request.POST.get('noticeid')
        title = request.POST.get('noticetitle')
        time = request.POST.get('noticetime')
        obj = models.NoticeInfo.objects.filter(notice_id=id,
                                               notice_title=title,
                                               notice_time=time)
        return render(request, 'NoticeOperation.html', {'notice_list': obj})


# 修改通知信息
def editnotice(request):
    if request.method == 'GET':
        return render(request, 'NoticeOperation.html')
    elif request.method == 'POST':
        id = request.POST.get('noticeid')
        title = request.POST.get('noticetitle')
        details = request.POST.get('noticedetails')
        time = request.POST.get('noticetime')
        obj = models.NoticeInfo.objects.get(notice_id=id)
        obj.notice_title = title
        obj.notice_details = details
        obj.notice_time = time
        obj.save()
        response = {'status': 'True'}
        return HttpResponse(json.dumps(response))


# 删除通知信息
def deletenotice(request):
    noticeid = request.GET.get('notice_id')
    models.NoticeInfo.objects.filter(notice_id=noticeid).delete()
    return redirect('/noticeoperation/')


##############################用户信息类################################

# 获取用户信息
def useroperation(request):
    userinfo_list = models.UserInfo.objects.all()
    return render(request, 'UserOperation.html', {'userinfo_list': userinfo_list})


# 添加用户信息
def adduserinfo(request):
    if request.method == 'GET':
        return render(request, 'UserOperation.html')
    elif request.method == 'POST':
        name = request.POST.get('username')
        phone = request.POST.get('userphone')
        sex = request.POST.get('usersex')
        type = request.POST.get('usertype')
        number = request.POST.get('usernumber')
        birth = request.POST.get('userbirth')
        # 将数据添加到数据库
        obj = models.UserInfo(user_name=name,
                              user_phone=phone,
                              user_sex=sex,
                              user_type=type,
                              user_number=number,
                              user_birth=birth,)
        obj.save()
        print(obj)
        response = {'status': 'True'}
        return HttpResponse(json.dumps(response))


# 查询用户信息
def searchuserinfo(request):
    if request.method == 'GET':
        return render(request, 'UserOperation.html')
    elif request.method == 'POST':
        name = request.POST.get('username')
        phone = request.POST.get('userphone')
        obj = models.UserInfo.objects.filter(user_name=name,
                                             user_phone=phone,)
        return render(request, 'UserOperation.html', {'userinfo_list': obj})


# 修改用户信息
def edituserinfo(request):
    if request.method == 'GET':
        return render(request, 'UserOperation.html')
    elif request.method == 'POST':
        name = request.POST.get('username')
        phone = request.POST.get('userphone')
        sex = request.POST.get('usersex')
        type = request.POST.get('usertype')
        number = request.POST.get('usernumber')
        birth = request.POST.get('userbirth')
        obj = models.UserInfo.objects.get(user_phone=phone)
        obj.user_name = name
        obj.user_phone = phone
        obj.user_sex = sex
        obj.user_type = type
        obj.user_number = number
        obj.user_birth = birth
        obj.save()
        response = {'status': 'True'}
        return HttpResponse(json.dumps(response))


# 删除用户信息
def deleteuserinfo(request):
    phone = request.GET.get('userinfo_phone')
    models.UserInfo.objects.filter(user_phone=phone).delete()
    return redirect('/useroperation/')

##############################大赛报名类################################

# 获取报名信息
def applyoperation(request):
    competitioninfo_list = models.CompetitionInfo.objects.all()
    return render(request, 'ApplyOperation.html', {'competitioninfo_list': competitioninfo_list})