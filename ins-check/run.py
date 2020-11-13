#!/opt/python3/bin/python3
# _*_ coding:utf-8 _*_
# Author: Yong

from core.main import run
from utils.response import BaseResponse

if __name__ == "__main__":
    '''程序入口'''
    resp = BaseResponse()
    result = run(resp)
    if not result.status:
        print(result.message)
    else:
        print('\n program run finish!')