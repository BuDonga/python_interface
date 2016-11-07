# -*- coding:utf-8 -*-
import xlrd
import xlwt
from xlutils.copy import copy
from b5c_interface.mysql import *
from b5c_interface.data_structure import *

__author__ = '不懂'


class Excel:
    def __init__(self, path='excel\\interface_caselist.xls'):
        self.path = path

    def open_excel(self):
        try:
            data = xlrd.open_workbook(self.path)
            return data
        except Exception, e:
            print str(e)

    def row_data(self, colnameindex=0, by_index=0):
        """得到excel所有的行数据"""
        data = self.open_excel()
        table = data.sheets()[by_index]
        nrows = table.nrows  # 行数
        ncols = table.ncols  # 列数
        colnames = table.row_values(colnameindex)
        data_list = []
        for i in range(1, nrows):
            app = {}
            n = 0
            for a in table.row_values(i):
                if a:
                    app[colnames[n]] = a
                    n += 1
            data_list.append(app)
        return data_list

    def write_return_code(self, row, value, column=7, by_index=0):
        """写入return code"""
        """设置字体加粗"""
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
            print 'write return_code successfully, current case_ID is %d' % row
        except Exception, e:
            print str(e)

    def write_return_message(self, row, value, column=8, by_index=0):
        """写入return message"""
        """设置字体加粗"""
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
            print 'write return_message successfully, current case_ID is %d' % row
        except Exception, e:
            print str(e)

    def write_return_data(self, row, value, column=9, by_index=0):
        """写入return data"""
        """设置字体加粗"""
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
            print 'write return_data successfully, current case_ID is %d' % row
        except Exception, e:
            print str(e)

    def write_return_status(self, row, value, column=10, by_index=0):
        """写入return status"""
        """设置字体加粗"""
        try:
            style = xlwt.XFStyle()
            font = xlwt.Font()
            font.bold = True
            if value.lower() == 'pass':
                font.colour_index = 3  # 绿色
            elif value.lower() == 'fail':
                font.colour_index = 2  # 红色
            else:
                print 'unknown return_status, please check'
                raise Exception('unknown return status!')
            style.font = font
            oldWb = xlrd.open_workbook(self.path, formatting_info=True)
            newWb = copy(oldWb)
            newWs = newWb.get_sheet(by_index)
            newWs.write(row, column, value.lower(), style)
            newWb.save(self.path)
            print 'write return_status successfully, current case_ID is %d' % row
        except Exception, e:
            print str(e)

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

    def to_db(self):
        c = MySQL()
        c.delete("TRUNCATE TABLE `test_data`")
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
    #Excel.test_excel()
    Excel().test_db()

