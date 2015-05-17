#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
stock_main.py
Created by Huaizheng ZHANG on 5/11.
Copyright (c) 2015 zhzHNN. All rights reserved.

"""
import stock_get as sg

#print(sg.get_fq_day_data('002024'))

#print(sg.get_realtime_quotes('000581'))

temp = sg.get_sharebonus_1_data('000002')
temp.to_csv('000002分红（新浪网）.csv',encoding='utf8')
#print(temp)