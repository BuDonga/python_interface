# -*- coding: utf-8 -*-
import os
import time
import logging


class Log:
    def __init__(self):
        self.log_name = ''.join(('AutoTest_', time.strftime('%Y%m%d', time.localtime()), '.log'))
        """设置log文件的存储路径"""

        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename=os.path.join(os.getcwd(), '..\\' 'log', self.log_name),
                            filemode='a')

    @staticmethod
    def debug(msg):
        return logging.debug(msg)

    @staticmethod
    def info(msg):
        return logging.info(msg)

    @staticmethod
    def warning(msg):
        return logging.warning(msg)

    @staticmethod
    def error(msg):
        return logging.error(msg)

    @staticmethod
    def critical(msg):
        return logging.critical(msg)

if __name__ == '__main__':
    a = Log()
    a.debug('nihaoa ')
    a.info('123')
    a.warning('gg')
    a.error('si你好da')
    a.critical('asfasdfsfas')
