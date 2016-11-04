# -*- coding:utf-8 -*-

import urllib
import urllib2
import json
url = 'http://i.b5cai.com/logistics/calculateLogisticsFee.json'
values = {"adprAddr":"\u6c5f\u82cf\u7701","transCheCd":"FISHER","tbMsOrdGudsOptDtos":[{"gudsId":"80003734","sllrId":"kgc","ordGudsQty":"1"}]}
header = {'content-type': 'application/json', 'cache-control': 'no-cache', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'}
#  'Content-Type': 'text/plain;charset=UTF-8', 'Content-Type': 'application/x-www-form-urlencoded
url2 = 'http://i.b5cai.com/goods/detail.json?sllrId=ponymemebox&gudsId=80000260&custId=13701705936'

# print url
# req = urllib2.Request(url2, headers=header)
# res = urllib2.urlopen(req)
# a = res.read()
# print a
# print values
# print type(values)
jdata = json.dumps(values)  # 转换成json data post
print jdata
print type(jdata)
req = urllib2.Request(url, headers=header, data=jdata)
response = urllib2.urlopen(req)
the_page = response.read()
print the_page
print type(the_page)

