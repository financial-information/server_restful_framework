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
# json格式
import json



def addUser(request):
	if request.method == "GET":
		username = request.GET['username']
		password = request.GET['password']
		phone = request.GET['phone']
		user = User.objects.create_user(username,password,phone)
		user.save()
		data = {'status':True,'message':'注册成功成功'}
		result = json.dumps(data)
	return HttpResponse(result)


def userLogin(request):
	result = ""
	if request.method == "GET":
		data = {'url':'/home'}
		result = json.dumps(data)
		return HttpResponse(result)
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
		    if user.is_active:
		        login(request, user)
		        user_session = request.session.session_key
		        data = {'status':True,'message':'登录成功','session':user_session}
		        result = json.dumps(data)
		        return HttpResponse(result)
		else:
			data = {'status':False,'message':'登录失败'}
			result = json.dumps(data)
			return HttpResponse(result)


