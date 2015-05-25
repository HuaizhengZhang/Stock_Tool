#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test.py
Created by Huaizheng ZHANG on 5.18.
Copyright (c) 2015 zhzHNN. All rights reserved.

"""

#print(sg.get_fq_day_data('002024'))

#print(sg.get_realtime_quotes('000581'))
#sg.get_fq_day_data('002024').to_csv('002024复权数据.csv',encoding='utf8')
#temp = sg.get_sharebonus_1_data('002024')
#temp.to_csv('0020242分红（新浪网）.csv',encoding='utf8')
#print(temp)

#print(sg.get_all_stock_list())
#sg.get_all_stock_list().to_csv('全部股票数据.csv',encoding='utf8')
#sg.get_realtime_quotes('002024').T.to_csv('002024实时数据.csv',encoding='utf8')

import stock_get as sg


#print(sg.get_stock_structure('002024'))
sg.get_stock_structure('000009').to_csv('000009.csv', header=False,encoding='utf8')

"""if sg.get_stock_structure('300431'):
	print('TRUE')
else:
	print('FALSE')"""