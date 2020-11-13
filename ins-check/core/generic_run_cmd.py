#!/opt/python3/bin/python3
# _*_ coding:utf-8 _*_
# Author: Yong
import os
from conf import config
from core.analyze_module.linux_result_analyze import ResultAnalyzeObj
from core.analyze_module.oracle_result_analyze import OracleResultAnalyzeObj
from core.analyze_module.db2_result_analyze import Db2ResultAnalyzeObj
from utils.remote_run_cmd import GeneralBase
from utils.oracle_module import OracleBase
from utils.db2_module import Db2Base


def linux_ssh_exec_cmd(server,resp,result_data_dir):
    '''linux,aix系统巡检主执行程序'''
    s_list_info = server.strip().split()
    if hasattr(config, s_list_info[1]):
        cmd_dict = getattr(config, s_list_info[1])  # 根据系统版本从配置文件获取对应的巡检命令
    else:
        cmd_dict = False
    ip = s_list_info[0]
    user = s_list_info[2]
    pwd = s_list_info[3]
    port = s_list_info[4]
    try:
        if cmd_dict:  # 如果存在巡检命令
            cli = GeneralBase(ip, user, pwd, port)  #连接系统
            if cli.client:
                analyze_obj = ResultAnalyzeObj()  # 实例化一个结果处理类
                result = {}
                result_filename = os.path.join(result_data_dir,ip)
                with open(result_filename,'w',encoding='utf-8') as resp_cmd_result:
                    for key in cmd_dict:
                        cmd_resp = cli.cmd(cmd_dict[key])  # 远程执行命令并返回结果
                        data_str = """
                        KEY: %s
                        VALUE: %s
                        """ % (key, cmd_resp)
                        resp_cmd_result.write(data_str)  # 保存返回的结果数据
                        if cmd_resp == cmd_dict[key] or len(cmd_resp) == 0:  # 命令在目标机无法执行或者执行延时
                            result[key] = "%s run faild" % cmd_dict[key]
                        elif 'command not found' in cmd_resp:
                            result[key] = '%s not found' % cmd_dict[key]
                        else:
                            try:
                                if hasattr(analyze_obj, key):  # 反射确认对应函数是否存在
                                    status = getattr(analyze_obj, key)(s_list_info[1], cmd_resp)  # 对结果数据进行分析处理
                                    result[key] = status
                            except Exception as e:
                                result[key] = e

                resp.data[ip] = result
                cli.close()
            else:
                resp.data[ip] = {'error':'SSH connect fault'}
        else:
            resp.data[ip] = {'error': "linux-server file: %s config error,config file not found!" % s_list_info[1]}
    except Exception as e:
        resp.data[ip] = {'error':'linux_ssh_exec_cmd function Exception err: %s' % e}


def oracle_exec_cmd(server,resp,result_data_dir):
    '''oracle执行主程序'''
    o_list_info = server.strip().split()
    cmd_dict = config.ORACLE
    ip = o_list_info[0]
    user = o_list_info[1]
    pwd = o_list_info[2]
    svc = o_list_info[3]
    port = o_list_info[4]
    try:
        conn = OracleBase(user, pwd, ip, port, svc)  #sqlplus连接数据库，生成游标
        if conn.client:
            analyze_obj = OracleResultAnalyzeObj()
            result = {}
            result_filename = os.path.join(result_data_dir,ip)
            with open(result_filename,'w',encoding='utf-8') as resp_cmd_result:
                for key in cmd_dict:
                    cmd_resp = conn.fetch_all(cmd_dict[key])  # 以列表元组[('OPEN',)]返回远程系统执行命令的结果
                    data_str = """
                    KEY: %s
                    VALUE: %s
                    """ % (key, str(cmd_resp))
                    resp_cmd_result.write(data_str)  # 保存返回的结果数据
                    try:
                        if hasattr(analyze_obj, key):  # 对结果数据进行分析，检测是否达到报警级别
                            status = getattr(analyze_obj, key)(cmd_resp)
                            result[key] = status
                    except Exception as e:
                        result[key] = e
            resp.data[ip] = result
            conn.close()
        else:
            resp.data[ip] = {'error':'ORACLE connect fault'}
    except Exception as e:
        resp.data[ip] = {'error':'oracle_exec_cmd function Exception err: %s' % e}


def db2_exec_cmd(server,resp,result_data_dir):
    '''db2执行主程序'''
    o_list_info = server.strip().split()
    ip = o_list_info[0]
    user = o_list_info[1]
    pwd = o_list_info[2]
    db = o_list_info[3]
    port = o_list_info[4]
    ssh_port = 22
    sql_dict = config.DB2_SQL
    cmd_dict = config.DB2_CMD

    try:
        analyze_obj = Db2ResultAnalyzeObj()
        result = {}
        result_filename = os.path.join(result_data_dir, ip)
        if os.path.exists(result_filename):
            os.remove(result_filename)
        if cmd_dict:
            cli = GeneralBase(ip, user, pwd, ssh_port)  # 连接系统
            if cli.client:
                with open(result_filename,'a',encoding='utf-8') as resp_cmd_result:
                    for key in cmd_dict:
                        cmd_resp = cli.channel_cmd(cmd_dict[key])
                        data_str = """
                        KEY: %s
                        VALUE: %s
                        """ % (key, str(cmd_resp))
                        resp_cmd_result.write(data_str)
                        try:
                            if hasattr(analyze_obj,key):
                                status = getattr(analyze_obj,key)(cmd_resp)
                                result[key] = status
                        except Exception as e:
                            result[key] = e
                cli.close()
            else:
                resp.data[ip] = {'error':'SSH connect fault'}
        if sql_dict:
            conn = Db2Base(user, pwd, ip, port, db)  #db2连接数据库
            if conn.client:
                with open(result_filename,'a+',encoding='utf-8') as resp_cmd_result:
                    for key in sql_dict:
                        cmd_resp = conn.fetch_all(sql_dict[key])  # 以字典返回远程系统执行命令的结果
                        data_str = """
                        KEY: %s
                        VALUE: %s
                        """ % (key, str(cmd_resp))
                        resp_cmd_result.write(data_str)  # 保存返回的结果数据
                        try:
                            if hasattr(analyze_obj, key):  # 对结果数据进行分析，并返回定制化结果
                                status = getattr(analyze_obj, key)(cmd_resp)
                                result[key] = status
                        except Exception as e:
                            result[key] = e
                resp.data[ip] = result
                conn.close()
            else:
                resp.data[ip] = {'error':'DB2 connect fault'}
    except Exception as e:
        resp.data[ip] = {'error':'db2_exec_cmd function Exception err: %s' % e}