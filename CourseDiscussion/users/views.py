from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from .forms import UserForm
from django.contrib.auth.forms import UserCreationForm
from . forms import UserForm
from . import models
# Create your views here.
def logout(request):
    """注销账户"""
    if not request.session.get('is_login', None):
        # 如果本来就未登录
        return HttpResponseRedirect(reverse('search:index'))
    request.session.flush()
    return HttpResponseRedirect(reverse('search:index'))

def register(request):
    """注册新用户"""
    if request.session.get('is_login', None):
        # 登录状态不允许注册
        HttpResponseRedirect(reverse('search:index'))
    if request.method == "POST":
        register_form = models.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            institute = register_form.cleaned_data['institute']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'users/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'users/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'users/register.html', locals())
                # 当一切都OK的情况下，创建新用户
                new_user = models.User.objects.create()
                new_user.name = username
                new_user.password = password1
                new_user.email = email
                new_user.sex = sex
                new_user.institute = institute
                new_user.save()
                return HttpResponseRedirect(reverse('users:users/login'))  # 自动跳转到登录页面
    register_form = models.RegisterForm()
    return render(request, 'users/register.html', locals())

def login(request):
    if request.session.get('is_login', None):
        return HttpResponseRedirect(reverse('search:index'))

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return HttpResponseRedirect(reverse('search:index'))
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'users/login.html', locals())

    login_form = UserForm()
    return render(request, 'users/login.html', locals())