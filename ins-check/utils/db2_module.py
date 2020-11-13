#!/opt/python3/bin/python3
# _*_ coding:utf-8 _*_
# Author: Yong

import ibm_db


class Db2Base(object):
    '''
    用于连接DB2数据库服务器，远程执行sql语句
    '''
    def __init__(self,db_user,db_pwd,db_ip,db_port,db_name):
        self.user = db_user
        self.pwd = db_pwd
        self.ip = db_ip
        self.port = db_port
        self.db_name = db_name
        self.client = self.__db_conn()
        self.stmt = 'None'

    def  __db_conn(self):
        ''' 连接数据库'''
        try:
            conn_str = 'database=%s;hostname=%s;port=%s;protocol=tcpip;uid=%s;pwd=%s' % \
                       (self.db_name,self.ip,self.port,self.user,self.pwd)
            ibm_db_conn = ibm_db.connect(conn_str,'','')
        except Exception as e:
            return False
        return ibm_db_conn

    def fetch_all(self,sql):
        ''' 执行sql命令'''
        try:
            resp_list = []
            # 显示客户端信息
            # print(ibm_db.client_info(self.client))
            # 显示服务端信息
            # print(ibm_db.server_info(self.client))
            # 打印查询结果
            self.stmt = ibm_db.exec_immediate(self.client,sql)
            # res = ibm_db.fetch_both(self.stmt)  # 返回一个字典，由列名和位置索引，表示结果集中的行
            # res = ibm_db.fetch_tuple(self.stmt)  # 返回按列位置索引的元组，表示结果集中的行。列是0索引的
            # res = ibm_db.fetch_assoc(self.stmt)
            flag = True
            while flag:
                res = ibm_db.fetch_assoc(self.stmt)
                if not res:
                    flag = False
                    return resp_list
                resp_list.append(res)

        except Exception as e:
            return False

    def close(self):
        ''' 关闭客户端'''
        if type(self.client) == 'object':
            ibm_db.free_stmt(self.stmt)
            ibm_db.close(self.client)