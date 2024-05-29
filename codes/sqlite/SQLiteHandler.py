# !/usr/bin/env python
# -*- coding:utf-8 -*-
import sqlite3
from sqlite3 import Connection
from threading import Lock


class SingletonMeta(type):
    """
    一个线程安全的单例模式实现。
    """

    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class SQLiteHandler(metaclass=SingletonMeta):
    """
    一个用于管理 SQLite 数据库连接的单例类。
    """

    _connection: Connection = None

    def __init__(self, db_path: str):
        if self._connection is None:
            self._connection = sqlite3.connect(db_path)
            self._cursor = self._connection.cursor()

    def execute(self, query: str, params=None):
        """
        执行 SQL 查询。

        :param query: 要执行的 SQL 查询
        :param params: SQL 查询的参数
        :return: 游标对象
        """
        if params is None:
            params = []
        self._cursor.execute(query, params)
        self._connection.commit()
        return self._cursor

    def fetchall(self):
        """
        获取查询结果的所有行。

        :return: 包含所有行的列表
        """
        return self._cursor.fetchall()

    def fetchone(self):
        """
        获取查询结果的下一行。

        :return: 单行数据或 None（如果没有更多行）
        """
        return self._cursor.fetchone()

    def close(self):
        """
        关闭数据库连接。
        """
        if self._connection:
            self._cursor.close()
            self._connection.close()
            self._connection = None
