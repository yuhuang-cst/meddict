# encoding: UTF-8

"""
@author: hy
"""

import xlrd

def readCHPO(xlsPath):
	sheet = xlrd.open_workbook(xlsPath).sheet_by_name('CHPO')
	dataDict = {}
	for row in range(1, sheet.nrows):
		code, eng, cns = sheet.cell(row, 1).value, sheet.cell(row, 2).value, sheet.cell(row, 3).value
		dataDict[code] = {'eng':eng, 'cns':cns}
	return dataDict


if __name__ == '__main__':
	from config import DATA_PATH
	import os
	folder = DATA_PATH+os.sep+'thesaurus'+os.sep+'cn'+os.sep+'HPO'
	dataDict = readCHPO(folder+os.sep+'chpo.2016-10.xls')
	ensDict = {code:dataDict[code]['eng'] for code in dataDict}
	cnsDict = {code:dataDict[code]['cns'] for code in dataDict}

	print('size:', len(dataDict))
	for key in cnsDict:
		print(key, ':', cnsDict[key])

