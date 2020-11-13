#!/opt/python3/bin/python3
# _*_ coding:utf-8 _*_
# Author: Yong

import xlrd,json, os, xlwt


def excel_read(file_name, col_tab_name=None):
    '''
    读取excel表数据
    :param file:excel文件名称
    :param tab:文件中表名称
    :return:以json格式返回数据
    '''
    result = {'status':True, 'data':{}}
    # 读取excel文件，如果文件路径中有中文，请用 r 使用原生字符
    data = xlrd.open_workbook(file_name)
    # 读取文件中所有sheet名称
    work_tabl_name = data.sheet_names()
    # 判断文件名和sheet名是否正确
    if not os.path.exists(file_name):
        result['status'] = False
        result['data'] = '文件：%s 不存在，请检查' % file_name
        return json.dumps(result)
    if col_tab_name:  # 对指定sheet获取数据
        if col_tab_name in work_tabl_name:
            work_tabl_name = [col_tab_name]  # 重写work_tabl_name 列表
        else:
            result['status'] = False
            result['data'] = '文件：%s sheet名称：%s 不存在，请检查' % (file_name, col_tab_name)
            return json.dumps(result)

    # 循环获取文件中所有sheet字段数据
    for tab_name in work_tabl_name:
        # 获取表对象
        tab_obj = data.sheet_by_name(tab_name)
        used_rows = tab_obj.nrows  # 获取表的有效行数
        if used_rows == 0:  # 空表跳过
            continue
        result['data'][tab_name] = []
        for row in range(used_rows):
            # 提取表中每行数据
            row_data = tab_obj.row_values(row, start_colx=0, end_colx=None)
            result['data'][tab_name].append(row_data)
    return json.dumps(result)


def excel_write(xls_file, xls_data):
    '''
    生成xls文件
    :param xls_file: xls文件路径和名称
    :param xls_data: xls文件数据,格式：{'sheet_name': [['tatol field'...], ['data field'...] ]}
    :return:
    '''
    table_book = xlwt.Workbook(encoding='utf-8')
    for sheet_name,sheet_data in xls_data.items():
        # sheet_name: 表sheet名称
        # sheet_data[0]： 表列的字段名称
        data_list = [sheet_data[0]]
        try:
            # 创建excel文件
            sheet = table_book.add_sheet(sheet_name)
            style = xlwt.XFStyle()
            font = xlwt.Font()
            font.bold = True
            font.name = 'Times New Roman'
            style.font = font
            alignment = xlwt.Alignment()
            alignment.horz = xlwt.Alignment.HORZ_LEFT
            alignment.vert = xlwt.Alignment.VERT_CENTER
            style.alignment = alignment
            for data in sheet_data[1:]:  # 循环所有的数据
                data_list.append(data)
            for i in range(len(data_list)):
                for j in range(len(data_list[i])):
                    if i == 0:
                        sheet.col(j).width = 3333
                        sheet.write(i, j, data_list[i][j], style)
                    else:
                        sheet.write(i, j, data_list[i][j])
            status = table_book.save(xls_file)
        except Exception as e:
            status = str(e)
    return status

def data_format_covert(report_file,xls_file_base,resp):
    '''
    对resp数据进行写xls文件格式转换，然后写xls文件
    :param report_file: excel文件路径和名称
    :param xls_file_base: excel文件sheet名称和表字段
    :param resp: 写xls文件的数据
    :return:
    '''
    # 提取名称作为表的sheet名称
    xls_sheet_name = list(xls_file_base.keys())[0]
    # 提取用于生成xls文件的字段名称
    xls_field_list = list(xls_file_base.values())[0][0]
    for ip in resp.data:
        tmp_list = []
        tmp_list.append(ip)
        if 'error' in resp.data[ip]:  # 处理错误的数据
            for f in xls_field_list[1:]:
                if f == 'note':
                    tmp_list.append(resp.data[ip]['error'])
                else:
                    tmp_list.append('-')
        else:
            for field in xls_field_list[1:len(xls_field_list) - 1]:  # 处理正常的数据
                tmp_list.append(resp.data[ip][field])
        # 添加临时数据列表到数据统计列表中
        xls_file_base[xls_sheet_name].append(tmp_list)
    out = excel_write(report_file, xls_file_base)
    return out