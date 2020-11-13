#!/opt/python3/bin/python3
# _*_ coding:utf-8 _*_
# Author: Yong

import paramiko


class GeneralBase(object):
    '''连接远程系统执行命令'''

    def __init__(self, ipaddr, user, pwd, port):
        self.ipaddr = ipaddr
        self.user = user
        self.pwd = pwd
        self.port = port
        self.client = self.conn()
        self.chan = None

    def conn(self):
        '''与远程服务器建立连接'''
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=self.ipaddr, port=self.port, username=self.user, password=self.pwd)
        except Exception as e:
            return False
        return ssh_client

    def cmd(self, cmd):
        '''远程执行命令'''
        try:
            stdin, stdout, stderr = self.client.exec_command(cmd,timeout=10)
            out, err = stdout.read(), stderr.read()
            # mess = out if out else err
            mess = out.decode()
        except Exception as e:
            mess = cmd
        return mess

    def channel_cmd(self,cmd):
        '''定义通道进行I/O操作，应用db2命令'''
        channel = self.client.get_transport().open_session()  # 建立一个session
        channel.get_pty()  # 定义一个虚拟终端
        channel.exec_command(cmd,timeout=10)  # 远程执行命令
        out,err = channel.makefile().read(),channel.makefile_stderr().read()
        resp_code = channel.recv_exit_status()
        if resp_code == 0:
            resp = out
        else:
            resp =  out if out else err
        return resp.decode('utf-8')

    def close(self):
        '''关闭连接'''
        self.client.close()