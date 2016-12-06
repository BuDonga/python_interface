# -*- coding: utf-8 -*-

import os
import time
from pyh import *


class HTMLReport:
    def __init__(self, cursor):
        self.title = 'test_report_page'  # 网页标签名称
        self.filename = ''  # 结果文件名
        self.time_took = '00:00:00'  # 测试耗时
        self.success_num = 1  # 测试通过的用例数
        self.fail_num = 2  # 测试失败的用例数
        self.error_num = 3  # 运行出错的用例数
        self.case_total = 4  # 运行测试用例总数
        self.cursor = cursor


if __name__ == '__main__':
    page = PyH('my python')
    page << h1('My big title!', cl='myCSSclass')
    page << div(id='mySubtitleDiv') << h2('My sub-title')
    maindiv = page << div(id='myMainDiv')
    maindiv << h3('A smaller title') + p('followed by a small paragraph')
    maindiv << p('Main paragraph ', style='color:red;') << a('a link', href='http://alink')
    maindiv << span('hehe', onclick='myJavaScriptFcn(); return false;')
    maindiv << br()
    maindiv << img(src='mypicture.jpg')
    page << div(id='myFooter') << span('My footer')
    page.printOut('sd1f.html')
