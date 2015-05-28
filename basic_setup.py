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
           'afi': 'app.finance.ifeng.com'}

HIST_FQ_COLS = ['date', 'open', 'high', 'close', 'low', 'volumn', 'amount', 'factor']
HIST_FQ_URL = '%s%s/corp/go.php/vMS_FuQuanMarketHistory/stockid/%s.phtml?year=%s&jidu=%s'
HIST_INDEX_URL = '%s%s/corp/go.php/vMS_MarketHistory/stockid/%s/type/S.phtml?year=%s&jidu=%s'
HIST_FQ_FACTOR_URL = '%s%s/api/json.php/BasicStockSrv.getStockFuQuanData?symbol=%s&type=hfq'


FORMAT = lambda x: '%.2f' % x

LIVE_DATA_URL = '%shq.%s/rn=%s&list=%s'
LIVE_DATA_COLS = ['name', 'open', 'pre_close', 'price', 'high', 'low', 'bid', 'ask', 'volume', 'amount',
                  'b1_v', 'b1_p', 'b2_v', 'b2_p', 'b3_v', 'b3_p', 'b4_v', 'b4_p', 'b5_v', 'b5_p',
                  'a1_v', 'a1_p', 'a2_v', 'a2_p', 'a3_v', 'a3_p', 'a4_v', 'a4_p', 'a5_v', 'a5_p', 'date', 'time', 's']

SHAREBONUS_URL = '%s%s/corp/go.php/vISSUE_ShareBonus/stockid/%s.phtml'
SHAREBONUS_1_COLS = ['公告日期',	'送股(股)', '转增(股)', '派息(税前)(元)', '进度', '除权除息日', '股权登记日',
					 '红股上市日', '查看详细', 'del1', 'del2']

SHAREBONUS_2_COLS = ['公告日期', '配股方案(每10股配股股数)', '配股价格(元)', '基准股本(万股)', '除权日', 
					 '股权登记日', '缴款起始日', '缴款终止日', '配股上市日', '募集资金合计(元)','查看详细','del']

ALL_STOCK_LIST = '%s%s/hq/list.php?type=stock_a&class=%s'

STOCK_STRUCTURE_URL = '%s%s/corp/go.php/vCI_StockStructure/stockid/%s.phtml'

import sys
PY3 = (sys.version_info[0] >= 3)
def _write_head():
    sys.stdout.write("[获取数据中:]")
    sys.stdout.flush()

def _write_console():
    sys.stdout.write("&")
    sys.stdout.flush()