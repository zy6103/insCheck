#!/opt/python3/bin/python3
# _*_ coding:utf-8 _*_
# Author: Yong

import cx_Oracle


class OracleBase(object):
    '''
    用于连接oracle服务器，远程执行sql语句
    '''
    def __init__(self,db_user,db_pwd,db_ip,db_port,db_svc_name):
        self.user = db_user
        self.pwd = db_pwd
        self.ip = db_ip
        self.port = db_port
        self.svc_name = db_svc_name
        self.client = self.__db_conn()
        if self.client:  # 数据库连接正常
            self.cursor = self.client.cursor()  # 生成游标

    def  __db_conn(self):
        ''' 连接数据库'''
        try:
            db_client = cx_Oracle.connect("%s/%s@%s:%d/%s" % (self.user,self.pwd,self.ip,int(self.port),self.svc_name))
        except Exception as e:
            return False
        return db_client

    def fetch_all(self,sql):
        ''' 执行sql命令'''
        if self.client:
            try:
                self.cursor.execute(sql)
                res = self.cursor.fetchall()
                return res
            except Exception as e:
                return False

    def close(self):
        ''' 关闭客户端'''
        if self.client:
            if type(self.cursor) == 'object':
                self.cursor.close()
            if type(self.client) == 'object':
                self.client.close()