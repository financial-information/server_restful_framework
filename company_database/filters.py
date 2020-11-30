
from rest_framework import mixins, generics, permissions, viewsets, renderers
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from company_database.models import CompanyBasicInformation

class CompanyBasicInformationFilter(filters.FilterSet):
	#对name进行模糊查询,类似于sql里面的like语句，如果不指定lookup_expr就是完全匹配
	company_name = filters.CharFilter(field_name="company_name",lookup_expr="contains")
	industry_type = filters.CharFilter(field_name="industry_type",lookup_expr="contains")
	deteled = filters.NumberFilter(field_name = "deteled")
	#最小资本
	min_price = filters.NumberFilter(field_name="registered_capital", lookup_expr='gte')
	#最大资本
	max_price = filters.NumberFilter(field_name="registered_capital", lookup_expr='lte')
