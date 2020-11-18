#!/opt/python3/bin/python3
# _*_ coding:utf-8 _*_
# Author: Yong
import time,os
from conf import config
from core.generic_run_cmd import linux_ssh_exec_cmd,oracle_exec_cmd,db2_exec_cmd
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.excel_read_write import data_format_covert
from utils.generic import progress_bar

def LINUX(resp):
    '''linux,unix类系统巡检函数'''
    try:
        curr_date = time.strftime("%Y-%m-%d", time.localtime())
        server_file = config.LINUX_SERVER_FILE
        result_data_dir = os.path.join(config.LINUX_SERVER_RESULT_DIR,curr_date)
        # 输出的xls文件
        file_date = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        xls_filename = "report_list_aix_%s.xls" % (file_date)
        report_file = os.path.join(config.ANALYZE_RESULT_DIR, xls_filename)
        # xls文件表头字段
        xls_file_base = config.XLS_FIELD
        # 对系统文件列表格式检测
        with open(server_file) as src_file:
            for line in src_file:
                if len(line.split()) != 5:
                    resp.status = False
                    resp.message = 'linux-server file config error, row(%s) != 5 line' % line
                    return resp
        if not os.path.isdir(result_data_dir):
            os.mkdir(result_data_dir)
        with open(server_file,encoding='utf-8') as sf:
            server_list =sf.readlines()
        resp.data = {}
        task_list = []
        # 定义具有3个线程的线程池
        with ThreadPoolExecutor(3) as executor:
            for server in server_list:
                all_task = executor.submit(linux_ssh_exec_cmd,server,resp,result_data_dir)
                task_list.append(all_task)
            # 多线程任务执行结果检测
            all_num = len(task_list)
            count = 0
            for task_result in as_completed(task_list):
                if task_result.done():
                    count += 1
                    progress_bar(count,all_num)
                    task_result.result()

        # 执行结果进行写xls文件
        print('\nstart create result file:%s' % report_file)
        out = data_format_covert(report_file,xls_file_base,resp)
        if out != None:
            resp.status = False
            resp.message = 'Write xls file error,out:%s' % out

    except Exception as e:
        resp.status = False
        resp.message = 'LINUX Function Exception Error: %s' % e
    return resp


def ORACLE(resp):
    '''oracle数据库巡检函数'''
    try:
        curr_date = time.strftime("%Y-%m-%d", time.localtime())
        oracle_file = config.ORACLE_SERVER_FILE
        result_data_dir = os.path.join(config.ORACLE_SERVER_RESULT_DIR,curr_date)
        file_date = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        xls_filename = "report_oracle_%s.xls" % (file_date)
        report_file = os.path.join(config.ANALYZE_RESULT_DIR, xls_filename)
        # xls文件表头字段
        xls_file_base = config.ORA_XLS_FIELD
        if not os.path.isdir(result_data_dir):
            os.mkdir(result_data_dir)
        with open(oracle_file,encoding='utf-8') as sf:
            oracle_list =sf.readlines()
        resp.data = {}
        task_list = []
        with ThreadPoolExecutor(3) as executor:
            for oracle in oracle_list:
                all_task = executor.submit(oracle_exec_cmd,oracle,resp,result_data_dir)
                task_list.append(all_task)

            all_num = len(task_list)
            count = 0
            for task_result in as_completed(task_list):
                if task_result.done():  # 判断任务是否完成
                    count += 1
                    progress_bar(count,all_num)  # 任务执行进度条打印
                    task_result.result()  # 获取任务结果

        # 执行结果进行写xls文件
        print('\nstart create result file:%s' % report_file)
        out = data_format_covert(report_file,xls_file_base,resp)
        if out != None:
            resp.status = False
            resp.message = 'ORACLE Write xls file error,out:%s' % out

    except Exception as e:
        resp.status = False
        resp.message = 'ORACLE Function Exception Error: %s' % e
    return resp


def DB2(resp):
    '''DB2数据库巡检函数'''
    try:
        curr_date = time.strftime("%Y-%m-%d", time.localtime())
        db2_file = config.DB2_SERVER_FILE
        result_data_dir = os.path.join(config.DB2_SERVER_RESULT_DIR,curr_date)
        file_date = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        xls_filename = "report_db2_%s.xls" % (file_date)
        report_file = os.path.join(config.ANALYZE_RESULT_DIR, xls_filename)
        # xls文件表头字段
        xls_file_base = config.DB2_XLS_FIELD
        if not os.path.isdir(result_data_dir):
            os.mkdir(result_data_dir)
        with open(db2_file,encoding='utf-8') as sf:
            db2_list =sf.readlines()
        resp.data = {}
        task_list = []
        with ThreadPoolExecutor(3) as executor:
            for db2 in db2_list:
                all_task = executor.submit(db2_exec_cmd,db2,resp,result_data_dir)
                task_list.append(all_task)

            all_num = len(task_list)
            count = 0
            for task_result in as_completed(task_list):
                if task_result.done():
                    count += 1
                    progress_bar(count,all_num)
                    task_result.result()

        # 执行结果进行写xls文件
        print('\nstart create result file:%s' % report_file)
        out = data_format_covert(report_file,xls_file_base,resp)
        if out != None:
            resp.status = False
            resp.message = 'DB2 Write xls file error,out:%s' % out

    except Exception as e:
        resp.status = False
        resp.message = 'DB2 Function Exception Error: %s' % e
    return resp