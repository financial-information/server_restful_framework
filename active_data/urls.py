from django.conf.urls import url, include
from django.urls import path


from active_data import views
# 权限
from django.contrib.auth.decorators import login_required

urlpatterns =[
  path('getExponentDataByCode/', views.getExponentDataByCode),
  path('getXSHGExponentType/', views.getXSHGExponentType),
  path('getXSHEExponentType/', views.getXSHEExponentType),
]


