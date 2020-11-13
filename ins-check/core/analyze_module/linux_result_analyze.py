#!/opt/python3/bin/python3
# _*_ coding:utf-8 _*_
# Author: Yong


class ResultAnalyzeObj(object):
    '''结果数据分析类'''

    def __init__(self):
        self.status = 'None'

    def memory_used(self,ver,resp_data):
        '''
        物理内存使用率统计
        :param ver: 系统版本
        :param resp_data: 原始数据
        :return: xx%
        '''
        if ver == 'RHEL7':
            resp_data = resp_data.split()
            used = int(int(resp_data[2]) / int(resp_data[1]) * 100)
        if ver == 'RHEL5' or ver == 'RHEL6' or ver == 'SUSE11' or ver == 'SUSE12':
            resp_data = resp_data.split()
            used = int(int(resp_data[2]) / (int(resp_data[2]) + int(resp_data[3])) * 100)
        if ver == 'AIX':
            resp_data = resp_data.split()
            used = int(int(resp_data[5]) / int(resp_data[1]) * 100)
        self.status = "%d%%" % used
        return self.status

    def swap_used(self,ver,resp_data):
        '''
        交换内存使用率统计
        :param ver:
        :param resp_data:
        :return:
        '''
        if ver == 'RHEL5' or ver == 'RHEL7' or ver == 'RHEL6' or ver == 'SUSE11' or ver == 'SUSE12':
            resp_data = resp_data.split()
            used = int(int(resp_data[2]) / int(resp_data[1]) * 100)
        if ver == 'AIX':
            resp_data = resp_data.split()
            used = int(int(resp_data[3]) / int(resp_data[2]) * 100)
        self.status = "%d%%" % used
        return self.status

    def cpu_used(self,ver,resp_data):
        '''
        CPU使用率统计
        :param ver:
        :param resp_data:
        :return:
        '''
        resp_data = resp_data.split()
        if ver == 'RHEL5' or ver == 'RHEL7' or ver == 'SUSE12' or ver == 'RHEL6' or ver == 'SUSE11':
            used = 100 - int(resp_data[14])
        if ver == 'AIX':
            used = 100 - int(resp_data[15])
        self.status = "%d%%" % used
        return self.status

    def filesystem_used(self,ver,resp_data):
        '''
        文件系统使用情况，高于80%的进行提示
        :param ver:
        :param resp_data:
        :return:
        '''
        status = 'Pass'
        value = 80
        resp_data = resp_data.split()
        if  ver == 'RHEL7' or ver == 'SUSE12' or ver == 'RHEL6' or ver == 'SUSE11':
            used = resp_data[4].replace('%','')
            if int(used) > value:
                fs_str = '%s %s' % (resp_data[5],resp_data[4])
                status = fs_str
        if ver == 'AIX':
            used = resp_data[3].replace('%','')
            if int(used) > value:
                fs_str = '%s %s' % (resp_data[6],resp_data[3])
                status = fs_str
        self.status = status
        return self.status

    def filesystem_inode_used(self,ver,resp_data):
        '''
        文件系统的 inode 使用率统计
        :param ver:
        :param resp_data:
        :return:
        '''
        status = 'Pass'
        value = 80
        resp_data = resp_data.split()
        if ver == 'RHEL5' or ver == 'RHEL7' or ver == 'SUSE12' or ver == 'RHEL6' or ver == 'SUSE11':
            used = resp_data[4].replace('%', '')
            if int(used) > value:
                fs_str = '%s %s' % (resp_data[5], resp_data[4])
                status = fs_str
        if ver == 'AIX':
            used = resp_data[5].replace('%','')
            if int(used) > value:
                fs_str = '%s %s' % (resp_data[6],resp_data[5])
                status = status
        self.status = status
        return self.status

    def ntp_service(self,ver,resp_data):
        '''
        时间服务状态检测，服务不正常或者高于200毫秒的进行提示
        :param ver:
        :param resp_data:
        :return:
        '''
        self.status = 'Pass'
        value = 200
        if ver == 'RHEL7' or ver == 'SUSE12':
            ntp_status = resp_data.find('running')
            if ntp_status >= 0:
                resp_data = resp_data.split('\n')[1]
                time_offset = int(float(resp_data.split()[8]))
                if time_offset > value:
                    self.status = 'time > 200ms'
            else:
                self.status = 'service not run'
        if ver == 'RHEL6' or ver == 'SUSE11':
            ntp_status = resp_data.find('pid')
            if ntp_status >= 0:
                resp_data = resp_data.split('\n')[-2]
                time_offset = int(float(resp_data.split()[8]))
                if time_offset > value:
                    self.status = 'time > 200ms'
            else:
                self.status = 'service not run'
        if ver == 'RHEL5':
            if len(resp_data) == 0:
                status = 'ntpd not running'
        if ver == 'AIX':
            ntp_status = resp_data.find('ntpq')
            if ntp_status < 0:
                self.status = 'Fault'
        return self.status

    def network_conn(self,ver,resp_data):
        '''
        网络连接数统计
        :param ver:
        :param resp_data:
        :return:
        '''
        self.status = int(resp_data)
        return self.status

    def all_process_number(self,ver,resp_data):
        '''最大进程数统计'''
        self.status = int(resp_data)
        return self.status

    def all_thread(self,ver,resp_data):
        '''
        最大线程数统计
        :param ver:
        :param resp_data:
        :return:
        '''
        self.status = int(resp_data)
        return self.status