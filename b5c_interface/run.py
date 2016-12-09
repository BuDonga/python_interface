# -*- coding: utf-8 -*-
import unittest
from b5c_interface.data_structure import *
from b5c_interface.excelLoad import *
from b5c_interface.http_service import *
from b5c_interface.mysql import *
import sys
import time


__author__ = '不懂'


class Run(unittest.TestCase):
    def setUp(self):
        reload(sys)
        sys.setdefaultencoding("utf-8")
        cf = ConfigParser.ConfigParser()
        cf.read(r'..\run_mode.ini')
        self.need_report = cf.get('RUNMODE', 'need_report')
        self.need_mail = cf.get('MAIL', 'need_mail')
        self.start_time = '00:00:00'  # 运行开始时间（报告显示用）
        self.end_time = '00:00:00'  # 运行结束时间（报告显示用）
        self.show_end_time = 0  # 用于计算的结束时间（报告计算用）
        self.log = Log()
        self.exc = Excel()
        self.row_data = self.exc.row_data()  # 返回所有excel的行数据，与列名成键值对
        self.msql = MySQL()
        #self.msql.delete("TRUNCATE TABLE `test_data`")  # 删除所有数据
        self.msql.delete("DELETE FROM `test_data`")  # 删除所有数据
        self.http = HttpService()
        self.log.info('\n' * 2 + '-' * 50 + '    Runner start!!!    ' + '-' * 50)

    def tearDown(self):
        self.end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.show_end_time = time.clock()
        self.log.info('end time is %s' % self.start_time)
        self.msql.close()

        # 选择是否生成report，1生成，0不生成
        if int(self.need_report) == 1:
            from b5c_interface.report import HTMLReport
            report = HTMLReport()
            report.generate_report(self.start_time, self.end_time, self.show_end_time)
        print 'testing is over!!!'

        # 选择是否需要发送邮件，1发送，0不发送
        if int(self.need_mail) == 1:
            from b5c_interface.mail import Mail
            mail = Mail()
            if mail.send_mail():
                self.log.info('mail send successfully!!')
                print 'mail send successfully!!'
            else:
                self.log.info('mail failed!!')
                print 'mail failed!!'

    def test_run_case(self):
        print 'start running...'
        self.start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        self.log.info('start time is %s' % self.start_time)
        """循环case"""
        """获取excel中的值"""
        for case in self.row_data:
            self.ds = DataStruct()  # 初始化结构体
            self.ds.case_id = int(case['Case ID'])
            self.log.info('-' * 25 + '    case %s started!!!    ' % str(int(case['Case ID'])) + '-' * 25)
            self.ds.description = case['Description']
            self.log.info('Description is: %s' % self.ds.description)
            self.ds.request_url = ''.join(str(self.ds.request_environment + case['Request Url']))
            self.log.info('Request Url is: %s' % self.ds.request_url)
            self.ds.http_method = case['Method']
            self.log.info('Method is: %s' % self.ds.http_method)
            self.ds.run_type = case['Run Type']
            self.log.info('Run Type is: %s' % self.ds.run_type)
            self.ds.data = case['Data']
            self.log.info('Post Data is: %s' % self.ds.data)
            self.ds.header = case['Header']
            self.log.info('Header is: %s' % self.ds.header)

            if not case['Assert_1']:
                self.log.info('Assert 1 is None')
                self.ds.assert_1_db = None
                self.ds.assert_1 = None
                self.ds.assert_1_value = None
            else:
                self.ds.assert_1_db = MySQLdb.escape_string(case['Assert_1'])  # 存入DB特殊字符处理
                self.ds.assert_1 = 'req' + case['Assert_1']
                if isinstance(case['Assert_1_Value'], (int, float)):  # 如果是int或者float类型，就不用MySQL string处理
                    self.log.info('Assert_1_Value is int/float')
                    self.ds.assert_1_value = case['Assert_1_Value']
                    self.log.info('Assert_1_Value is: %s' % str(self.ds.assert_1_value))
                else:
                    self.ds.assert_1_value = MySQLdb.escape_string(case['Assert_1_Value'])  # 存入DB特殊字符处理
                    self.log.info('Assert_1_Value is: %s' % str(self.ds.assert_1_value))

            if not case['Assert_2']:
                self.log.info('Assert 2 is None')
                self.ds.assert_2_db = None
                self.ds.assert_2 = None
                self.ds.assert_2_value = None
            else:
                self.ds.assert_2_db = MySQLdb.escape_string(case['Assert_2'])
                self.ds.assert_2 = 'req' + case['Assert_2']
                if isinstance(case['Assert_2_Value'], (int, float)):
                    self.log.info('Assert_2_Value is int/float')
                    self.ds.assert_2_value = case['Assert_2_Value']
                    self.log.info('Assert_2_Value is: %s' % str(self.ds.assert_2_value))
                else:
                    self.ds.assert_2_value = MySQLdb.escape_string(case['Assert_2_Value'])  # 存入DB特殊字符处理
                    self.log.info('Assert_2_Value is: %s' % str(self.ds.assert_2_value))

            if not case['Assert_3']:
                self.log.info('Assert 3 is None')
                self.ds.assert_3_db = None
                self.ds.assert_3 = None
                self.ds.assert_3_value = None
            else:
                self.ds.assert_3_db = MySQLdb.escape_string(case['Assert_3'])
                self.ds.assert_3 = 'req' + case['Assert_3']
                if isinstance(case['Assert_3_Value'], (int, float)):
                    self.log.info('Assert_3_Value is int/float')
                    self.ds.assert_3_value = case['Assert_3_Value']
                    self.log.info('Assert_3_Value is: %s' % str(self.ds.assert_3_value))
                else:
                    self.ds.assert_3_value = MySQLdb.escape_string(case['Assert_3_Value'])  # 存入DB特殊字符处理
                    self.log.info('Assert_3_Value is: %s' % str(self.ds.assert_3_value))

            """设置参数"""
            self.http.set_all(self.ds.request_url, self.ds.data, self.ds.header)

            """调用接口"""
            if self.ds.http_method.lower() == 'get':
                req = self.http.request_get()
            elif self.ds.http_method.lower() == 'post':
                req = self.http.request_post()

            """获取返回值"""
            self.ds.return_code = req['code']
            self.log.info('Return Code is: %s' % self.ds.return_code)
            self.ds.return_data = json.dumps(req['data'])  # 去除'u'
            #self.ds.return_data = MySQLdb.escape_string(self.ds.return_data)  # 去除特殊符号'，如果数据带这个特殊符号会导致写入DB报错，what the fuck! 大坑！！！！
            self.ds.return_msg = req['msg']
            self.log.info('Return Message is: %s' % self.ds.return_msg)

            """效验模块，效验http返回值，以及excel设置的断言"""
            try:
                if not (self.assertEquals(self.ds.return_code, 2000) or self.assertEquals(self.ds.return_msg,
                                                                                          'success')):
                    self.log.info('Return Code is 2000, success')
                    if self.ds.assert_1_value:   # 断言1验证
                        self.assertEqual(self.ds.assert_1_value, eval(self.ds.assert_1))
                        self.log.info('Assert 1 passed')
                    if self.ds.assert_2_value:  # 断言2验证
                       self.assertEqual(self.ds.assert_2_value, eval(self.ds.assert_2))
                       self.log.info('Assert 2 passed')
                    if self.ds.assert_3_value:  # 断言3验证
                        self.assertEqual(self.ds.assert_3_value, eval(self.ds.assert_3))
                        self.log.info('Assert 3 passed')
                    self.deal_ok()
                    #time.sleep(1)
            except Exception, e:
                self.deal_exception(e)

    def deal_ok(self):
        self.exc.write_return_data(self.ds.case_id, self.ds.return_data)
        self.exc.write_return_message(self.ds.case_id, self.ds.return_msg)
        self.exc.write_return_code(self.ds.case_id, self.ds.return_code)
        self.exc.write_return_status(self.ds.case_id, 'pass')
        self.msql.insert(
            "INSERT INTO `test_data` (`Case_ID`, `Description`, `Request_URL`, `Method`, `Run_Type`, `Data`, `Header`, `Assert_1`, `Assert_1_Value`,`Assert_2`,`Assert_2_Value`,`Assert_3`,`Assert_3_Value`, `Return_Code`, `Return_Msg`, `Return_Data`, `Status`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
                self.ds.case_id, self.ds.description, self.ds.request_url, self.ds.http_method,
                self.ds.run_type, self.ds.data, self.ds.header, self.ds.assert_1_db, self.ds.assert_1_value, self.ds.assert_2_db, self.ds.assert_2_value, self.ds.assert_3_db, self.ds.assert_3_value, self.ds.return_code, MySQLdb.escape_string(self.ds.error_msg),
                MySQLdb.escape_string(self.ds.return_data), 'pass'))
        self.log.info('deal ok')
        self.log.info('-' * 25 + '    running over!!!    ' + '-' * 25 + '\n')

    def deal_exception(self, msg):
        self.ds.error_msg = str(msg)
        if not self.ds.return_code:
            self.ds.return_code = 0
        self.exc.write_return_data(self.ds.case_id, self.ds.return_data)
        self.exc.write_return_message(self.ds.case_id, self.ds.error_msg)
        self.exc.write_return_code(self.ds.case_id, self.ds.return_code)
        self.exc.write_return_status(self.ds.case_id, 'fail')
        self.msql.insert(
            "INSERT INTO `test_data` (`Case_ID`, `Description`, `Request_URL`, `Method`, `Run_Type`, `Data`, `Header`, `Assert_1`, `Assert_1_Value`,`Assert_2`,`Assert_2_Value`,`Assert_3`,`Assert_3_Value`, `Return_Code`, `Return_Msg`, `Return_Data`, `Status`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
                self.ds.case_id, self.ds.description, self.ds.request_url, self.ds.http_method,
                self.ds.run_type, self.ds.data, self.ds.header, self.ds.assert_1_db, self.ds.assert_1_value, self.ds.assert_2_db, self.ds.assert_2_value, self.ds.assert_3_db, self.ds.assert_3_value, self.ds.return_code, MySQLdb.escape_string(self.ds.error_msg),
                MySQLdb.escape_string(self.ds.return_data), 'fail'))
        self.log.info('deal error, error is: %s' % str(msg))
        self.log.info('-' * 25 + '    running over!!!    ' + '-' * 25 + '\n')

if __name__ == '__main__':
    unittest.main()

