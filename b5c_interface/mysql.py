# -*- coding: utf-8 -*-
from __future__ import with_statement
import MySQLdb
import ConfigParser

__author__ = '不懂'


class MySQL:
    def __init__(self):
        cf = ConfigParser.ConfigParser()
        cf.read(r'..\db_config.ini')
        self.host = cf.get('DATABASE1', 'host')
        self.port = cf.get('DATABASE1', 'port')
        self.user = cf.get('DATABASE1', 'user')
        self.password = cf.get('DATABASE1', 'password')
        self.db = cf.get('DATABASE1', 'db')
        try:
            self.db = MySQLdb.connect(self.host, self.user, self.password, self.db)
            self.db.set_character_set('utf8')
        except Exception, e:
            print e
            raise IOError('connection failed')
        self.cursor = self.db.cursor()

    def select(self, sql):
        self.cursor.execute(sql)
        print '受影响的行数一共有%d行' % self.cursor.rowcount
        return self.cursor.fetchall()

    def close(self):
        self.db.close()
        print 'DB连接已关闭'
        print '-' * 50

    def insert(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
            print '受影响的行数一共有%d行' % self.cursor.rowcount
            print '插入成功！！'
        except Exception, e:
            self.db.rollback()
            print '插入失败！！'
            print e

    def update(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
            print '受影响的行数一共有%d行' % self.cursor.rowcount
            print '更新成功！！'
        except Exception, e:
            self.db.rollback()
            print '更新失败！！'
            print e

    def delete(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
            print '受影响的行数一共有%d行' % self.cursor.rowcount
            print '删除成功！！'
        except Exception, e:
            self.db.rollback()
            print '删除失败！！'
            print e

    @staticmethod
    def test_sql():
        """测试代码"""
        """select"""
        a = MySQL()
        sql = "SELECT * FROM test WHERE sex = 'm'"
        try:
            result = a.select(sql)
            c = []
            b = {}
            index = 0
            for re in result:
                No = re[0]
                name = re[1]
                sex = re[2]
                age = re[3]
                c.append(name)
                b[index] = re
                index += 1
                print No, name, sex, age
        except Exception, e:
            print e
            raise IOError
        finally:
            a.close()
        print c
        print b

        """insert"""
        b = MySQL()
        sql2 = "INSERT INTO `test` (`no`, `name`, `sex`, `age`) VALUES ('4', 'sdf', 'male', '38')"
        b.insert(sql2)
        b.close()

        """update"""
        c = MySQL()
        sql3 = "UPDATE `test` SET `sex`='m' WHERE (`sex`='male')"
        c.update(sql3)
        c.close()

        """delete"""
        d = MySQL()
        sql4 = "DELETE FROM `test` WHERE no = '4'"
        d.delete(sql4)
        d.close()


if __name__ == '__main__':
    MySQL.test_sql()
