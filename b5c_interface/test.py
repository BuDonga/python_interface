# -*- coding: utf-8 -*-

import os
import time
from pyh import *
import sys
from mysql import *


class HTMLReport:
    def __init__(self, cursor):
        self.title = 'test_report'  # 网页标签名称
        self.filename = ''  # 结果文件名
        self.time_took = '00:00:00'  # 测试耗时
        self.success_num = 1  # 测试通过的用例数
        self.fail_num = 2  # 测试失败的用例数
        self.error_num = 3  # 运行出错的用例数
        self.case_total = 4  # 运行测试用例总数


if __name__ == '__main__':
    # a = MySQL()
    # sql = "SELECT * FROM test_data"
    # #sql = "SELECT Case_ID, Description, Request_URL, Method, Run_Type, Data, Header,  Assert_1, Assert_1_Value,  Assert_2, Assert_2_Value,  Assert_3, Assert_3_Value, Return_Code, Return_Msg, Return_Data, Status FROM test_data"
    # data = a.select(sql)
    # page = PyH('my python')
    # page << h1('My big title!', cl='myCSSclass')
    # page << div(id='mySubtitleDiv') << h2('My sub-title')
    # maindiv = page << div(id='myMainDiv')
    # maindiv << h3('A smaller title') + p('followed by a small paragraph')
    # maindiv << p('Main paragraph ', style='color:red;') << a('a link', href='http://alink')
    # maindiv << span('hehe', onclick='myJavaScriptFcn(); return false;')
    # maindiv << br()
    # maindiv << img(src='mypicture.jpg')
    # page << div(id='myFooter') << span('My footer')
    # page.printOut('sd1f.html')
    # page << h1('帮5采接口测试报告', align='center')  # 标题居中
    # page << p('测试总耗时：' + '总耗时')
    # page << p('测试用例数：' + str('用李树') + '&nbsp' * 10 + '成功用例数：' + str('成功'))
    # tab = table(border='1', cellpadding='1', cellspacing='0', cl='table')
    # tab1 = page << tab
    # tab1 << tr(td('用例ID', bgcolor='#ABABAB', align='center')
    #            + td('接口描述', bgcolor='#ABABAB', align='center')
    #            + td('请求URL', bgcolor='#ABABAB', align='center')
    #            + td('方法', bgcolor='#ABABAB', align='center')
    #            + td('请求数据', bgcolor='#ABABAB', align='center')
    #            + td('返回值', bgcolor='#ABABAB', align='center')
    #            + td('返回信息', bgcolor='#ABABAB', align='center')
    #            + td('用例状态', bgcolor='#ABABAB', align='center'))
    # for row in data:
    #     # 设置status颜色
    #     if str(row[17].lower()) == 'pass':
    #         font_colour = 'color:#64A600'  # 绿色
    #     elif str(row[17].lower()) == 'fail':
    #         font_colour = 'color:#FF2D2D'  # 红色
    #     tab1 << tr(td(int(row[1]), align='center') + td(row[2]) +
    #                td(row[3]) + td(row[4], align='center') +
    #                td(row[6], align='center') + td(row[14], align='center') + td(row[15]) +
    #                td(row[17], style=font_colour, align='center'))
    # page.printOut('sd1f.html')
    cf = ConfigParser.ConfigParser()
    cf.read(r'..\db_config.ini')
    cf.get()