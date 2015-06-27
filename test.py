#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test.py
Created by Huaizheng ZHANG on 5.18.
Copyright (c) 2015 zhzHNN. All rights reserved.

"""
import stock_get as sg
import numpy as np
#print(sg.get_fq_day_data('002024'))

#print(sg.get_realtime_quotes('000581'))
#sg.get_fq_day_data('000009').to_csv('000009复权数据.csv',encoding='utf8')


"""Volumn = np.loadtxt('000009复权数据.csv',delimiter=',' , skiprows=1, usecols=(5,), unpack=True)
for x in xrange(0,481):
	Volumn[x] = Volumn[x+534]
for x in xrange(0,476):
	sum = (Volumn[x+1] + Volumn[x+2] + Volumn[x+3] + Volumn[x+4] + Volumn[x+5]) / 5
	Volumn[x] = Volumn[x] / sum
	print Volumn[x]
np.savetxt('000009train.csv',Volumn,fmt='%s')"""

Volumn = np.loadtxt('000009复权数据.csv',delimiter=',' , skiprows=1, usecols=(5,), unpack=True)
for x in xrange(0,239):
	Volumn[x] = Volumn[x+300]
for x in xrange(0,234):
	sum = (Volumn[x+1] + Volumn[x+2] + Volumn[x+3] + Volumn[x+4] + Volumn[x+5]) / 5
	Volumn[x] = Volumn[x] / sum
	print Volumn[x]
np.savetxt('000009test.csv',Volumn,fmt='%s')



"""for x in xrange(0,3563):
	if x+5 < 3400:
		lb[x] =Volumn[x] / ((Volumn[x+1] + Volumn[x+2]+ Volumn[x+3]+ Volumn[x+4]+ Volumn[x+5])/5)
print lb"""
#temp = sg.get_sharebonus_1_data('002024')
#temp.to_csv('0020242分红（新浪网）.csv',encoding='utf8')
#print(temp)

#print(sg.get_all_stock_list())
#sg.get_all_stock_list().to_csv('全部股票数据.csv',encoding='utf8')
#sg.get_realtime_quotes('002024').T.to_csv('002024实时数据.csv',encoding='utf8')




#print(sg.get_stock_structure('002024'))
#sg.get_stock_structure('000009').to_csv('000009.csv', header=False,encoding='utf8')

"""if sg.get_stock_structure('300431'):
	print('TRUE')
else:
	print('FALSE')"""