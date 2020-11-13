#!/opt/python3/bin/python3
# _*_ coding:utf-8 _*_
# Author: Yong

class BaseResponse(object):
    '''响应类，用于结果数据和状态返回'''
    def __init__(self):
        self.status = True
        self.message = None
        self.data = None