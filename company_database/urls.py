from django.conf.urls import url, include
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

# , api_root
from rest_framework import renderers
# 路由
from rest_framework.routers import DefaultRouter

from rest_framework.schemas import get_schema_view

from company_database.views import * 


# from rest_framework.documentation import include_docs_urls

router = DefaultRouter()
router.register(r'company_basic_data', CompanyBasicInformationViewSet, basename="company_basic_data")
urlpatterns = router.urls



