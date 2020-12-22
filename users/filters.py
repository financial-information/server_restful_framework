
from rest_framework import mixins, generics, permissions, viewsets, renderers
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from company_database.models import CompanyBasicInformation

class UserInfoFilter(filters.FilterSet):
	user_phone = filters.CharFilter(field_name ="phone")
	username = filters.CharFilter(field_name = "username")

class UserHistoryFilter(filters.FilterSet):
	#对name进行模糊查询,类似于sql里面的like语句，如果不指定lookup_expr就是完全匹配
	user_phone = filters.CharFilter(field_name="user_phone")
	history_module_type = filters.CharFilter(field_name="history_module_type")
	history_module_id = filters.CharFilter(field_name="history_module_id")


class UserCollectionFilter(filters.FilterSet):
	#对name进行模糊查询,类似于sql里面的like语句，如果不指定lookup_expr就是完全匹配
	user_phone = filters.CharFilter(field_name="user_phone")
	collection_module_type = filters.CharFilter(field_name="history_module_type")
	collection_module_id = filters.CharFilter(field_name="history_module_id")