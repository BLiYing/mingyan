"""
数据库连接工具类
# """
import logging

import pymysql
import traceback
from scrapy.utils.project import get_project_settings


class MysqlUtil(object):
    # 获取setting文件中的配置
    settings = get_project_settings()

    config = {
        'host': settings.get('MYSQL_HOST'),
        'port': settings.get('MYSQL_PORT'),
        'database': settings.get('MYSQL_DATABASE'),
        'user': settings.get('MYSQL_USER'),
        'password': settings.get('MYSQL_PASSWORD'),
        'charset': settings.get('MYSQL_CHARSET')
    }

    """
    MYSQL数据库对象，负责产生数据库连接 , 此类中的连接采用连接池实现获取连接对象：conn = Mysql.getConn()
            释放连接对象;conn.close()或del conn
    """

    # 连接池对象
    def __init__(self):
        # 数据库构造函数，从连接池中取出连接，并生成操作游标
        self._conn = MysqlUtil.get_conn()
        self._cursor = self._conn.cursor()

    # 获取链接
    @staticmethod
    def get_conn():
        """
        @summary: 静态方法，从连接池中取出连接
        @return MySQLdb.connection
        """

        db = pymysql.connect(host=MysqlUtil.config['host'], port=MysqlUtil.config['port'],
                             user=MysqlUtil.config['user'], passwd=MysqlUtil.config['password'],
                             db=MysqlUtil.config['database'], charset=MysqlUtil.config['charset'])
        return db

    # 查询所有数据
    def get_all(self, sql, param=None):
        """
        @summary: 执行查询，并取出所有结果集
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list(字典对象)/boolean 查询到的结果集
        """
        try:
            if param is None:
                count = self._cursor.execute(sql)
            else:
                count = self._cursor.execute(sql, param)
            if count > 0:
                result = self._cursor.fetchall()
            else:
                result = False
            return result
        except Exception as e:
            traceback.print_exc(e)

    # 查询某一个数据
    def get_one(self, sql, param=None):
        """
        @summary: 执行查询，并取出第一条
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """
        try:
            if param is None:
                count = self._cursor.execute(sql)
            else:
                count = self._cursor.execute(sql, param)
            if count > 0:
                result = self._cursor.fetchone()
            else:
                result = False
            return result
        except Exception as e:
            traceback.print_exc(e)

    # 查询数量
    def get_count(self, sql, param=None):
        """
        @summary: 执行查询，返回结果数
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """
        try:
            if param is None:
                count = self._cursor.execute(sql)
            else:
                count = self._cursor.execute(sql, param)
            return count
        except Exception as e:
            traceback.print_exc(e)

    # 查询部分
    def get_many(self, sql, num, param=None):
        """
        @summary: 执行查询，并取出num条结果
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param num:取得的结果条数
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """
        try:
            if param is None:
                count = self._cursor.execute(sql)
            else:
                count = self._cursor.execute(sql, param)
            if count > 0:
                result = self._cursor.fetchmany(num)
            else:
                result = False
            return result
        except Exception as e:
            traceback.print_exc(e)

    # 插入一条数据
    def insert_one(self, sql, param):
        """
        @summary: 向数据表插入一条记录
        @param sql:要插入的ＳＱＬ格式
        @param value:要插入的记录数据tuple/list
        @return: insertId 受影响的行数
        """
        try:
            row_count = self._cursor.execute(sql, param)
            return row_count
        except Exception as e:
            traceback.print_exc(e)
            self.end("rollback")

    # 插入多条数据
    def insert_many(self, sql, values):
        """
        @summary: 向数据表插入多条记录
        @param sql:要插入的ＳＱＬ格式
        @param values:要插入的记录数据tuple(tuple)/list[list]
        @return: count 受影响的行数
        """
        try:
            row_count = self._cursor.executemany(sql, values)
            return row_count
        except Exception as e:
            traceback.print_exc(e)
            self.end("rollback")

    # def __get_insert_id(self):
    #     """
    #     获取当前连接最后一次插入操作生成的id,如果没有则为０
    #     """
    #     self._cursor.execute("SELECT @@IDENTITY AS id")
    #     result = self._cursor.fetchall()
    #     return result[0]['id']

    # 执行sql
    def __query(self, sql, param=None):
        try:
            if param is None:
                count = self._cursor.execute(sql)
            else:
                count = self._cursor.execute(sql, param)
            return count
        except Exception as e:
            traceback.print_exc(e)

    # 更新
    def update(self, sql, param=None):
        """
        @summary: 更新数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要更新的  值 tuple/list
        @return: count 受影响的行数
        """
        return self.__query(sql, param)

    # 删除
    def delete(self, sql, param=None):
        """
        @summary: 删除数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要删除的条件 值 tuple/list
        @return: count 受影响的行数
        """
        return self.__query(sql, param)

    def begin(self):
        """
        @summary: 开启事务
        """
        self._conn.autocommit(0)

    def end(self, option='commit'):
        """
        @summary: 结束事务
        """
        if option == 'commit':
            self._conn.commit()
        else:
            self._conn.rollback()

    def dispose(self, is_end=1):
        """
        @summary: 释放连接池资源
        """
        if is_end == 1:
            self.end('commit')
        else:
            self.end('rollback')
        self._cursor.close()
        self._conn.close()
        logging.info('--------------------------------------close db success')

