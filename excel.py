#!/usr/bin/env python
# encoding: utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
"""
@author: tangtao
@contact: tangtao@lhtangtao.com
@site: http://www.lhtangtao.com
@software: PyCharm
@file: excel.py
@time: 2017/7/22 13:08
"""
import xlwt
import xlrd
from xlutils.copy import copy


def save_to_excel(infos):
    oldWb = xlrd.open_workbook('demo.xls', "sheet1", formatting_info=True)
    table = oldWb.sheets()[0]
    nrows = table.nrows  # 行数
    newWb = copy(oldWb)
    newWs = newWb.get_sheet(0)
    newWs.write(nrows, 0, infos[0])
    newWs.write(nrows, 1, infos[1])
    newWs.write(nrows, 2, infos[2])
    newWs.write(nrows, 3, infos[3])
    newWs.write(nrows, 4, infos[4])
    newWs.write(nrows, 5, infos[5])
    newWs.write(nrows, 6, infos[6])
    newWs.write(nrows, 7, infos[7])
    newWs.write(nrows, 8, infos[8])
    newWs.write(nrows, 9, infos[9])
    newWs.write(nrows, 10, infos[10])
    if len(infos) == 12:
        newWs.write(nrows, 11, infos[11])
    if len(infos) == 13:
        newWs.write(nrows, 11, infos[11])
        newWs.write(nrows, 12, infos[12])

    newWb.save('demo.xls')


