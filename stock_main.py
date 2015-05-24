#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
stock_main.py
Created by Huaizheng ZHANG on 5/11.
Copyright (c) 2015 zhzHNN. All rights reserved.

"""

import numpy as np
import stock_get as sg
import os
import datetime as dt

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
while i < length:
	dirname = StockCode[i] + '(' + StockName[i] + ')'
	
	if os.path.isdir('Data/'+dirname): 
		pass
	else: 
		os.mkdir('Data/'+dirname)
	
	print u'当前正在获取'.encode('utf-8') + dirname + u'第'.encode('utf-8')+ str(i+1) + u'个，共计'.encode('utf-8') + str(length)
#HeadData
	try:
		HeadData = sg.get_fq_day_data(code=StockCode[i], autype='qfq')
	except ValueError, e:
		print u'复权日K线数据出错了，跳过'.encode('utf-8')
	Filename = dirname + u'复权日K线数据(前复权)'.encode('utf-8') + '.csv'
	if os.path.exists('Data/'+ dirname + '/' + Filename):
		os.remove('Data/'+ dirname + '/' + Filename)
		HeadData.to_csv('Data/'+ dirname + '/' + Filename, columns=['open','high','low','close','volumn'])
	else:
		HeadData.to_csv('Data/'+ dirname + '/' + Filename, columns=['open','high','low','close','volumn']) 
#KDate
	try:
		KData = sg.get_fq_day_data(code=StockCode[i], autype=None)
	except ValueError, e:
		print u'日K线数据出错了，跳过'.encode('utf-8')
	Filename = dirname + u'日K线数据(新浪网)'.encode('utf-8') + '.csv'
	if os.path.exists('Data/'+ dirname + '/' + Filename):
		os.remove('Data/'+ dirname + '/' + Filename)
		KData.to_csv('Data/'+ dirname + '/' + Filename, columns=['open','high','low','close','volumn'])
	else:
		KData.to_csv('Data/'+ dirname + '/' + Filename, columns=['open','high','low','close','volumn']) 
#real_time_data
	try:
		Realtime_Data = sg.get_realtime_quotes(StockCode[i]).T
	except ValueError, e:
		print u'实时行情数据出错了，跳过'.encode('utf-8')
	Filename = dirname + u'实时行情数据(新浪网)'.encode('utf-8') + '.csv'
	if os.path.exists('Data/'+ dirname + '/' + Filename):
		os.remove('Data/'+ dirname + '/' + Filename)
		Realtime_Data.to_csv('Data/'+ dirname + '/' + Filename,encoding='utf8')
	else:
		Realtime_Data.to_csv('Data/'+ dirname + '/' + Filename,encoding='utf8')

#sharebonus_data
	try:
		Sharebonus_1_Data = sg.get_sharebonus_1_data(StockCode[i])
		Sharebonus_2_Data = sg.get_sharebonus_2_data(StockCode[i])
	except ValueError, e:
		print u'分红派息数据数据出错了，跳过'.encode('utf-8')
	Filename = dirname + u'分红派息数据(新浪网)'.encode('utf-8') + '.csv'
	if os.path.exists('Data/'+ dirname + '/' + Filename):
		os.remove('Data/'+ dirname + '/' + Filename)
		Sharebonus_1_Data.to_csv('Data/'+ dirname + '/' + Filename,encoding='utf8')
		Sharebonus_2_Data.to_csv('Data/'+ dirname + '/' + Filename, mode='a', encoding='utf8')
	else:
		Sharebonus_1_Data.to_csv('Data/'+ dirname + '/' + Filename,encoding='utf8')
		Sharebonus_2_Data.to_csv('Data/'+ dirname + '/' + Filename, mode='a', encoding='utf8')  
	
	i = i+1

