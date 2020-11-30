from django.shortcuts import render

# Create your views here.
# 引入自定义用户表
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model  # 要加上这句话不然会报错（1）
User = get_user_model()
#返回值
from django.http import HttpResponse
# 认证用户
from django.contrib.auth import authenticate
# 进行登录（插入session）
from django.contrib.auth import login



def addUser(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		phone = request.POST['phone']
		user = User.objects.create_user(username,password,phone)
		user.save()
	return HttpResponse("success!!!")


def login(request):
	if request.method == "GET":
		return HttpResponse("请登录")
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
		    if user.is_active:
		        login(request, user)
		        return HttpResponse("success!!!")
		else:
			return HttpResponse("fail!!!")


