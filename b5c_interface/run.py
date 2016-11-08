# -*- coding: utf-8 -*-
import unittest
from b5c_interface.data_structure import *
from b5c_interface.excelLoad import *
from b5c_interface.http_service import *
from b5c_interface.mysql import *


class Run(unittest.TestCase):
    def setUp(self):
        self.exc = Excel()
        self.row_data = self.exc.row_data()  # 返回所有excel的行数据，与列名成键值对
        self.msql = MySQL()
        self.msql.delete("TRUNCATE TABLE `test_data`")  # 删除所有数据
        self.http = HttpService()
        self.ds = DataStruct()  # 结构体

    def tearDown(self):
        self.msql.close()

    def test_run_case(self):
        """循环case"""
        """获取excel中的值"""
        for case in self.row_data:
            try:
                self.ds.case_id = int(case['Case ID'])
                self.ds.description = case['Description']
                self.ds.request_url = case['Request Url']
                self.ds.http_method = case['Method']
                self.ds.run_type = case['Run Type']
                self.ds.data = case['Data']
                self.ds.header = case['Header']

                """设置参数"""
                self.http.set_all(self.ds.request_url, self.ds.data, self.ds.header)

                """调用接口"""
                try:
                    if self.ds.http_method.lower() == 'get':
                        req = self.http.request_get()
                    elif self.ds.http_method.lower() == 'post':
                        req = self.http.request_post()
                except Exception, e:
                    print '接口调用失败'
                    print e

                """获取返回值"""
                self.ds.return_code = req['code']
                self.ds.return_data = json.dumps(req['data'])  # 去除'u'
                print '*' * 100
                self.ds.return_msg = req['msg']
                """写入excel，同时结果写入DB"""
                try:
                    if not (self.assertEquals(self.ds.return_code, 2000) or self.assertEquals(self.ds.return_msg,
                                                                                              'success')):
                        self.exc.write_return_data(self.ds.case_id, self.ds.return_data)
                        self.exc.write_return_message(self.ds.case_id, self.ds.return_msg)
                        self.exc.write_return_code(self.ds.case_id, self.ds.return_code)
                        self.exc.write_return_status(self.ds.case_id, 'pass')
                        self.msql.insert(
                            "INSERT INTO `test_data` (`Case_ID`, `Description`, `Request_URL`, `Method`, `Run_Type`, `Data`, `Header`, `Return_Code`, `Return_Msg`, `Return_Data`, `Status`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
                                self.ds.case_id, self.ds.description, self.ds.request_url, self.ds.http_method,
                                self.ds.run_type, self.ds.data, self.ds.header, self.ds.return_code, self.ds.return_msg,
                                self.ds.return_data, 'pass'))
                except Exception, e:
                    self.exc.write_return_data(self.ds.case_id, self.ds.return_data)
                    self.exc.write_return_message(self.ds.case_id, self.ds.return_msg)
                    self.exc.write_return_code(self.ds.case_id, self.ds.return_code)
                    self.exc.write_return_status(self.ds.case_id, 'fail')
                    self.msql.insert(
                        "INSERT INTO `test_data` (`Case_ID`, `Description`, `Request_URL`, `Method`, `Run_Type`, `Data`, `Header`, `Return_Code`, `Return_Msg`, `Return_Data`, `Status`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
                            self.ds.case_id, self.ds.description, self.ds.request_url, self.ds.http_method,
                            self.ds.run_type, self.ds.data, self.ds.header, self.ds.return_code, self.ds.return_msg,
                            self.ds.return_data, 'fail'))
                    print e
            except Exception, e:
                """如果抛出异常则把用例的数据写入DB"""
                self.msql.insert(
                "INSERT INTO `test_data` (`Case_ID`, `Description`, `Request_URL`, `Method`, `Run_Type`, `Data`, `Header`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
                    self.ds.case_id, self.ds.description, self.ds.request_url, self.ds.http_method, self.ds.run_type, self.ds.data, self.ds.header))
                print e
                print 'parameter wrong with %s test case' % self.ds.case_id
                print '*' * 100

if __name__ == '__main__':
    unittest.main()

