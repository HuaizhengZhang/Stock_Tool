#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test.py
Created by Huaizheng ZHANG on 7.8.
Copyright (c) 2015 zhzHNN. All rights reserved.

"""

import tushare as ts
import numpy as np
import stock_get as sg
import os
import datetime as dt
import pandas as pd
"""jingzichan = sg.get_fundholdshares_data("600733")
print jingzichan
HeadData = ts.get_hist_data(code="000517", start='2015-01-01',end='2015-07-09')
print len(HeadData)"""

###judge the dir
if os.path.isdir('Data'):
	pass
else:
	os.mkdir('Data')


StockBasics = sg.get_all_stock_list()
StockBasics.to_csv('Data/stock.csv',encoding='utf8')

StockCode,StockName = np.loadtxt('Data/stock.csv', dtype=str, delimiter=',' , skiprows=1, usecols=(0,1), unpack=True)

#np.savetxt('name.csv',StockCode,fmt='%s')
StockCode = StockCode.tolist()
StockName = StockName.tolist()


i = 0
length = len(StockCode)
temp_data = []
while i < length:
	dirname = StockCode[i] + '(' + StockName[i] + ')'

	print u'当前正在获取'.encode('utf-8') + dirname + u'第'.encode('utf-8')+ str(i+1) + u'个，共计'.encode('utf-8') + str(length)
#HeadData
	HeadData = ts.get_hist_data(code=StockCode[i], start='2015-01-01',end='2015-07-09')
	jingzichan, per_profit = sg.get_fundholdshares_data(code=StockCode[i])

	if type(HeadData) == pd.core.frame.DataFrame:
		if len(HeadData) > 0:
			if (jingzichan != 0) and (per_profit != 0):
				temp_data.append([str(StockCode[i]),
									StockName[i],
									HeadData.index[-1],
									round(HeadData["close"][-1],2),
									jingzichan,
									round((HeadData["close"][-1] / jingzichan),3),
									per_profit,
									round(HeadData["close"][-1] / (per_profit*4),3)])
				i = i+1
			elif (jingzichan != 0) and (per_profit == 0):
				temp_data.append([str(StockCode[i]),
									StockName[i],
									HeadData.index[-1],
									round(HeadData["close"][-1],2),
									jingzichan,
									round((HeadData["close"][-1] / jingzichan),3),
									per_profit,
									"无法计算"])
				i = i+1
			elif (jingzichan == 0) and (per_profit != 0):
				temp_data.append([str(StockCode[i]),
									StockName[i],
									HeadData.index[-1],
									round(HeadData["close"][-1],2),
									jingzichan,
									"无法计算",
									per_profit,
									round(HeadData["close"][-1] / (per_profit*4),3)])
				i = i+1
			elif (jingzichan == 0) and (per_profit == 0):
				temp_data.append([str(StockCode[i]),
									StockName[i],
									HeadData.index[-1],
									round(HeadData["close"][-1],2),
									jingzichan,
									"无法计算",
									per_profit,
									"无法计算"])
				i = i+1
			print temp_data
		else:
			i = i+1
	else:
		i = i+1

df = pd.DataFrame(temp_data)
df.columns = ["股票代码","股票名称","最新日期","最新价格","最新净资产价格","最新价格与净资产比值","最新季度每股收益","市盈率"]
df = df.set_index('股票代码')
df.to_csv('股票最新价格与净资产比值.csv')
print df
