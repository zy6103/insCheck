#!/opt/python3/bin/python3
# _*_ coding:utf-8 _*_
# Author: Yong

from core.base_function import *


def run(resp):
    '''主程序'''
    select_str = """
            Please select check dest:
            1........................  LINUX
            2........................  DB2
            3........................  ORACLE
    
            Press Key ( Exit )
    """
    choise_dest = {
        '1':LINUX,
        '2':DB2,
        '3':ORACLE
    }
    print(select_str)
    choise = input('choice Number:')
    if choise not in choise_dest:
        resp.status = False
        resp.message = 'choice number not exist!'
        return resp

    return choise_dest[choise](resp)  # 执行菜单选择的对应程序
