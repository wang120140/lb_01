# -*- coding: utf-8 -*-

# 这个是暴露出数据库连接池
import pymysql
from datetime import datetime
from pymysql import OperationalError
from dbutils.pooled_db import PooledDB
# 配置连接参数
host = "localhost"
port = 3306
user = "root"
password = "CaZRPEejMKGE5TmG"
database = "my_lb"
from sshtunnel import SSHTunnelForwarder
# 代理参数设置
proxyHost = "152.136.45.25"
proxyPort = "22"
proxyUser = "root"
proxyPass = "wyh07143612@CSY"
charset = 'utf8mb4'


pool__ = None
class MySQLClient:

    def __init__(self):
            try:
                server = SSHTunnelForwarder(
                    ssh_address_or_host=(proxyHost, 22),  # 指定ssh登录的跳转机的address
                    ssh_username=proxyUser,  # 跳转机的用户
                    ssh_password=proxyPass,  # 跳转机的密码
                    remote_bind_address=(host, 3306))
                server.start()
                self.pool = PooledDB(
                    creator=pymysql,
                    host=host,
                    port=server.local_bind_port,
                    user=user,
                    password=password,
                    database=database,
                    charset=charset,
                    autocommit=False,
                    maxconnections=10,
                    cursorclass=pymysql.cursors.DictCursor
                )

            except OperationalError as e:
                print(f"Cannot connect to database: {e}")
                exit(1)
    @staticmethod
    def __dict_datetime_obj_to_str(result_dict):
        """把字典里面的datetime对象转成字符串"""
        if result_dict:
            result_replace = {k: v.__str__() for k, v in result_dict.items() if isinstance(v, datetime)}
            result_dict.update(result_replace)
        return result_dict

    def execute(self, sql, params=None):
        """
        执行，返回的为 list，可单条也可多条
        """
        conn = self.pool.connection()
        cursor = conn.cursor()
        self.cursor = cursor

        try:
            if params is None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, params)
                conn.commit()
            return [self.__dict_datetime_obj_to_str(row_dict) for row_dict in cursor.fetchall()]
        except Exception as e:
            print(f"Cannot execute query all: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def executemany(self, sql, params):
        """
        插入和更新时使用
        """
        conn = self.pool.connection()
        cursor = conn.cursor()
        self.cursor = cursor

        try:
            cursor.executemany(sql, params)
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Cannot execute query: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def query_one(self, sql, params=None):
        """
        查询单条数据，返回的为dict
        """
        conn = self.pool.connection()
        cursor = conn.cursor()
        self.cursor = cursor

        try:
            if params is None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, params)
            result = cursor.fetchone()
            return self.__dict_datetime_obj_to_str(result)
        except Exception as e:
            print(f"Cannot execute query one: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def insert(self, table, data):
        """
        插入单条数据
        """
        columns = ", ".join(data.keys())
        values_template = ", ".join(["%s"] * len(data))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({values_template})"
        params = tuple(data.values())
        self.executemany(sql, [params])

    def insert_many(self, table, data_list):
        """
        批量插入数据
        """
        columns = ", ".join(data_list[0].keys())
        values_template = ", ".join(["%s"] * len(data_list[0]))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({values_template})"
        params_list = [tuple(data.values()) for data in data_list]
        self.executemany(sql, params_list)

    def update(self, table, data, where_clause, param):
        """
        更新数据
        """
        set_clause = ", ".join([f"{key}=%s" for key in data.keys()])
        sql = f"UPDATE {table} SET {set_clause}  WHERE {where_clause}"
        params = tuple(list(data.values()) + param)
        self.executemany(sql, [params])

    def delete(self, table, where_clause, pram):
        """
        删除数据
        """
        sql = f"DELETE FROM {table} WHERE {where_clause}"
        print(sql)
        print(pram)
        self.execute(sql)


connector = MySQLClient()