# -*- coding: utf-8 -*-
import ConfigParser
import os
import smtplib
from b5c_interface.log import Log
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart

__author__ = '不懂'


class Mail:
    def __init__(self):
        cf = ConfigParser.ConfigParser()
        cf.read(r'..\run_mode.ini')
        self.log = Log()
        self.report = self.get_newest_report()  # 得到最新生成的report名字
        self.mailto_list = cf.get('MAIL', 'mailto_list')
        # mailto_list = ['guohuai@b5m.com', '595220635@qq.com']  # 收件组
        self.mail_host = cf.get('MAIL', 'mail_host')  # 设置服务器
        self.mail_user = cf.get('MAIL', 'mail_user')  # 用户名
        self.mail_pass = cf.get('MAIL', 'mail_password')  # 口令
        self.mail_postfix = cf.get('MAIL', 'mail_postfix')  # 发件箱的后缀
        self.me = u'郭淮' + "<" + self.mail_user + "@" + self.mail_postfix + ">"
        self.report_path = ''.join(('..\\', 'report\\', self.report))
        self.content = ''  # 发送邮件内容（处理前）
        self.body = ''  # 发送邮件内容（处理后）

    def get_newest_report(self):
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
        self.log.info('newest report name is: ' + str(c[d[0]]))
        return c[d[0]]

    def send_mail(self):
        """发送邮件"""
        try:
            with open(self.report_path, 'r') as f:
                self.content = f.read()
                self.log.info('mail is sending...')
                print 'mail is sending...'
        except IOError, e:
            self.log.error(str(e))
        # msg = MIMEText(content, 'html', _charset='utf-8')
        msg = MIMEMultipart()
        try:
            self.body = MIMEText(self.content, 'html', _charset='utf-8')
        except IOError, e:
            self.log.error('content is not found!!!')
            self.log.error(str(e))
        msg.attach(self.body)

        '''添加html附件'''
        att = MIMEApplication(self.content, _subtype="html")
        att.add_header('Content-Disposition', 'attachment', filename=self.report)
        msg.attach(att)

        '''设置标题、寄件人、收件人'''
        msg['Subject'] = Header('接口自动化测试报告', 'utf-8')
        msg['From'] = self.me
        # msg['To'] = ";".join(mailto_list)
        msg['To'] = self.mailto_list

        '''发邮件'''
        try:
            server = smtplib.SMTP()
            server.connect(self.mail_host, 25)
            server.login(self.mail_user, self.mail_pass)
            server.sendmail(self.me, self.mailto_list, msg.as_string())
            server.close()
            return True
        except Exception, e:
            self.log.info(str(e))
            return False

