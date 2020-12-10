# users方法
from users import views
from users.views import *
# path 路径包
from django.urls import path
# 路由
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'user_info',UserProfileSerializerViewSet, basename="user_info")
router.register(r'user_history',UserHistoryViewSet, basename="user_history")
router.register(r'user_collection', UserCollectionViewSet, basename="user_collection")
urlpatterns = [
    path('register/', views.addUser),
    path('login/', views.userLogin),
    path('recordHistory/', views.recordHistory),
    path('recordCollection/', views.recordCollection),
    path('getHotCompanyInfo/', views.getHotCompanyInfo),
]
urlpatterns += router.urls