# -*- coding:utf-8 -*-
import urllib2
import json
from b5c_interface.excelLoad import *

__author__ = '不懂'


class HttpService:
    def __init__(self):
        self.header = {}
        self.data = {}
        self.url = None

    def get_header(self):
        return self.header

    def set_header(self, header):
        self.header = eval(header)  # unicode 转 dict

    def get_data(self):
        return self.data

    def set_data(self, data):
        if data.lower() == 'none':
            self.data = data
        else:
            self.data = json.dumps(eval(data))  # 转换成json data post

    def get_url(self):
        return self.url

    def set_url(self, url):
        self.url = url

    def request_get(self):
        """get请求"""
        try:
            response = urllib2.urlopen(self.url)
            content = json.loads(response.read())
            return content
        except Exception, e:
            print str(e)
            return {}

    def set_all(self, url, data, header):
        self.set_url(url)
        self.set_data(data)
        self.set_header(header)

    def request_post(self):
        """post请求"""
        try:
            req = urllib2.Request(url=self.url, headers=self.header, data=self.data)
            response = urllib2.urlopen(req)
            content = json.loads(response.read())
            return content
        except Exception, e:
            print str(e)
            return {}

    @staticmethod
    def test_http():
        """测试代码"""
        """get methond"""
        exc = Excel()
        test_data = exc.row_data()
        b = HttpService()
        url1 = test_data[0]['Request Url']
        b.set_url(url1)
        req1 = b.request_get()
        print req1['data']['gudsId']
        print eval(req1['data']['gudsNewPrices'])[0]['price']
        print '-' * 30
        # print str(req)

        """post method"""
        a = HttpService()
        url2 = test_data[1]['Request Url'].encode("utf-8")
        data = test_data[1]['Data']
        header = test_data[1]['Header']
        a.set_all(url2, data, header)
        b = a.request_post()
        print json.dumps(b)  # 去除'u'
        print type(b)
        print type(b)
        print b['msg']
        print b['code']
        print b['data']

if __name__ == '__main__':
   HttpService.test_http()






