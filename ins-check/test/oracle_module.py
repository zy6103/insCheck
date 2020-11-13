#!/opt/python3/bin/python3
# _*_ coding:utf-8 _*_
# Author: Yong

import cx_Oracle

conn = cx_Oracle.connect('zhaoyong/ls3du8@192.168.240.236:1521/orcl')  # 连接数据库

cr = conn.cursor()  # 创建连接游标
sql = 'select status from v$instance'  # 执行的sql语句
cr.execute(sql)  # 执行sql语句
# fetchall: 一次性返回sql执行的所有结果
# fetchone： 一次返回一行执行结果
rs = cr.fetchall()
print(rs)

#关闭游标
cr.close()
# 关闭连接
conn.close()