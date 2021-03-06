# -*- coding:utf-8 -*-
import ConfigParser

__author__ = '不懂'


# 定义结构体
class DataStruct:
    """于接收读取的测试数据,记录要写入测试报告的数据"""
    def __init__(self):
        cf = ConfigParser.ConfigParser()
        cf.read(r'..\run_mode.ini')
        self.case_id = 0       # 用例ID
        self.description = ''  # 接口描述
        self.request_url = ''  # 接口请求url
        self.http_method = ''  # 接口http方法
        self.run_type = ''     # 定义运行方法
        self.data = ''         # 测试数据
        self.header = ''       # header
        self.assert_1 = ''     # 需要检测的内容1
        self.assert_1_db = ''  # 存入DB值
        self.assert_1_value = ''    # 内容1返回值
        self.assert_2 = ''     # 需要检测的内容2
        self.assert_2_db = ''  # 存入DB值
        self.assert_2_value = ''    # 内容2返回值
        self.assert_3 = ''     # 需要检测的内容3
        self.assert_3_db = ''  # 存入DB值
        self.assert_3_value = ''    # 内容3返回值
        self.return_code = ''  # 返回值
        self.return_msg = ''   # 返回信息
        self.return_data = ''  # 返回数据
        self.status = ''       # 用例状态
        self.error_msg = ''    # 错误信息
        self.request_environment = cf.get('RUNMODE', 'api_environment')  # 接口请求环境
