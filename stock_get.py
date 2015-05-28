#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
stock_get.py
Created by Huaizheng ZHANG on 5/11.
Copyright (c) 2015 zhzHNN. All rights reserved.

"""

import time
import json
import lxml.html
from lxml import etree
import pandas as pd
import numpy as np
import basic_setup as bs
from pandas.util.testing import _network_error_classes
import re
from pandas.compat import StringIO
from urllib2 import urlopen, Request
import stock_date as sd


#生成股票完整代码
def _code_to_symbol(code):
    if code in bs.INDEX_LABELS:
        return bs.INDEX_LIST[code]
    else:
        if len(code) != 6 :
            return ''
        else:
            return 'sh%s'%code if code[:1] == '6' else 'sz%s'%code

#获取日k线数据
def get_day_data(code=None, ktype='D', retry_count=3, pause=0.001):
    
    symbol = _code_to_symbol(code)
    url = ''
    bs._write_head()
    if ktype.upper() in bs.K_LABELS:
        url = bs.DAY_PRICE_URL%(bs.P_TYPE['http'], bs.DOMAINS['ifeng'],
                                bs.K_TYPE[ktype.upper()], symbol)
    elif ktype in bs.K_MIN_LABELS:
        url = bs.DAY_PRICE_MIN_URL%(bs.P_TYPE['http'], bs.DOMAINS['ifeng'],
                                    symbol, ktype)
    else:
        raise TypeError('ktype input error.')
    
    for _ in range(retry_count):
        time.sleep(pause)
        try:
            request = Request(url)
            lines = urlopen(request, timeout=10).read()
        except _network_error_classes:
            pass
        else:
            js = json.loads(lines.decode('utf-8') if bs.PY3 else lines)
            cols = []
            if (code in bs.INDEX_LABELS) & (ktype.upper() in bs.K_LABELS):
                cols = bs.INX_DAY_PRICE_COLUMNS
            else:
                cols = bs.DAY_PRICE_COLUMNS

            if len(js['record'][0]) == 14:
                cols = bs.INX_DAY_PRICE_COLUMNS

            df = pd.DataFrame(js['record'], columns=cols)
            if ktype.upper() in ['D', 'W', 'M']:
                df = df.applymap(lambda x: x.replace(u',', u''))
            
            for col in cols[1:]:
                df[col] = df[col].astype(float)
            
            df = df[df.date >= '2000-01-01']

            end = dt.datetime.strftime(dt.datetime.today(),'%Y-%m-%d')
            df = df[df.date <= end]

            if (code in bs.INDEX_LABELS) & (ktype in bs.K_MIN_LABELS):
                df = df.drop('turnover', axis=1)
            df = df.set_index('date')
            return df
    
    raise IOError("%s网络有问题，请重新获取:%s" % (code, url))

#复权日数据链接
def _get_index_url(index, code, qt):
    if index:
        url = bs.HIST_INDEX_URL%(bs.P_TYPE['http'], bs.DOMAINS['vsf'],
                              code, qt[0], qt[1])
    else:
        url = bs.HIST_FQ_URL%(bs.P_TYPE['http'], bs.DOMAINS['vsf'],
                              code, qt[0], qt[1])
    return url

#复权日网页数据处理
def _parase_fq_factor(code, start, end):
    symbol = _code_to_symbol(code)
    url = bs.HIST_FQ_FACTOR_URL%(bs.P_TYPE['http'], bs.DOMAINS['vsf'], symbol)
    request = Request(url)
    text = urlopen(request, timeout=10).read()
    text = text[1:len(text)-1]
    text = text.decode('utf-8') if bs.PY3 else text
    text = text.replace('{_', '{"')
    text = text.replace('total', '"total"')
    text = text.replace('data', '"data"')
    text = text.replace(':"', '":"')
    text = text.replace('",_', '","')
    text = text.replace('_', '-')
    text = json.loads(text)
    df = pd.DataFrame({'date':list(text['data'].keys()), 'factor':list(text['data'].values())})
    df['date'] = df['date'].map(_fun_except)
    if df['date'].dtypes == np.object:
        df['date'] = df['date'].astype(np.datetime64)
    df = df.drop_duplicates('date')
    df['factor'] = df['factor'].astype(float)
    return df

def _fun_except(x):
    if len(x) > 10:
        return x[-10:]
    else:
        return x

#网络连接，获取复权数据
def _parse_fq_data(url, index, retry_count, pause):
    for _ in range(retry_count):
        time.sleep(pause)
        try:
            html = lxml.html.parse(url)  
            res = html.xpath('//table[@id=\"FundHoldSharesTable\"]')           
            sarr = [etree.tostring(node) for node in res]
            sarr = ''.join(sarr)
            df = pd.read_html(sarr, skiprows = [0, 1])[0]
            if len(df) == 0:
                return pd.DataFrame()
            if index:
                df.columns = bs.HIST_FQ_COLS[0:7]
            else:
                df.columns = bs.HIST_FQ_COLS
            if df['date'].dtypes == np.object:
                df['date'] = df['date'].astype(np.datetime64)
            df = df.drop_duplicates('date')
        except _network_error_classes:
            pass
        else:
            return df
    raise IOError("复权数据获取失败，请检查网络")

#获取复权股票日K线数据
def get_fq_day_data(code, retry_count=3, autype='qfq', index=False, pause=0.001):
    
    start = sd.get_past_year()
    end = sd.today()
    qs = sd.get_quarts(start, end)
    qt = qs[0]
    bs._write_head()
    data = _parse_fq_data(_get_index_url(index, code, qt), index,
                          retry_count, pause)
    if len(qs)>1:
        for d in range(1, len(qs)):
            qt = qs[d]
            bs._write_console()
            df = _parse_fq_data(_get_index_url(index, code, qt), index,
                                retry_count, pause)
            data = data.append(df, ignore_index=True)
    if len(data) == 0 or len(data[(data.date>=start)&(data.date<=end)]) == 0:
        return None
    data = data.drop_duplicates('date')
    if index:
        data = data[(data.date>=start) & (data.date<=end)]
        data = data.set_index('date')
        data = data.sort_index(ascending=False)
        return data
    if autype == 'hfq':
        data = data.drop('factor', axis=1)
        data = data[(data.date>=start) & (data.date<=end)]
        for label in ['open', 'high', 'close', 'low']:
            data[label] = data[label].map(bs.FORMAT)
        data = data.set_index('date')
        data = data.sort_index(ascending = False)
        return data
    else:
        if autype == 'qfq':
            data = data.drop('factor', axis=1)
            df = _parase_fq_factor(code, start, end)
            df = df.drop_duplicates('date')
            df = df.sort('date', ascending=False)
            frow = df.head(1)
            preClose = float(get_realtime_quotes(code)['pre_close'])
            rate = float(frow['factor']) / preClose
            data = data[(data.date >= start) & (data.date <= end)]
            for label in ['open', 'high', 'low', 'close']:
                data[label] = data[label] / rate
                data[label] = data[label].map(bs.FORMAT)
            data = data.set_index('date')
            data = data.sort_index(ascending = False)
            return data
        else:
            for label in ['open', 'high', 'close', 'low']:
                data[label] = data[label] / data['factor']
            data = data.drop('factor', axis=1)
            data = data[(data.date>=start) & (data.date<=end)]
            for label in ['open', 'high', 'close', 'low']:
                data[label] = data[label].map(bs.FORMAT)
            data = data.set_index('date')
            data = data.sort_index(ascending=False)
            data = data.astype(float)
            return data

#获取实时交易数据
def get_realtime_quotes(symbols=None):
    symbols_list = ''
    if type(symbols) is list or type(symbols) is set or type(symbols) is tuple or type(symbols) is pd.Series:
        for code in symbols:
            symbols_list += _code_to_symbol(code) + ','
    else:
        symbols_list = _code_to_symbol(symbols)
    bs._write_head()    
    symbols_list = symbols_list[:-1] if len(symbols_list) > 8 else symbols_list 
    request = Request(bs.LIVE_DATA_URL%(bs.P_TYPE['http'], bs.DOMAINS['sinahq'],
                                                _random(), symbols_list))
    text = urlopen(request,timeout=10).read()
    text = text.decode('GBK')
    reg = re.compile(r'\="(.*?)\";')
    data = reg.findall(text)
    regSym = re.compile(r'(?:sh|sz)(.*?)\=')
    syms = regSym.findall(text)
    data_list = []
    for row in data:
        if len(row)>1:
            data_list.append([astr for astr in row.split(',')])
    df = pd.DataFrame(data_list, columns=bs.LIVE_DATA_COLS)
    df = df.drop('s', axis=1)
    df['code'] = syms
    ls = [cls for cls in df.columns if '_v' in cls]
    for txt in ls:
        bs._write_console()
        df[txt] = df[txt].map(lambda x : x[:-2])
    df = df.set_index('name')
    return df

def _random(n=13):
    from random import randint
    start = 10**(n-1)
    end = (10**n)-1
    return str(randint(start, end))

def get_sharebonus_1_data(code, retry_count=3, pause=0.001):
    for _ in range(retry_count):
        time.sleep(pause)
        try:
            url = bs.SHAREBONUS_URL%(bs.P_TYPE['http'], bs.DOMAINS['vsf'], code)
            html = lxml.html.parse(url)  
            res = html.xpath('//table[@id=\"sharebonus_1\"]')
            sarr = [etree.tostring(node) for node in res]
            sarr = ''.join(sarr)
            df = pd.read_html(sarr)[0]
            df.columns = bs.SHAREBONUS_1_COLS
            del df['del1']
            del df['del2']
            df = df.set_index('公告日期')
        except _network_error_classes:
            pass
        else:
            return df
    raise IOError("分红获取失败，请检查网络")


def get_sharebonus_2_data(code, retry_count=3, pause=0.001):
    for _ in range(retry_count):
        time.sleep(pause)
        try:
            url = bs.SHAREBONUS_URL%(bs.P_TYPE['http'], bs.DOMAINS['vsf'], code)
            html = lxml.html.parse(url)  
            res = html.xpath('//table[@id=\"sharebonus_2\"]')
            sarr = [etree.tostring(node) for node in res]
            sarr = ''.join(sarr)
            df = pd.read_html(sarr)[0]
            df.columns = bs.SHAREBONUS_2_COLS
            del df['del']
            df = df.set_index('公告日期')
        except _network_error_classes:
            pass
        else:
            return df
    raise IOError("配股获取失败，请检查网络")

def get_all_stock_list():
    stock_name = []
    stock_code = []
    bs._write_head()
    #获取深A股票
    url = bs.ALL_STOCK_LIST%(bs.P_TYPE['http'], bs.DOMAINS['afi'], 'sa')
    html = lxml.html.parse(url)
    res = html.xpath('//div[@class=\"result\"]/ul')
    nodes=res[0].xpath("li/a")
    for n in nodes:
        text = n.text
        stock_name.append(text[0:-8].encode('utf-8'))
        stock_code.append(text[-7:-1])
    
    #获取创业板股票
    url = bs.ALL_STOCK_LIST%(bs.P_TYPE['http'], bs.DOMAINS['afi'], 'gem')
    html = lxml.html.parse(url)
    res = html.xpath('//div[@class=\"result\"]/ul')
    nodes=res[0].xpath("li/a")
    for n in nodes:
        text = n.text
        stock_name.append(text[0:-8].encode('utf-8'))
        stock_code.append(text[-7:-1])

    #获取沪A股票
    url = bs.ALL_STOCK_LIST%(bs.P_TYPE['http'], bs.DOMAINS['afi'], 'ha')
    html = lxml.html.parse(url)
    res = html.xpath('//div[@class=\"result\"]/ul')
    nodes=res[0].xpath("li/a")  
    for n in nodes:
        text = n.text
        stock_name.append(text[0:-8].encode('utf-8'))
        stock_code.append(text[-7:-1])   
    
    data = {'name':stock_name,'code':stock_code}
    df = pd.DataFrame(data)
    df = df.set_index('code')
    return df
    
def get_stock_structure(code, retry_count=3, pause=0.001):
    temp = []
    temp_index = []
    temp_data1 = []
    temp_data2 = []
    temp_data3 = []
    temp_data4 = []
    temp_data5 = []
    i = 0
    df_total = []
    url = bs.STOCK_STRUCTURE_URL%(bs.P_TYPE['http'], bs.DOMAINS['vsf'], code)
    for _ in range(retry_count):
        time.sleep(pause)
        try:
            html = lxml.html.parse(url)
            bs._write_head()  
            while html.xpath('//table[@id=\"StockStructureNewTable%s\"]'%i):
                bs._write_console()
                res = html.xpath('//table[@id=\"StockStructureNewTable%s\"]'%i)
                nodes=res[0].xpath("tbody/tr/td")  
                for n in nodes:
                    temp.append(n.text)
                length = len(temp)
                for x in xrange(0,length):
                    if length % 6 == 0:
                        if x % 6 == 0:
                            temp_index.append(temp[x])
                            temp_data1.append(temp[x+1])
                            temp_data2.append(temp[x+2])
                            temp_data3.append(temp[x+3])
                            temp_data4.append(temp[x+4])
                            temp_data5.append(temp[x+5])
                        data = {'index':temp_index,'data1':temp_data1,'data2':temp_data2,'data3':temp_data3,'data4':temp_data4,'data5':temp_data5}
                        df = pd.DataFrame(data)
                    elif length % 5 ==0:
                        if x % 5 == 0:
                            temp_index.append(temp[x])
                            temp_data1.append(temp[x+1])
                            temp_data2.append(temp[x+2])
                            temp_data3.append(temp[x+3])
                            temp_data4.append(temp[x+4])
                        data = {'index':temp_index,'data1':temp_data1,'data2':temp_data2,'data3':temp_data3,'data4':temp_data4}
                        df = pd.DataFrame(data)
                    elif length % 4 ==0:
                        if x % 4 == 0:
                            temp_index.append(temp[x])
                            temp_data1.append(temp[x+1])
                            temp_data2.append(temp[x+2])
                            temp_data3.append(temp[x+3])
                        data = {'index':temp_index,'data1':temp_data1,'data2':temp_data2,'data3':temp_data3}
                        df = pd.DataFrame(data)
                    elif length % 3 ==0:
                        if x % 3 == 0:
                            temp_index.append(temp[x])
                            temp_data1.append(temp[x+1])
                            temp_data2.append(temp[x+2])
                        data = {'index':temp_index,'data1':temp_data1,'data2':temp_data2}
                        df = pd.DataFrame(data)
                    elif length % 2 ==0:
                        if x % 2 == 0:
                            temp_index.append(temp[x])
                            temp_data1.append(temp[x+1])
                        data = {'index':temp_index,'data1':temp_data1}
                        df = pd.DataFrame(data)
                if i < 1:
                    df_total = df
                else:
                    df_total = pd.merge(df_total, df, on='index')
                temp = []
                temp_index = []
                temp_data1 = []
                temp_data2 = []
                temp_data3 = []
                temp_data4 = []
                temp_data5 = []
                i = i + 1
        except _network_error_classes:
            pass
        else:
            df_total = df_total.set_index('index')
            return df_total
    raise IOError("股本结构获取失败，请检查网络")



