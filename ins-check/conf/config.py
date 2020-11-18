#!/opt/python3/bin/python3
# _*_ coding:utf-8 _*_
# Author: Yong
import os
# 根目录
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 并发线程数，设置为CPU内核数
THREAD_NUM = 6
############### LINUX, AIX config info #############################
# 分析结果汇总目录
ANALYZE_RESULT_DIR = os.path.join(ROOT_DIR, 'result')
# linux 主机文件列表
LINUX_SERVER_FILE = os.path.join(ROOT_DIR,'server_list','linux-server')
# linux主机命令执行结果保存目录
LINUX_SERVER_RESULT_DIR = os.path.join(ROOT_DIR,'result','linux')
# 生成的xls表格字段定义
XLS_FIELD = {'linux':[['ipadd','memory_used','swap_used','cpu_used','filesystem_used','filesystem_inode_used',
                       'ntp_service','network_conn','all_process_number','all_thread','note']]}
# redhat7 远程执行的命令
RHEL7 = {'memory_used':'free -m| grep Mem',
         'swap_used':'free -m|grep -i swap',
         'cpu_used': "vmstat 1 2 | tail -1",
         'filesystem_used': "df -Ph|sed '1d'|sort -rn -k5|head -1",
         'filesystem_inode_used': "df -Pi|sed '1d'|sort -rn -k5|head -1",
         'ntp_service': "systemctl status ntpd | grep -i active && /usr/sbin/ntpq -p|awk 'NR>2 {print $0}'|sort -rn -k9|head -1",
         'network_conn': "netstat -an|awk '/tcp/'|grep -v 'LISTEN'| wc -l",
         'all_process_number': "ps waux | wc -l",
         'all_thread':"ps -eLf | wc -l"}

# redhat6 VER
RHEL6 = {'memory_used':"free -m| grep -i cache|sed '1d'",
         'swap_used':'free -m|grep -i swap',
         'cpu_used': "vmstat 1 2 | tail -1",
         'filesystem_used': "df -Ph|sed '1d'|sort -rn -k5|head -1",
        'filesystem_inode_used': "df -Pi|sed '1d'|sort -rn -k5|head -1",
         'ntp_service': "ps -ef | grep ntpd|grep -v grep && /usr/sbin/ntpq -p|awk 'NR>2 {print $0}'|sort -rn -k9|head -1",
         'network_conn': "netstat -an|awk '/tcp/'|grep -v 'LISTEN'| wc -l",
         'all_process_number': "ps waux | wc -l",
         'all_thread':"ps -eLf | wc -l"}
# redhat5 VER
RHEL5 = {'memory_used':"free -m| grep -i cache|sed '1d'",
         'swap_used':'free -m|grep -i swap',
         'cpu_used': "vmstat 1 2 | tail -1",
         'filesystem_used': "df -Ph|sed '1d'|sort -rn -k5|head -1",
        'filesystem_inode_used': "df -Pi|sed '1d'|sort -rn -k5|head -1",
         'ntp_service': "ps -ef | grep ntpd|grep -v grep",
         'network_conn': "netstat -an|awk '/tcp/'|grep -v 'LISTEN'| wc -l",
         'all_process_number': "ps waux | wc -l",
         'all_thread': "ps -eLf | wc -l"}
# SUSE11 VER
SUSE11 = {'memory_used':"free -m| grep -i cache|sed '1d'",
         'swap_used':'free -m|grep -i swap',
         'cpu_used': "vmstat 1 2 | tail -1",
         'filesystem_used': "df -Ph|sed '1d'|sort -rn -k5|head -1",
         'filesystem_inode_used': "df -Pi|sed '1d'|sort -rn -k5|head -1",
         'ntp_service': "ps -ef | grep ntpd|grep -v grep && /usr/sbin/ntpq -p|awk 'NR>2 {print $0}'|sort -rn -k9|head -1",
         'network_conn': "netstat -an|awk '/tcp/'|grep -v 'LISTEN'| wc -l",
         'all_process_number': "ps waux | wc -l",
         'all_thread': "ps -eLf | wc -l"}
# SUSE12 VER
SUSE12 = {'memory_used':"free -m| grep -i cache|sed '1d'",
         'swap_used':'free -m|grep -i swap',
         'cpu_used': "vmstat 1 2 | tail -1",
         'filesystem_used': "df -Ph|sed '1d'|sort -rn -k5|head -1",
         'filesystem_inode_used': "df -Pi|sed '1d'|sort -rn -k5|head -1",
         'ntp_service': "systemctl status ntpd | grep -i active && /usr/sbin/ntpq -p|awk 'NR>2 {print $0}'|sort -rn -k9|head -1",
         'network_conn': "netstat -an|awk '/tcp/'|grep -v 'LISTEN'| wc -l",
         'all_process_number': "ps waux | wc -l",
         'all_thread': "ps -eLf | wc -l" }
# AIX VER
AIX = {
    'memory_used': 'svmon -G|grep -i mem',
    'swap_used': 'svmon -G|grep -i "^pg"',
    'cpu_used': "vmstat 1 2|tail -1",
    'filesystem_used': "df -g|sort -rn -k4|head -1",
    'filesystem_inode_used': "df -g|sort -rn -k6|head -1",
    'ntp_service': "whereis ntpq",
    'network_conn': "netstat -an|awk '/tcp/'|grep -v 'LISTEN'|wc -l",
    'all_process_number': "ps -Aef|wc -l",
    'all_thread': "ps -ef -mo THREAD | wc -l"
}

####################### oracle #############################
# oracle 主机文件列表
ORACLE_SERVER_FILE = os.path.join(ROOT_DIR,'server_list','oracle-server')
# oracle 主机命令执行结果保存目录
ORACLE_SERVER_RESULT_DIR = os.path.join(ROOT_DIR,'result','oracle')
# 生成的xls表格字段定义
ORA_XLS_FIELD = {'oracle':[['ipadd','instance_status','redo_file_status','tablespace_status','datafile_status','check_fault_obj',
                           'rollback_status','connect_number','note']]}
ORACLE = {'instance_status': "select status from v$instance",
          'redo_file_status': "select group#,status,type,member from v$logfile",
          'tablespace_status': "select tablespace_name,status from dba_tablespaces",
          'datafile_status': "select name,status from v$datafile",
          'check_fault_obj': "select owner, object_name, object_type from dba_objects where status != 'VALID' and owner != 'SYS' and owner != 'SYSTEM'",
          'rollback_status': "select segment_name,status from dba_rollback_segs",
          'connect_number': 'select count(*) from v$session'}

####################### db2 #############################

# oracle 主机文件列表
DB2_SERVER_FILE = os.path.join(ROOT_DIR,'server_list','db2-server')
# oracle 主机命令执行结果保存目录
DB2_SERVER_RESULT_DIR = os.path.join(ROOT_DIR,'result','db2')
# 生成的xls表格字段定义
DB2_XLS_FIELD = {'db2':[['ipadd','db2_start_time','tablespace_status','fault_table','db_search_status',
                         'fault_page_severe','fault_page_error','note']]}

# DB2_XLS_FIELD = {'db2':[['ipadd','db2_start_time','tablespace_status','fault_table','db_search_status','note']]}

DB2_CMD = {'fault_page_severe': "db2diag -H 1d -l Severe|grep -Ei 'Corrupt PD | bad'",
           'fault_page_error': "db2diag -H 1d -l Error |grep -Ei 'Corrupt PD | bad'"}
# DB2_CMD = {}
DB2_SQL = {'db2_start_time': "select DB2START_TIME from sysibmadm.snapdbm",
       'tablespace_status': "select MEMBER,char(TBSP_NAME,50),char(TBSP_STATE,50) from table(mon_get_tablespace('',-2)) t",
       'fault_table': "select tabname from syscat.tables where status != 'N'",
       'db_search_status': "select count(1) from syscat.dbauth with ur"}

##################### other #########################