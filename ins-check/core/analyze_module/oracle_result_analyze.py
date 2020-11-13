#!/opt/python3/bin/python3
# _*_ coding:utf-8 _*_
# Author: Yong


class OracleResultAnalyzeObj(object):
    ''' oracle 结果数据分析类'''

    def __init__(self):
        self.status = 'Node'

    def instance_status(self,resp_data):
        '''
        oracle 数据库实例状态检测
        :param resp_data: 原始数据:（列表元组格式）
        :return:
        '''
        self.status = resp_data[0][0]
        return self.status

    def redo_file_status(self,resp_data):
        ''' 检查redo文件状态'''
        self.status = 'PASS'
        for line in resp_data:
            if 'ONLINE' != line[2]:
                self.status = '%s %s' % (line[3],line[2])
                break
        return self.status

    def tablespace_status(self,resp_data):
        '''检查表空间状态'''
        self.status = 'PASS'
        for line in resp_data:
            if 'ONLINE' != line[1]:
                self.status = '%s %s' % (line[0], line[1])
                break
        return self.status

    def datafile_status(self,resp_data):
        '''数据文件状态'''
        self.status = 'PASS'
        for line in resp_data:
            if 'ONLINE' != line[1] or 'SYSTEM' != line[1]:
                self.status = '%s %s' % (line[0], line[1])
                break
        return self.status

    def check_fault_obj(self,resp_data):
        ''' 检查无效对象'''
        self.status = 'PASS'
        if len(resp_data) != 0:
            self.status = str(resp_data)
        return self.status

    def rollback_status(self,resp_data):
        '''检查所有回滚段状态'''
        self.status = 'PASS'
        for line in resp_data:
            if 'ONLINE' != line[1]:
                self.status = '%s %s' % (line[0], line[1])
        return self.status

    def connect_number(self,resp_data):
        ''' 数据库连接数统计'''
        if resp_data[0][0]:
            self.status = resp_data[0][0]
        return self.status
