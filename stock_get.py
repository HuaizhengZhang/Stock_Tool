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

#网络连接，获取数据
def _parse_fq_data(url, retry_count, pause):
    for _ in range(retry_count):
        time.sleep(pause)
        try:
            html = lxml.html.parse(url)  
            res = html.xpath('//table[@id=\"FundHoldSharesTable\"]')
            if bs.PY3:
                sarr = [etree.tostring(node).decode('utf-8') for node in res]
            else:
                sarr = [etree.tostring(node) for node in res]
            sarr = ''.join(sarr)
            df = pd.read_html(sarr, skiprows=[0, 1])[0]
            df.columns = bs.HIST_FQ_COLS
            if df['date'].dtypes == np.object:
                df['date'] = df['date'].astype(np.datetime64)
            df = df.drop_duplicates('date')
        except _network_error_classes:
            pass
        else:
            return df
    raise IOError("获取失败，请检查网络")

#获取复权股票日K线数据
def get_fq_day_data(code, retry_count=3, autype='qfq', index=False, pause=0.001):
    
    start = sd.get_past_year()
    end = sd.today()
    qs = sd.get_quarts(start, end)
    qt = qs[0]
    bs._write_head()
    data = _parse_fq_data(bs.HIST_FQ_URL%(bs.P_TYPE['http'], bs.DOMAINS['vsf'],
                              code, qt[0], qt[1]), retry_count, pause)
    if len(qs)>1:
        for d in range(1, len(qs)):
            qt = qs[d]
            bs._write_console()
            url = bs.HIST_FQ_URL%(bs.P_TYPE['http'], bs.DOMAINS['vsf'],
                                  code, qt[0], qt[1])
            df = _parse_fq_data(url, retry_count, pause)
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
        data = data.sort_index(ascending=False)
        return data
    else:
        for label in ['open', 'high', 'close', 'low']:
            data[label] = data[label] / data['factor']
        data = data.drop('factor', axis=1)
        
        if autype == 'qfq':
            df = _parase_fq_factor(code, start, end)
            df = df.drop_duplicates('date')
            df = df.sort('date', ascending=False)
            frow = df.head(1)
            df = pd.merge(data, df)
            preClose = float(get_realtime_quotes(code)['pre_close'])
            df = df[(df.date>=start) & (df.date<=end)]
            rate = preClose / float(frow['factor'])
            df['close_temp'] = df['close']
            df['close'] = rate * df['factor']
            for label in ['open', 'high', 'low']:
                df[label] = df[label] * (df['close'] / df['close_temp'])
                df[label] = df[label].map(bs.FORMAT)
            df = df.drop(['factor', 'close_temp'], axis=1)
            df['close'] = df['close'].map(bs.FORMAT)
            df = df.set_index('date')
            df = df.sort_index(ascending=False)
            df = df.astype(float)
            return df
        else:
            data = data[(data.date>=start) & (data.date<=end)]
            for label in ['open', 'high', 'close', 'low']:
                data[label] = data[label].map(bs.FORMAT)
            data = data.set_index('date')
            data = data.sort_index(ascending=False)
            data = data.astype(float)
            return data

#获取实时交易数据
def get_realtime_quotes(symbols=None):
    """
        获取实时交易数据 getting real time quotes data
       用于跟踪交易情况（本次执行的结果-上一次执行的数据）
    Parameters
    ------
        symbols : string, array-like object (list, tuple, Series).
        
    return
    -------
        DataFrame 实时交易数据
              属性:0：name，股票名字
            1：open，今日开盘价
            2：pre_close，昨日收盘价
            3：price，当前价格
            4：high，今日最高价
            5：low，今日最低价
            6：bid，竞买价，即“买一”报价
            7：ask，竞卖价，即“卖一”报价
            8：volumn，成交量 maybe you need do volumn/100
            9：amount，成交金额（元 CNY）
            10：b1_v，委买一（笔数 bid volume）
            11：b1_p，委买一（价格 bid price）
            12：b2_v，“买二”
            13：b2_p，“买二”
            14：b3_v，“买三”
            15：b3_p，“买三”
            16：b4_v，“买四”
            17：b4_p，“买四”
            18：b5_v，“买五”
            19：b5_p，“买五”
            20：a1_v，委卖一（笔数 ask volume）
            21：a1_p，委卖一（价格 ask price）
            ...
            30：date，日期；
            31：time，时间；
    """
    symbols_list = ''
    if type(symbols) is list or type(symbols) is set or type(symbols) is tuple or type(symbols) is pd.Series:
        for code in symbols:
            symbols_list += _code_to_symbol(code) + ','
    else:
        symbols_list = _code_to_symbol(symbols)
        
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
        df[txt] = df[txt].map(lambda x : x[:-2])
    return df

def _random(n=13):
    from random import randint
    start = 10**(n-1)
    end = (10**n)-1
    return str(randint(start, end))
