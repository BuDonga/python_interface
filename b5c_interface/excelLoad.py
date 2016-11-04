# -*- coding:utf-8 -*-
import xlrd


class Excel:
    def __init__(self, path='excel\\interface_caselist.xlsx'):
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

    @staticmethod
    def test_excel():
        a = Excel()
        print a.row_data()
        print a.row_data()[0]['Method']
        print a.row_data()[1]['Data']

if __name__ == '__main__':
    Excel.test_excel()

