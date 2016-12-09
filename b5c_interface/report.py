# -*- coding: utf-8 -*-
import os
import time
from pyh import *
import sys
from mysql import *


__author__ = '不懂'


class HTMLReport:
    def __init__(self):
        self.title = 'Interface Test Report'  # 网页标签名称
        self.filename = ''  # 结果文件名
        self.time_took = 0  # 测试耗时
        self.pass_num = 0  # 测试通过的用例数
        self.fail_num = 0  # 测试失败的用例数
        self.total_case_num = 0  # 运行测试用例总数
        self.sql = MySQL()
        self.log = Log()

    @staticmethod
    # 获取报告名字
    def get_report_name():
        report_name = 'B5C_interface_report_' + time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime())
        return report_name

    def get_passed_case(self):
        sq = "SELECT COUNT(*) FROM test_data WHERE status = 'pass'"
        return self.sql.select(sq)[0][0]

    def get_failed_case(self):
        sq = "SELECT COUNT(*) FROM test_data WHERE status = 'fail'"
        return self.sql.select(sq)[0][0]

    def get_total_case(self):
        sq = "SELECT COUNT(*) FROM test_data"
        return self.sql.select(sq)[0][0]

    def get_all_data(self):
        sq = "SELECT * FROM test_data"
        return self.sql.select(sq)

    def generate_report(self, start_time='00:00:00', end_time='00:00:00', show_end_time=0):
        # 定义报告变量
        self.time_took = round(show_end_time, 2)
        self.filename = self.get_report_name()
        self.pass_num = self.get_passed_case()
        self.fail_num = self.get_failed_case()
        self.total_case_num = self.get_total_case()

        # pyh生成html代码
        page = PyH(self.title)
        page << h1('接口测试报告', align='center')  # 标题居中
        page << p('开始时间：' + str(start_time))
        page << p('结束时间：' + str(end_time))
        page << p('测试总耗时：' + str(self.time_took) + 's')
        page << p('测试用例数：' + str(self.total_case_num) + '&nbsp' * 10 + '成功用例数：' + str(self.pass_num)
                  + '&nbsp' * 10 + '失败用例数：' + str(self.fail_num))
        tab = table(border='1', cellpadding='1', cellspacing='0', cl='table')
        tab1 = page << tab
        tab1 << tr(td('用例ID', bgcolor='#ABABAB', align='center')
                   + td('接口描述', bgcolor='#ABABAB', align='center')
                   + td('请求URL', bgcolor='#ABABAB', align='center')
                   + td('方法', bgcolor='#ABABAB', align='center')
                   + td('请求数据', bgcolor='#ABABAB', align='center')
                   + td('返回值', bgcolor='#ABABAB', align='center')
                   + td('返回信息', bgcolor='#ABABAB', align='center')
                   + td('用例状态', bgcolor='#ABABAB', align='center'))

        data = self.get_all_data()
        for row in data:
            # 设置status颜色
            if str(row[17].lower()) == 'pass':
                font_colour = 'color:#64A600'  # 绿色
            elif str(row[17].lower()) == 'fail':
                font_colour = 'color:#FF2D2D'  # 红色

            # 生成报告数据
            tab1 << tr(td(int(row[1]), align='center') + td(row[2]) +
                       td(row[3]) + td(row[4], align='center') +
                       td(row[6], align='center') + td(row[14], align='center') + td(row[15]) +
                       td(row[17], style=font_colour, align='center'))
            page << p('<br/>')

        # 生成报告文件
        try:
            page.printOut('..\\report\\' + self.filename + '.html')
            self.log.info('report is generated successfully!!')
        except Exception, e:
            self.log.error('report is failed!!, reason is: ' + str(e))
        self.sql.close()


if __name__ == '__main__':
    a= HTMLReport()
    b = a.get_passed_case()
    c = a.get_failed_case()
    d = a.get_total_case()
    a.generate_report()
    print b, type(b)
    print c, type(c)
    print d, type(d)
