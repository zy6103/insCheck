#!/opt/python3/bin/python3
# _*_ coding:utf-8 _*_
# Author: Yong

# 通道方法
# def run_cmd(sshClient, command):
#     channel = sshClient.get_transport().open_session()
#     channel.get_pty()
#     channel.exec_command(command)
#     out = channel.makefile().read()
#     err = channel.makefile_stderr().read()
#     returncode = channel.recv_exit_status()
#     channel.close()  # channel is closed, but not the client
#     return out, err, returncode
# c = GeneralBase('192.168.240.236','db2inst1','ls3du8',22)
# c.cmd("db2 connect to test")
# r = c.cmd("db2 'select * from syscat.bufferpools'")
# print(type(r))
# x = c.cmd("db2 list db directory")
# print('------')
# print(type(x))
# z = c.cmd('''db2 "select tabname,tbspace from syscat.tables where tabname = 'T3'"''')
# print(z.strip().split('\n'))