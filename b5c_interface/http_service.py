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
        self.log = Log()

    def get_header(self):
        return self.header

    def set_header(self, header):
        self.header = eval(header)  # unicode 转 dict
        self.log.info('set header successfully, current url is: ' + self.url)

    def get_data(self):
        return self.data

    def set_data(self, data):
        if data.lower() == 'none':
            self.data = data
            self.log.info('current DATA is NONE')
        else:
            self.data = json.dumps(eval(data))  # 转换成json data post
            self.log.info('set DATA successfully!!')

    def get_url(self):
        return self.url

    def set_url(self, url):
        self.url = url
        self.log.info('set URL successfully, current url is: ' + self.url)

    def request_get(self):
        """get请求"""
        # response = urllib2.urlopen(self.url)
        # content = json.loads(response.read())
        # self.log.info('get method ')
        # return content
        try:
            response = urllib2.urlopen(self.url)
            content = json.loads(response.read())
            self.log.info('GET method successfully!!')
            return content
        except Exception, e:
            self.log.error('GET method failed, error is: ' + str(e))
            return {}
        # raise Exception

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
            self.log.info('POST method successfully!!')
            return content
        except Exception, e:
            self.log.error('POST method failed, error is: ' + str(e))
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






