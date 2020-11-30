from django.conf.urls import url, include
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

# , api_root
from rest_framework import renderers
# 路由
from rest_framework.routers import DefaultRouter

from rest_framework.schemas import get_schema_view

from company_database.views import * 

from company_database import views
# rest framework 文档接口
from rest_framework.documentation import include_docs_urls
# 权限
from django.contrib.auth.decorators import login_required

router = DefaultRouter()
router.register(r'company_basic_data',CompanyBasicInformationViewSet, basename="company_basic_data")
router.register(r'company_finance_data', CompanyFinanceDataViewSet, basename="company_finance_data")
urlpatterns =[
	path('save_static_data/',views.saveStaticData),
	path('delete_company_data/',views.DeleteCompanyInfo),
	path('docs/', include_docs_urls(title='说明文档')),
]

urlpatterns += router.urls

