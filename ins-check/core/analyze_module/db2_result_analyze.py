#!/opt/python3/bin/python3
# _*_ coding:utf-8 _*_
# Author: Yong


class Db2ResultAnalyzeObj(object):
    ''' db2 结果数据分析类'''

    def __init__(self):
        self.status = 'None'

    def db2_start_time(self,resp_data):
        '''
        db2 数据库启动时间
        :param resp_data: 原始数据:（字典格式）
        :return:
        '''
        self.status = resp_data[0]['DB2START_TIME'].strftime('%Y-%m-%d %H:%M:%S')
        return self.status

    def tablespace_status(self,resp_data):
        '''
        db2 数据库表空间状态
        :param resp_data: 原始数据:（字典格式）
        :return:
        '''
        for tablespace in resp_data:
            if tablespace['3'].strip() == 'NORMAL':  # 巡检检查所有表空间
                self.status = 'NORMAL'
            else:
                err_tablespace = '%s %s' % (tablespace['2'],tablespace[3])  # 非正常表空间
                self.status = err_tablespace
                break
        return self.status

    def fault_table(self,resp_data):
        '''
        db2 数据库错误表
        :param resp_data: 原始数据:（字典格式）
        :return:
        '''
        if resp_data:  # 如果有错误表
            self.status = resp_data
        return self.status

    def db_search_status(self,resp_data):
        '''
        db2 数据库查询状态
        :param resp_data: 原始数据:（字典格式）
        :return:
        '''
        if resp_data[0]['1'] > 0:
            self.status = 'NORMAL'
        else:
            self.status = 'FAULT'
        return self.status

    def fault_page_severe(self,resp_data):
        '''
        db2 page severe
        :param resp_data:
        :return:
        '''
        if resp_data:
            self.status = resp_data
        return self.status

    def fault_page_error(self,resp_data):
        '''
        db2 page error
        :param resp_data:
        :return:
        '''
        if resp_data:
            self.status = resp_data
        return self.status