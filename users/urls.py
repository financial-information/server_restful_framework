# users方法
from users import views
# path 路径包
from django.urls import path

urlpatterns = [
    path('register/', views.addUser),
    path('login/', views.login),
    ]