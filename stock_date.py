#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
stock_date.py
Created by Huaizheng ZHANG on 5.16.
Copyright (c) 2015 zhzHNN. All rights reserved.

"""
import pandas as pd
import datetime

def year_qua(date):
    mon = date[5:7]
    mon = int(mon)
    return[date[0:4], _quar(mon)]
    

def _quar(mon):
    if mon in [1, 2, 3]:
        return '1'
    elif mon in [4, 5, 6]:
        return '2'
    elif mon in [7, 8, 9]:
        return '3'
    elif mon in [10, 11, 12]:
        return '4'
    else:
        return None
 
 
def today():
    day = datetime.datetime.today().date()
    return str(day) 

def get_year():
    year = datetime.datetime.today().year
    return year

def get_month():
    month = datetime.datetime.today().month
    return month

def get_past_year():
    #lasty = datetime.datetime.today().date() - datetime.timedelta(days=1095)
    lasty = '2000-01-04'
    return str(lasty)


def get_quarts(start, end):
    idx = pd.period_range('Q'.join(year_qua(start)), 'Q'.join(year_qua(end)),
                          freq='Q-JAN')
    return [str(d).split('Q') for d in idx]
