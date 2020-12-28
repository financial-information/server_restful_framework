from django.shortcuts import render

from django.shortcuts import get_list_or_404, get_object_or_404

#返回值
from django.http import HttpResponse

#读excel
import xlrd
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
# 过滤器
from django_filters.rest_framework import DjangoFilterBackend

# 引入模型
from company_database.models import CompanyBasicInformation,CompanyFinanceData
# 引入序列
from company_database.serializers import CompanyBasicInformationSerializer,CompanyFinanceDataSerializer
# 引入过滤器
from company_database.filters import CompanyBasicInformationFilter
# 分页
from rest_framework.pagination import LimitOffsetPagination


# rest_framework cbv 查询方式
# 公司基本信息视图集

class CompanyBasicInformationViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    # 用于详细查询的字段，当下为股票的名字展示股票的内容
    # lookup_field = "stock_name"
    queryset = CompanyBasicInformation.objects.all()
    serializer_class = CompanyBasicInformationSerializer
    filter_class = CompanyBasicInformationFilter
    # 分页
    pagination_class = LimitOffsetPagination


# 年报视图集
class CompanyFinanceDataViewSet(viewsets.ModelViewSet):
	# 用于详细查询的字段，当下为股票的名字展示股票的内容
	queryset = CompanyFinanceData.objects.all()
	serializer_class = CompanyFinanceDataSerializer
	pagination_class = LimitOffsetPagination
	# 支持搜索和过滤，写在一起
	filter_backends = (filters.SearchFilter, DjangoFilterBackend)
	# 搜索的关键字从这些字段取
	search_fields = ('id','stock_code')



def listCompanyBasicInfo(request):
	if request.method == "GET":
		id = request.GET['id']
		queryset = CompanyBasicInformation.objects.filter('id' == id).first()



# =============================静态数据存入数据库 ===========================================

# 数据所在位置r
# 根目录（注意：将此处路径修改为数据存放位置）
# <<<<<<< HEAD
BASIC_URL = "C:/Users/黑子/Desktop/大三/金融信息系统/"
# =======
# BASIC_URL = "C:/Users/user/Documents/Tencent Files/540269559/FileRecv/static/"
# 公司基本信息
COMPANY_BASIC_DATA_URL = BASIC_URL+"全部AB股公司基本信息.xls"
# 年报数据
FINANCE_DTAT_URL = BASIC_URL+"全部AB股的报表.xls"
# 股票数据
STOCK_URL_LIST = [
	BASIC_URL+"全部A股.xls",
	BASIC_URL+"上证A股.xls",
	BASIC_URL+"深证A股.xls",
	BASIC_URL+"中小企业板.xls",
	BASIC_URL+"创业板.xls",
	BASIC_URL+"科创板.xls",       
	BASIC_URL+"深证主板A股.xls",       
	BASIC_URL+"全部B股.xls",       
	BASIC_URL+"上证B股.xls",
	BASIC_URL+"深证B股.xls",
	BASIC_URL+"全部AB股.xls",
	BASIC_URL+"上证AB股.xls",
	BASIC_URL+"深证AB股.xls",
]
# 行业数据根目录
INDUSTRY_URL = BASIC_URL+"行业/"
# 行业数据子目录
INDUSTRY_URL_LIST = [
	INDUSTRY_URL+"采矿业.xls",
	INDUSTRY_URL+"电力、热力、燃气及水生产和供应业.xls",
	INDUSTRY_URL+"房地产业.xls",
	INDUSTRY_URL+"建筑业.xls",
	INDUSTRY_URL+"交通运输、仓储和邮政业.xls",
	INDUSTRY_URL+"教育.xls",       
	INDUSTRY_URL+"金融业.xls",       
	INDUSTRY_URL+"居民服务、修理和其他服务业.xls",       
	INDUSTRY_URL+"科学研究和技术服务业.xls",
	INDUSTRY_URL+"农、林、牧、渔业.xls",
	INDUSTRY_URL+"批发和零售业.xls",
	INDUSTRY_URL+"水利、环境和公共设施管理业.xls",
	INDUSTRY_URL+"卫生和社会工作.xls",
	INDUSTRY_URL+"文化、体育和娱乐业.xls",
	INDUSTRY_URL+"信息传输、软件和信息技术服务业.xls",
	INDUSTRY_URL+"制造业.xls",
	INDUSTRY_URL+"住宿和餐饮业.xls",
	INDUSTRY_URL+"租赁和商务服务业.xls",
]
# 行业名称
INDUSTRY_NMAE = [
	"采矿业",
	"电力、热力、燃气及水生产和供应业",
	"房地产业",
	"建筑业",
	"交通运输、仓储和邮政业",
	"教育",       
	"金融业",       
	"居民服务、修理和其他服务业",       
	"科学研究和技术服务业",
	"农、林、牧、渔业",
	"批发和零售业",
	"水利、环境和公共设施管理业",
	"卫生和社会工作",
	"文化、体育和娱乐业",
	"信息传输、软件和信息技术服务业",
	"制造业",
	"住宿和餐饮业",
	"租赁和商务服务业",
]


# 打开excel，将数据list化
def readXls(file_name):
	data = xlrd.open_workbook(file_name)
	table = data.sheets()[0]
	rows = table.nrows
	cols=table.ncols
	list_data = []
	for v in range(1,rows):
		values = table.row_values(v)
		row_data = []
		for col in range(0,cols):
			row_data.append(str(values[col]))
		list_data.append(row_data)
	return list_data


# 检测数据是否合格
def checkCondition(item):
	if(item == "--" or item == '-'):
		return ''
	else:
		return item

# 拼接年报数据
def connectStr(items):
	return_str = ""
	for item in items:
		if(item == "--" or item == '-'):
			return_str = return_str+";"
		else:
			return_str = return_str+item+";"
	return return_str

# 公司基本信息存入
def saveCompanyData(file_name):
	list_data = readXls(file_name)
	for items in list_data:
		cbi = CompanyBasicInformation()
		cbi.stock_code = checkCondition(items[0])
		cbi.stock_name = checkCondition(items[1])
		cbi.credit_code = checkCondition(items[2])
		cbi.company_name = checkCondition(items[3])
		cbi.found_date = checkCondition(items[4])
		cbi.business_code = checkCondition(items[5])
		cbi.registered_capital = checkCondition(items[6])
		cbi.legal_representative = checkCondition(items[7])
		cbi.phone = checkCondition(items[8]).split(';')[0]
		cbi.registered_address = checkCondition(items[9])
		cbi.website = checkCondition(items[10]).split(';')[0]
		cbi.profile = checkCondition(items[11])
		cbi.stock_type = ''
		cbi.business_scope = checkCondition(items[12])
		cbi.listed = 0
		cbi.deteled = 0
		try:
			cbi.save()
		except BaseException as reason:
			print("error"+str(reason))

# 年报存入
def saveFinanceData(file_name):
	list_data = readXls(file_name)
	for items in list_data:
		cfd = CompanyFinanceData()
		cfd.stock_code = items[0]
		cfd.stock_name = items[1]
		cfd.total_share_capital = checkCondition(items[2])
		cfd.total_assets_turnover = connectStr(items[3:9])
		cfd.roa = connectStr(items[9:15])
		cfd.total_assets = connectStr(items[15:21])
		cfd.total_liabilities = connectStr(items[21:27])
		cfd.asset_liability_ratio = connectStr(items[27:33])
		cfd.net_profit = connectStr(items[33:39])
		cfd.net_assets = connectStr(items[39:45])
		cfd.roe = connectStr(items[45:51])
		cfd.total_profit = connectStr(items[51:57])
		cfd.current_ratio = connectStr(items[57:63])
		cfd.net_assets_per_share = connectStr(items[63:69])
		cfd.operating_income_per_share = connectStr(items[69:75])
		cfd.enterprise_value = checkCondition(items[75])
		cfd.equity_multiplier = connectStr(items[76:82])
		cfd.cash_return = connectStr(items[82:88])
		cfd.quick_ratio = connectStr(items[88:94])
		cfd.sale_net_profit = connectStr(items[94:100])
		cfd.forecast_earnings = checkCondition(items[100])
		cfd.forecast_net_profit = checkCondition(items[101])
		cfd.forecast_main_business_income = checkCondition(items[102])
		cfd.forecast_earnings_before_tax = checkCondition(items[103])
		cfd.forecast_cash_flow = checkCondition(items[104])
		cfd.forecast_total_profit = checkCondition(items[105])
		cfd.forecast_operating_profit = checkCondition(items[106])
		cfd.operating_profit_total = connectStr(items[107:113])
		cfd.cash_ratio = connectStr(items[113:119])
		cfd.cash_flow = connectStr(items[119:125])
		cfd.inventory_turnover_days = connectStr(items[125:131])
		cfd.current_assets_turnover_days = connectStr(items[131:137])
		cfd.sales_outstanding_turnover_days = connectStr(items[137:143])
		cfd.shareholders_equity_ratio = connectStr(items[143:149])
		cfd.beta = checkCondition(items[149])
		cfd.annualized_rate_return = checkCondition(items[150])
		cfd.annualized_volatility = checkCondition(items[151])
		try:
			cfd.save()
		except BaseException as reason:
			print("error"+str(reason))

	
# 区分板块：stock_type 和 industry_type
def disStockPlates(file_name):
	s_list_data = readXls(file_name)
	company_all_data = CompanyBasicInformation.objects.all()
	for item in company_all_data:
		judge = 0
		for ld in s_list_data:
			if(item.stock_code == ld[0]):
				judge = 1
				break
		c = CompanyBasicInformation.objects.filter(stock_code = item.stock_code)
		now = c.first().stock_type
		if judge == 1: 
			c.update(stock_type = now + "1")
		else:
			c.update(stock_type = now + "0")


# 初始化stock_code 和 industry_type 字段
def initStockData():
	company_all_data = CompanyBasicInformation.objects.all()
	for item in company_all_data:
		c = CompanyBasicInformation.objects.filter(stock_code = item.stock_code)
		c.update(stock_type = '')# 将stock_code置为空

# 初始化，然后区分模块
def fillStockType(stock_list):
	#初始化
	initStockData()
	#股票区分
	for url in stock_list:
		disStockPlates(url)

# 区分板块：stock_type 和 industry_type
def disIndustryPlates(file_name,index):
	s_list_data = readXls(file_name)
	company_all_data = CompanyBasicInformation.objects.all()
	for item in company_all_data:
		judge = 0
		for ld in s_list_data:
			if(item.stock_code == ld[0]):
				judge = 1
				break
		if judge == 1: 
			c = CompanyBasicInformation.objects.filter(stock_code = item.stock_code)
			c.update(industry_type = INDUSTRY_NMAE[index])

# 初始化stock_code 和 industry_type 字段
def initIndustryData():
	company_all_data = CompanyBasicInformation.objects.all()
	for item in company_all_data:
		c = CompanyBasicInformation.objects.filter(stock_code = item.stock_code)
		c.update(industry_type ='其他')# 将industry_type置为空

def fillIndustryType(industry_list):
	#初始化
	initIndustryData()
	#取模块名
	#行业区分
	index = 0
	for url in industry_list:
		disIndustryPlates(url,index)
		index = index + 1

# 存储静态数据
# 存出公司基本信息
def saveCompanyBasicData(request):
	# 注：已经进行数据存储可以不用重复存入数据库，需要那一部分则调用哪一部分
	# # 存公司基本信息
	saveCompanyData(COMPANY_BASIC_DATA_URL)
	return HttpResponse("success!!!")

def saveCompanyFinanceData(request):
	# # 存年报
	saveFinanceData(FINANCE_DTAT_URL)
	return HttpResponse("success!!!")

def saveStockType(request):
	# 存股票类型
	fillStockType(STOCK_URL_LIST)
	return HttpResponse("success!!!")

def saveIndustryType(request):
	# 存行业类型
	fillIndustryType(INDUSTRY_URL_LIST)
	return HttpResponse("success!!!")