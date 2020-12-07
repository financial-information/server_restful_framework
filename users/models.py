from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser,BaseUserManager

# 自定义user_create方法
class UserManger(BaseUserManager):
	#  写此方法为了精简代码，下面创建普通用户跟超级用户都会调用此方法
	def _create_user(self,username,password,phone,**kwargs):
	    if not username:
	        raise ValueError('请输入用户名！')
	    if not password:
	        raise ValueError('请输入密码！')
	    if not phone:
	        raise ValueError('请输入手机号码！')
	    #  self.model 表示User
	    user = self.model(phone=phone,username=username,**kwargs)
	    user.set_password(password)
	    user.save()
	    return user

	    # 创建普通用户
	def create_user(self,username,password,phone,**kwargs):
	    kwargs['is_superuser'] = False
	    return self._create_user(username,password,phone,**kwargs)

	    # 创建超级用户
	def create_superuser(self,username,password,phone,**kwargs):
	    kwargs['is_superuser'] = True
	    return self._create_user(username,password,phone,**kwargs)


class UserProfile(AbstractUser):
	# 删除字段
	first_name = None
	last_name = None
	date_joined = None
	last_login = None
    # 添加字段
	birthday = models.DateField(verbose_name='生日', null=True, blank=True)
	gender = models.CharField(max_length=2,choices=(("1", '男'), ("2", '女')), default='1')
	address = models.CharField(max_length=11, verbose_name='地址', null=True, blank=True)
	image = models.ImageField(upload_to='image/%Y/%m', default="image/default.png", max_length=100) # image依赖Pillow
	phone = models.CharField(max_length=11, verbose_name="手机号码", null=False, blank=True,unique=True)
	create_time = models.DateTimeField(auto_now = True)
    # 设置字段性质
	USERNAME_FIELD = 'phone'  # 作为唯一认证标识， 如果不重写User模型则默认username
	REQUIRED_FIELDS = ['username']  # 设置此属性会提示 username,phone,password
	EMAIL_FIELD = 'email'  # 给指定用户发送邮件 
    #用户管理器重写
	objects = UserManger()
	class Meta:
		ordering = ('id', 'create_time')


class UserHistory(models.Model):
	id = models.AutoField(primary_key = True)
	user_phone = models.CharField(max_length = 11)
	history_module_type = models.CharField(max_length = 5)
	history_module_id = models.CharField(max_length = 20)
	create_time = models.DateTimeField(auto_now = True)
	deleted = models.IntegerField(default= 0)
	class Meta:
		ordering = ('id', 'create_time')


class UserCollection(models.Model):
	id =models.AutoField(primary_key = True)
	user_phone = models.CharField(max_length = 11)
	collection_module_type = models.CharField(max_length = 5)
	collection_module_id = models.CharField(max_length = 20)
	create_time  = models.DateTimeField(auto_now = True)
	deleted = models.IntegerField(default= 0)
	class Meta:
		ordering = ('id', 'create_time')
