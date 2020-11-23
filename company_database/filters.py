from rest_framework import filters
from rest_framework import mixins, generics, permissions, viewsets, renderers
from django_filters.rest_framework import DjangoFilterBackend


import django_filters
from company_database.models import CompanyBasicInformation

class CompanyBasicInformationFilter(django_filters.FilterSet):
    """
    返回商品列表,自定义序列化器，分页,过滤,搜索，排序
    """

