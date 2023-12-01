import threading
from typing import List

import pymysql
from dbutils.pooled_db import PooledDB

from MovieRecSystem.config import redis_config, mysql_config
from MovieRecSystem.utils.logger_util import logger


def _encode(v, encoding='UTF-8') -> str:
    return str(v, encoding=encoding)


'''
单例是redis, 然后提供静态方法
可以使用其它的
'''


class DB(object):
    # 单例模式
    # 必须要有一个静态的属性, 或者说类上的属性
    __lock = threading.Lock()  # 锁
    __pool = None  # 只要是单例就会有一个静态的属性, mysql就是我们的线程池

    def __init__(self):
        self.pool = DB.__get_conn_pool() # 链接时是需要时间的,所以创建连接池! 保证整个运行只有一个线程

    @staticmethod
    def __get_conn_pool():
        '''
        就是获取一个连接池(因为是单例), 获取锁之后再添加实例(和redis一样)
        但是不代表已经连接成功了,还需要connection
        :return:
        '''
        if DB.__pool is None:
            DB.__lock.acquire()
            try:
                if DB.__pool is None:
                    # 获取配置信息
                    _cfg = mysql_config.cfg.copy()
                    if 'creator' not in _cfg:
                        raise ValueError("必须给定creator参数")
                    if _cfg['creator'] != 'pymysql':
                        raise ValueError("creator参数必须给定为pymysql")
                    del _cfg['creator']
                    DB.__pool = PooledDB(pymysql, **_cfg)
                    # DB.__pool = PooledDB(
                    #     creator=pymysql,  # 使用链接数据库的模块
                    #     maxconnections=500,  # 连接池允许的最大连接数，0和None表示不限制连接数
                    #     mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
                    #     maxcached=50,  # 链接池中最多闲置的链接，0和None不限制
                    #     blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
                    #     maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
                    #     setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
                    #     ping=1,
                    #     host="121.40.96.93",
                    #     port=3306,
                    #     user="gerry",
                    #     password="123456",
                    #     database="rec_system",
                    #     charset="utf8"
                    # )
            except Exception as e:
                raise ValueError("创建Mysql数据库连接池异常!") from e
            finally:
                DB.__lock.release()
        return DB.__pool

    def _get_connection(self):
        conn = self.pool.connection()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        return conn, cursor

    @staticmethod
    def _close_connection(conn, cursor):
        if cursor:
            try:
                cursor.close()
            except Exception as e:
                logger.error("关闭Mysql连接cursor异常。", exc_info=e)
        if conn:
            try:
                conn.close()
            except Exception as e:
                logger.error("关闭Mysql连接conn异常。", exc_info=e)

    # 执行查询结果(这个可以放到缓存里)
    def query_sql(self, sql, **params):
        conn, cursor = self._get_connection()
        try:
            cursor.execute(sql, params)
            result = cursor.fetchall()
        except Exception as e:
            raise ValueError(f"Query查询异常，当前sql语句为:{sql}, 参数类别为:{params}.") from e
        finally:
            self._close_connection(conn, cursor)
        return result

    # 执行
    def execute_sql(self, sql, **params):
        conn, cursor = self._get_connection()
        try:
            cursor.execute(sql, params)
            result = cursor.lastrowid
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise ValueError(f"Execute执行异常，当前sql语句为:{sql}, 参数类别为:{params}.") from e
        finally:
            self._close_connection(conn, cursor)
        return result

