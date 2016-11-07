# -*- coding: utf-8 -*-
import unittest
from b5c_interface.data_structure import *
from b5c_interface.excelLoad import *
from b5c_interface.http_service import *
from b5c_interface.mysql import *


class Run(unittest.TestCase):
    def setUp(self):
        self.exc = Excel()
        self.exc.to_db()  # 把所有excel写入DB
        self.row_data = self.exc.row_data()  # 返回所有excel的行数据，与列名成键值对
        self.msql = MySQL()
        self.http = HttpService()
        self.ds = DataStruct()

    def tearDown(self):
        pass

    def test_run_case(self):
        u"""登录"""
        ggg = self.row_data
        print ggg
        # self.m.login('15921826291', 'qq5566')
        # try:
        #     if not self.assertEqual('awdadasd', self.e.login_name_after().text, '用户名不对'):
        #         print 'login is success'
        #         logging.info('login is success')
        # except Exception, e:
        #         self.f.get_snapshot('not_login_success')
        #         logging.error(e)
        #         raise AssertionError


if __name__ == '__main__':
    unittest.main()

