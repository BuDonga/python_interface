# -*- coding:utf-8 -*-
import xlrd
import xlwt
from xlutils.copy import copy
from b5c_interface.log import Log
from b5c_interface.mysql import *
from b5c_interface.data_structure import *

__author__ = '不懂'


class Excel:
    def __init__(self, path='excel\\interface_caselist.xls'):
    #def __init__(self, path='excel\\test.xls'):
        self.log = Log()
        self.path = path

    def open_excel(self):
        try:
            data = xlrd.open_workbook(self.path)
            return data
        except Exception, e:
            self.log.error('open excel error: ' + str(e))

    def row_data(self, colnameindex=0, by_index=0):
        """得到excel所有的行数据"""
        data = self.open_excel()
        table = data.sheets()[by_index]
        nrows = table.nrows  # 行数
        self.log.info('total rows are: ' + str(nrows))
        ncols = table.ncols  # 列数
        self.log.info('total columns are: ' + str(ncols))
        colnames = table.row_values(colnameindex)
        self.log.info('column names are: ' + ','.join(colnames))
        data_list = []
        for i in range(1, nrows):
            app = {}
            n = 0
            for a in table.row_values(i):
                if a:
                    app[colnames[n]] = a
                    n += 1
                else:
                    app[colnames[n]] = None
                    n += 1
            data_list.append(app)
        return data_list

    def write_data(self, row, value, column, by_index):
        """设置字体加粗"""
        if len(str(value)) > 32767:
            value = 'String longer than 32767 characters,please check it in report'
            self.log.info(value)
        try:
            style = xlwt.XFStyle()
            font = xlwt.Font()
            font.bold = True
            style.font = font
            oldWb = xlrd.open_workbook(self.path, formatting_info=True)
            newWb = copy(oldWb)
            newWs = newWb.get_sheet(by_index)
            newWs.write(row, column, value, style)
            newWb.save(self.path)
            self.log.info('write successfully, current case_ID is %d' % row)
        except Exception, e:
            self.log.error('write unsuccessfully, error is: ' + str(e))

    def write_return_code(self, row, value):
        """写入return code"""
        self.write_data(row, value, column=13, by_index=0)

    def write_assert_1_resault(self, row, value):
        """写入验证结果1"""
        self.write_data(row, value, column=8, by_index=0)

    def write_assert_2_resault(self, row, value):
        """写入验证结果2"""
        self.write_data(row, value, column=10, by_index=0)

    def write_assert_3_resault(self, row, value):
        """写入验证结果3"""
        self.write_data(row, value, column=12, by_index=0)

    def write_return_message(self, row, value):
        """写入return message"""
        self.write_data(row, value, column=14, by_index=0)

    def write_return_data(self, row, value):
        """写入return data"""
        self.write_data(row, value, column=15, by_index=0)

    def write_return_status(self, row, value, column=16, by_index=0):
        """写入return status"""
        try:
            style = xlwt.XFStyle()
            font = xlwt.Font()
            font.bold = True
            if value.lower() == 'pass':
                font.colour_index = 3  # 绿色
            elif value.lower() == 'fail':
                font.colour_index = 2  # 红色
            else:
                self.log.error('unknown return_status, please check')
                raise Exception('unknown return status!')
            style.font = font
            oldWb = xlrd.open_workbook(self.path, formatting_info=True)
            newWb = copy(oldWb)
            newWs = newWb.get_sheet(by_index)
            newWs.write(row, column, value.lower(), style)
            newWb.save(self.path)
            self.log.info('write return_status successfully, current case_ID is %d' % row)
        except Exception, e:
            self.log.error('write return_status unsuccessfully, error is: ' + str(e))

    @staticmethod
    def test_excel():
        """读取excel"""
        a = Excel(path='excel\\test.xls')
        print a.row_data()
        print len(a.row_data())
        print a.row_data()[0]['Method']
        print a.row_data()[1]['Data']
        a.write_return_code(1, '2000')
        a.write_return_message(1, 'test ok!!!')
        a.write_return_status(1, 'pasS')
        a.write_return_status(2, 'FAIL')
        a.write_return_data(1, 'data!!!!!')
        a.write_assert_1_resault(1, 'pass')
        a.write_assert_2_resault(2, 'fail')
        a.write_assert_3_resault(2, 'heelo')

    def to_db(self):
        c = MySQL()
        #c.delete("TRUNCATE TABLE `test_data`")
        d = DataStruct()
        b = Excel(self.path)
        dd = b.row_data()
        for info in dd:
            d.case_id = info['Case ID']
            d.description = info['Description']
            d.request_url = info['Request Url']
            d.http_method = info['Method']
            d.run_type = info['Run Type']
            d.data = info['Data']
            d.header = info['Header']
            c.insert(
                "INSERT INTO `test_data` (`Case_ID`, `Description`, `Request_URL`, `Method`, `Run_Type`, `Data`, `Header`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
                d.case_id, d.description, d.request_url, d.http_method, d.run_type, d.data, d.header))
        c.close()

    def test_db(self):
        c = MySQL()
        #c.delete("TRUNCATE TABLE `test_data`")
        d = DataStruct()
        b = Excel(path='excel\\test.xls')
        dd = b.row_data()
        for info in dd:
            d.case_id = info['Case ID']
            d.description = info['Description']
            d.request_url = info['Request Url']
            d.http_method = info['Method']
            d.run_type = info['Run Type']
            d.data = info['Data']
            d.header = info['Header']
            c.insert("INSERT INTO `test_data` (`Case_ID`, `Description`, `Request_URL`, `Method`, `Run_Type`, `Data`, `Header`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')"  %(d.case_id, d.description, d.request_url, d.http_method, d.run_type, d.data, d.header))
        c.close()
if __name__ == '__main__':
    Excel.test_excel()
    #Excel().test_db()

