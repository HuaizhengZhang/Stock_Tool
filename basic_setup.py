#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
basic_setup.py
Created by Huaizheng ZHANG on 5/11.
Copyright (c) 2015 zhzHNN. All rights reserved.

"""
K_TYPE = {'D': 'akdaily', 'W': 'akweekly', 'M': 'akmonthly'}
K_LABELS = ['D', 'W', 'M']
K_MIN_LABELS = ['5', '15', '30', '60']

INDEX_LABELS = ['sh', 'sz', 'hs300', 'sz50', 'cyb', 'zxb']

DAY_PRICE_COLUMNS = ['date', 'open', 'high', 'close', 'low', 'volume', 'price_change', 'p_change',
                     'ma5', 'ma10', 'ma20', 'v_ma5', 'v_ma10', 'v_ma20', 'turnover']
INX_DAY_PRICE_COLUMNS = ['date', 'open', 'high', 'close', 'low', 'volume', 'price_change', 'p_change',
                         'ma5', 'ma10', 'ma20', 'v_ma5', 'v_ma10', 'v_ma20']

DAY_PRICE_URL = '%sapi.finance.%s/%s/?code=%s&type=last'
DAY_PRICE_MIN_URL = '%sapi.finance.%s/akmin?scode=%s&type=%s'

P_TYPE = {'http': 'http://'}

DOMAINS = {'sina': 'sina.com.cn', 'sinahq': 'sinajs.cn',
           'ifeng': 'ifeng.com', 'sf': 'finance.sina.com.cn',
           'vsf': 'vip.stock.finance.sina.com.cn', 
           'idx':'www.csindex.com.cn', '163':'money.163.com',
           'em':'eastmoney.com'}
PAGES = {'fd': 'index.phtml', 'dl': 'downxls.php', 'jv': 'json_v2.php',
         'cpt': 'newFLJK.php', 'ids': 'newSinaHy.php', 'lnews':'rollnews_ch_out_interface.php',
         'ntinfo':'vCB_BulletinGather.php', 'hs300b':'000300cons.xls',
         'hs300w':'000300closeweight.xls','sz50b':'000016cons.xls',
         'dp':'all_fpya.php', '163dp':'fpyg.html',
         'emxsg':'JS.aspx', '163fh':'jjcgph.php',
         'newstock':'vRPD_NewStockIssue.php', 'zz500b':'000905cons.xls',
         't_ticks':'vMS_tradedetail.php'}

HIST_FQ_FACTOR_URL = '%s%s/api/json.php/BasicStockSrv.getStockFuQuanData?symbol=%s&type=qfq'
HIST_FQ_COLS = ['date', 'open', 'high', 'close', 'low', 'volumn', 'amount', 'factor']
HIST_FQ_URL = '%s%s/corp/go.php/vMS_FuQuanMarketHistory/stockid/%s.phtml?year=%s&jidu=%s'

FORMAT = lambda x: '%.2f' % x

LIVE_DATA_URL = '%shq.%s/rn=%s&list=%s'
LIVE_DATA_COLS = ['name', 'open', 'pre_close', 'price', 'high', 'low', 'bid', 'ask', 'volume', 'amount',
                  'b1_v', 'b1_p', 'b2_v', 'b2_p', 'b3_v', 'b3_p', 'b4_v', 'b4_p', 'b5_v', 'b5_p',
                  'a1_v', 'a1_p', 'a2_v', 'a2_p', 'a3_v', 'a3_p', 'a4_v', 'a4_p', 'a5_v', 'a5_p', 'date', 'time', 's']

import sys
PY3 = (sys.version_info[0] >= 3)
def _write_head():
    sys.stdout.write("[获取数据中:]")
    sys.stdout.flush()

def _write_console():
    sys.stdout.write("#")
    sys.stdout.flush()