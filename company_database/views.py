from django.shortcuts import render

from django.shortcuts import get_list_or_404, get_object_or_404
# Create your views here.

# restful框架包
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
#页数处理
from rest_framework.pagination import PageNumberPagination
# 混入
from rest_framework import mixins, generics, permissions, viewsets, renderers, filters

from django_filters.rest_framework import DjangoFilterBackend

# 引入模型
from company_database.models import CompanyBasicInformation
# 引入序列
from company_database.serializers import CompanyBasicInformationSerializer
# 引入过滤器
from company_database.filters import CompanyBasicInformationFilter


# 视图集
class CompanyBasicInformationViewSet(viewsets.ModelViewSet):
    # lookup_field = "credit_code"
    # 用于详细查询的字段，当下为股票的名字展示股票的内容
    # lookup_field = "stock_name"
    queryset = CompanyBasicInformation.objects.all()
    serializer_class = CompanyBasicInformationSerializer


    