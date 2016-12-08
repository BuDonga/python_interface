# -*- coding: utf-8 -*-
import ConfigParser
import os


__author__ = '不懂'


class Mail:
    def __init__(self):
        cf = ConfigParser.ConfigParser()
        cf.read(r'..\run_mode.ini')
        self.report = self.get_newest_report()
        self.mail_host = cf.get('MAIL', 'mail_host')  # 设置服务器
        self.mail_user = cf.get('MAIL', 'mail_user')  # 用户名
        self.mail_pass = cf.get('MAIL', 'mail_password')  # 口令
        self.mail_postfix = cf.get('MAIL', 'mail_postfix')  # 发件箱的后缀
        self.me = u'郭淮' + "<" + self.mail_user + "@" + self.mail_postfix + ">"
        self.report_path = ''.join(('..\\', 'report\\', self.report))

    @staticmethod
    def get_newest_report():
        """根据创建时间排序，得到最新的测试报告
            a：获得report目录下所有文件的文件名
            c：创建一个字典，用来存储各文件的信息，key是创建时间（未经过时间戳处理），value是文件名
            b：用来遍历a目录下的文件名
            d：存储所有文件的创建时间，并且倒序排列，最新的创建时间是d[0]
            c[d[0]]:返回最新创建时间所对应的文件名，即是最新的测试报告
        """
        a = os.listdir('..\\report')
        c = {}
        for b in a:
            c[os.stat(''.join(('..\\report\\', b))).st_atime] = b
        d = sorted(c.keys(), reverse=True)
        return c[d[0]]

    def send_mail(self):
        [MAIL]
        mail_user =  ###
        mail_password =  ###
        mail_host = smtp
        .163.com
        mail_postfix = 163.
        com
        mailto_list = guohuai @ gshopper.com

