# -*- coding: utf-8 -*-
import unittest
from b5c_interface.data_structure import *
from b5c_interface.excelLoad import *
from b5c_interface.http_service import *
from b5c_interface.mysql import *

__author__ = '不懂'


class Run(unittest.TestCase):
    def setUp(self):
        self.exc = Excel()
        self.row_data = self.exc.row_data()  # 返回所有excel的行数据，与列名成键值对
        self.msql = MySQL()
        self.msql.delete("TRUNCATE TABLE `test_data`")  # 删除所有数据
        self.http = HttpService()

    def tearDown(self):
        self.msql.close()

    def test_run_case(self):
        """循环case"""
        """获取excel中的值"""
        for case in self.row_data:
            self.ds = DataStruct()  # 初始化结构体
            try:
                self.ds.case_id = int(case['Case ID'])
                self.ds.description = case['Description']
                self.ds.request_url = ''.join(str(self.ds.request_environment + case['Request Url']))
                self.ds.http_method = case['Method']
                self.ds.run_type = case['Run Type']
                self.ds.data = case['Data']
                self.ds.header = case['Header']

                """设置参数"""
                self.http.set_all(self.ds.request_url, self.ds.data, self.ds.header)

                """调用接口"""
                if self.ds.http_method.lower() == 'get':
                    req = self.http.request_get()
                elif self.ds.http_method.lower() == 'post':
                    req = self.http.request_post()

                """获取返回值"""
                self.ds.return_code = req['code']
                self.ds.return_data = json.dumps(req['data'])  # 去除'u'
                self.ds.return_data = self.ds.return_data.replace('\'', '')  # 去除特殊符号'，如果数据带这个特殊符号会导致写入DB报错，what the fuck! 大坑！！！！
                print self.ds.return_data
                print '*' * 100
                self.ds.return_msg = req['msg']
                """写入excel，同时结果写入DB"""
                try:
                    if not (self.assertEquals(self.ds.return_code, 2000) or self.assertEquals(self.ds.return_msg,
                                                                                              'success')):
                        self.deal_ok()
                except Exception, e:
                    print e
                    raise Exception
            except Exception, e:
                """如果抛出异常则把用例的数据写入DB"""
                self.deal_exception(e)
                print 'parameter wrong with %s test case' % self.ds.case_id
                print str(e)
                print '*' * 100

    def deal_ok(self):
        self.exc.write_return_data(self.ds.case_id, self.ds.return_data)
        self.exc.write_return_message(self.ds.case_id, self.ds.return_msg)
        self.exc.write_return_code(self.ds.case_id, self.ds.return_code)
        self.exc.write_return_status(self.ds.case_id, 'pass')
        self.msql.insert(
            "INSERT INTO `test_data` (`Case_ID`, `Description`, `Request_URL`, `Method`, `Run_Type`, `Data`, `Header`, `Return_Code`, `Return_Msg`, `Return_Data`, `Status`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
                self.ds.case_id, self.ds.description, self.ds.request_url, self.ds.http_method,
                self.ds.run_type, self.ds.data, self.ds.header, self.ds.return_code, self.ds.return_msg,
                self.ds.return_data, 'pass'))
        print 'ok'

    def deal_exception(self, msg):
        self.ds.error_msg = str(msg)
        if not self.ds.return_code:
            self.ds.return_code = 0
        self.exc.write_return_data(self.ds.case_id, self.ds.return_data)
        self.exc.write_return_message(self.ds.case_id, self.ds.error_msg)
        self.exc.write_return_code(self.ds.case_id, self.ds.return_code)
        self.exc.write_return_status(self.ds.case_id, 'fail')
        self.msql.insert(
            "INSERT INTO `test_data` (`Case_ID`, `Description`, `Request_URL`, `Method`, `Run_Type`, `Data`, `Header`, `Return_Code`, `Return_Msg`, `Return_Data`, `Status`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
                self.ds.case_id, self.ds.description, self.ds.request_url, self.ds.http_method,
                self.ds.run_type, self.ds.data, self.ds.header, self.ds.return_code, self.ds.error_msg,
                '', 'fail'))

if __name__ == '__main__':
    unittest.main()

