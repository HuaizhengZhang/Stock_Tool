#data = {'index':temp_index,'data1':temp_data1,'data2':temp_data2,'data3':temp_data3,'data4':temp_data4}
"""df = pd.DataFrame(temp)

Filename = dirname + u'股票最新价格与净资产比值'.encode('utf-8') + '.csv'
if os.path.exists('Data/'+ dirname + '/' + Filename):
	os.remove('Data/'+ dirname + '/' + Filename)
	HeadData.to_csv('Data/'+ dirname + '/' + Filename, columns=['open','high','low','close','volumn'])
else:
	HeadData.to_csv('Data/'+ dirname + '/' + Filename, columns=['open','high','low','close','volumn'])"""



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

"""Volumn = np.loadtxt('000009复权数据.csv',delimiter=',' , skiprows=1, usecols=(5,), unpack=True)
for x in xrange(0,239):
	Volumn[x] = Volumn[x+300]
for x in xrange(0,234):
	sum = (Volumn[x+1] + Volumn[x+2] + Volumn[x+3] + Volumn[x+4] + Volumn[x+5]) / 5
	Volumn[x] = Volumn[x] / sum
	print Volumn[x]
np.savetxt('000009test.csv',Volumn,fmt='%s')"""



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
