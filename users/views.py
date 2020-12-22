from django.shortcuts import render

# json格式
import json
# Create your views here.
# 引入自定义用户表
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model  # 要加上这句话不然会报错
User = get_user_model()
#返回值
from django.http import HttpResponse
# 认证用户
from django.contrib.auth import authenticate
# 进行登录（插入session）
from django.contrib.auth import login
# 混入
from rest_framework import mixins, generics, permissions, viewsets, renderers, filters
# 引入序列
from users.serializers import UserProfileSerializer,UserHistorySerializer,UserCollectionSerializer
# 引入模型
# 引入数据库连接
from django.db import connection
# 过滤器模块和自定义过滤类
from django_filters.rest_framework import DjangoFilterBackend
from users.filters import UserHistoryFilter,UserCollectionFilter,UserInfoFilter
# 分页
from rest_framework.pagination import LimitOffsetPagination
# 引入模型
from users.models import UserProfile,UserCollection,UserHistory

# 分页
from rest_framework.pagination import LimitOffsetPagination

class UserProfileSerializerViewSet(viewsets.ModelViewSet):
	queryset = UserProfile.objects.all()
	serializer_class = UserProfileSerializer
	filter_class = UserInfoFilter
	# 分页
	pagination_class = LimitOffsetPagination



class UserHistoryViewSet(viewsets.ModelViewSet):
	queryset = UserHistory.objects.all()
	serializer_class = UserHistorySerializer
	filter_class = UserHistoryFilter
	# 分页
	pagination_class = LimitOffsetPagination


class UserCollectionViewSet(viewsets.ModelViewSet):
	queryset = UserCollection.objects.all()
	serializer_class = UserCollectionSerializer
	filter_class = UserCollectionFilter
	# 分页
	pagination_class = LimitOffsetPagination


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
	if request.method == "GET":
		data = {'url':'/home'}
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
		    if user.is_active:
		        login(request, user)
		        user_session = request.session.session_key
		        data = {'status':True,'message':'登录成功','session':user_session}
		    else:
		    	data = {'status':False,'message':'用户未激活'}
		else:
			data = {'status':False,'message':'登录失败'}
		result = json.dumps(data)
		return HttpResponse(result)


def recordHistory(request):
	userPhone = request.POST['user_phone']
	history_module_id = request.POST['history_id']
	history_module_type = request.POST['history_type']
	uh = UserHistory()
	uh.user_phone = userPhone
	uh.history_module_type = history_module_type
	uh.history_module_id = history_module_id
	try:
		uh.save()
		data = {'status':True,'message':'历史记录保存成功'}
	except BaseException as reason:
		data = {'status':False,'message':'历史记录保存失败'}
	result = json.dumps(data)
	return HttpResponse(result)


def recordCollection(request):
	userPhone = request.POST['user_phone']
	collection_module_id = request.POST['collection_id']
	collection_module_type = request.POST['collection_type']
	uc = UserCollection()
	uc.user_phone = userPhone
	uc.collection_module_type = collection_module_type
	uc.collection_module_id = collection_module_id
	try:
		uc.save()
		data = {'status':True,'message':'收藏成功'}
	except BaseException as reason:
		data = {'status':False,'message':'收藏失败'}
	result = json.dumps(data)
	return HttpResponse(result)


def getHotCompanyInfo(request):
	module_type = request.POST['module_type']
	size = request.POST['size']
	cursor = connection.cursor()
	if(module_type == "1"):
		try:	
			data = []		
			cursor.execute("SELECT COUNT(*) AS total_visits,history_module_id FROM users_userhistory WHERE history_module_type =%s GROUP BY history_module_id ORDER BY create_time,total_visits DESC",(module_type,))
			rows = cursor.fetchmany(int(size))
			for row in rows:
				drow = {
				'history_module_id':row[1],
				'total_visits':row[0]
				}
				data.append(drow)
			datas = {'status':True,'data':data}
			print(datas)
		except BaseException as reason:
			datas = {'status':False}
			print(reason)
	else:
		datas = None
	results = json.dumps(datas)
	return HttpResponse(results)


def deleteHistory(request):
	deleteArray = request.POST['deleteArray']
	deleteArray = deleteArray.split(",")
	cursor = connection.cursor()
	for item in deleteArray:
		try:
			cursor.execute("UPDATE users_userhistory set deleted = %s WHERE id = %s",(1,item,))
			result = {"status":True}
		except BaseException as reason:
			result = {'status':False,"messgae":reason}
			break
	if result.get("status") == True:
		result = {"status":True,"message":"删除成功"}
	result = json.dumps(result)
	return HttpResponse(result)

def deleteCollection(request):
	deleteArray = request.POST['deleteArray']
	deleteArray = deleteArray.split(",")
	cursor = connection.cursor()
	for item in deleteArray:
		try:
			cursor.execute("UPDATE users_usercollection set deleted = %s WHERE id = %s",(1,item,))
			result = {"status":True}
		except BaseException as reason:
			result = {'status':False,"messgae":reason}
			break
	if result.get("status") == True:
		result = {"status":True,"message":"删除成功"}
	result = json.dumps(result)
	return HttpResponse(result)

