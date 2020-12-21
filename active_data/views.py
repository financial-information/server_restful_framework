from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

import numpy as np
# 获取pandas各种数据格式以及状态
from pandas import Series
import pandas as pd
#获取jqdata平台数据
import jqdatasdk as jq
#json数据的转换包
import json
#对excel文件进行处理
import xlrd
# 用来获取文件路径
import os


class JQData:
  def __init__(self, name="账号", password="密码"):
    #登陆
    jq.auth(name, password)

  def valid(self):
    # 如果该账号没有可用数据条数了就返回False
    if jq.get_query_count()['spare'] > 0:
      return True
    else :
      return False

  def exponent_data(self, stock_code, start_time, end_time):
    #获取数据
    data = jq.get_price(stock_code, start_date=start_time, end_date=end_time)
    # 获取第index列，也就是第0列
    mydate = data.index
    # 这个数组用来在原来的数据上再加一列
    add_list = []
    for i in range(mydate.size):
      # 将原来的时间数据转化程字符串数据，这样才可以存放到json中
      add_list.append(mydate[i].strftime("%Y/%m/%d"))

    # 这个数组用来替换index列  data_1、data_2
    date_list = ["data_" + str(i) for i in range(mydate.size)]
    data.index = Series(date_list)
    # 将得到的时间数据加入到data中
    data['time'] = add_list
    # 变成json
    json_data = data.to_json()
    # 还原成字典对象返回
    return json.loads(json_data)

#获取行情指数
def getExponentDataByCode(request):
  result = dict()
  result["success"] = False
  # 方法是否为POST
  if request.method == "POST":
    #对应参数是否存在
    if request.POST and request.POST.get('stock_code') and request.POST.get('start_time') and request.POST.get('end_time'):
      # 赋值
      stock_code = request.POST['stock_code']
      start_time = request.POST['start_time']
      end_time = request.POST['end_time']
      result["success"] = True
      result["stock_code"] = stock_code
      # 创建对象
      myjq = JQData()
      if myjq.valid():
        result["result"] = myjq.exponent_data(stock_code, start_time, end_time)
      else:
        result["result"] = "账号可用的数据条数没了"
      return HttpResponse(json.dumps(result), content_type="application/json")
    else:
      result["message"] = "传输参数格式错误"
      return HttpResponse(json.dumps(result), content_type="application/json")

  else:
    result["message"] = "传输方法错误"
    return HttpResponse(json.dumps(result), content_type="application/json")
    

# 处理execel文件
def handleData(exponent_type):
  # 路径
  base_url = os.getcwd()
  # 上证
  if exponent_type == 1:
    base_url += "/static/file/exponent_XSHG_type.xlsx"
  # 深证
  else :
    base_url += "/static/file/exponent_XSHE_type.xlsx"
  #获取文件
  file = xlrd.open_workbook(base_url)
  # 获取表格
  table = file.sheets()[0]
  # 获取行数
  nrows = table.nrows
  
  result_arr = []
  # 循环+赋值
  for i in range(2, nrows):
      obj = dict()
      obj["value"] = str(table.row(i)[0]).replace("'", "").replace("text:", "")
      obj["label"] = str(table.row(i)[1]).replace("'", "").replace("text:", "")
      result_arr.append(obj)
  return result_arr

# 获取上海市场指数列表
def getXSHGExponentType(request):
  result = {}
  result["success"] = True
  result["result"] = handleData(1)
  return HttpResponse(json.dumps(result), content_type="application/json")

# 获取深圳市场指数列表
def getXSHEExponentType(request):
  result = {}
  result["success"] = True
  result["result"] = handleData(0)
  return HttpResponse(json.dumps(result), content_type="application/json")
