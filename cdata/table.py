#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Li Ding
# table/excel data manipulation

#base packages
import os
import sys
import json
import logging
import codecs
import hashlib
import datetime
import logging
import time
import re
import collections

import xlwt
import xlrd

def json2excel(items, keys, filename, page_size=60000):
    wb = xlwt.Workbook()
    rowindex =0
    sheetindex=0
    for item in items:
        if rowindex % page_size ==0:
            sheetname = "%02d" % sheetindex
            ws = wb.add_sheet(sheetname)
            rowindex = 0
            sheetindex +=1

            colindex =0
            for key in keys:
                ws.write(rowindex, colindex, key)
                colindex+=1
            rowindex +=1

        colindex =0
        for key in keys:
            v = item.get(key,"")
            if type(v) == list:
                v = ','.join(v)
            if type(v) == set:
                v = ','.join(v)
            ws.write(rowindex, colindex, v)
            colindex+=1
        rowindex +=1

    logging.debug(filename)
    wb.save(filename)

####################################
# 2017-01-21  selected

def excel2json(filename, non_empty_col=0, file_contents=None):
    # http://www.lexicon.net/sjmachin/xlrd.html

    counter = collections.Counter()
    if file_contents:
        workbook = xlrd.open_workbook(file_contents=file_contents)
    else:
        workbook = xlrd.open_workbook(filename)

    start_row = 0
    ret = collections.defaultdict(list)
    fields = {}
    for name in workbook.sheet_names():
        sh = workbook.sheet_by_name(name)
        headers = []
        for col in range(len(sh.row(start_row))):
            headers.append(sh.cell(start_row,col).value)

        logging.info( u"sheet={} header={} rows={}".format( name, json.dumps(headers,ensure_ascii=False) , sh.nrows) )

        fields[name]= headers

        for row in range(start_row+1, sh.nrows):
            item={}
            rowdata = sh.row(row)
            if len(rowdata)< len(headers):
                msg = "skip mismatched row {}".format(json.dumps(rowdata, ensure_ascii=False))
                logging.warning(msg)
                continue

            for col in range(len(headers)):
                value = sh.cell(row,col).value
                if type(value) in [unicode, basestring]:
                    value = value.strip()
                item[headers[col]]= value

            if non_empty_col>=0 and not item[headers[non_empty_col]]:
                logging.debug("skip empty cell")
                continue

            ret[name].append(item)
        logging.info( u"loaded {} {} (non_empty_col={})".format( filename, len(ret[name]) , non_empty_col))
    return {'data':ret,'fields':fields}
