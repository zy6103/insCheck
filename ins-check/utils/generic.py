#!/opt/python3/bin/python3
# _*_ coding:utf-8 _*_
# Author: Yong

import sys

def progress_bar(curr_num,all_num):
    '''
    打印进度条
    :param curr_num:当前数量
    :param all_num: 总数量
    :return:
    '''
    percent = curr_num / all_num
    sys.stdout.write("\r{1}".format('%.2f%%' % (percent * 100)))
    sys.stdout.flush()
