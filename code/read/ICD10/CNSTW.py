# encoding: UTF-8

"""
@author: hy
"""

import xlrd
from opencc import OpenCC
from tqdm import tqdm

def readSheet(sheet):
	dataDict = {}
	for row in range(2, sheet.nrows, 2):
		code = sheet.cell(row, 0).value.strip()
		eng = sheet.cell(row, 1).value.strip()
		cns = sheet.cell(row+1, 1).value.strip()
		dataDict[code] = {'eng': eng, 'cns': cns}
	return dataDict


def readICD10CM(xlsPath):
	xls = xlrd.open_workbook(xlsPath)
	sheetNames = [
		'Chapter 1', 'Chapter 2', 'Chapter 3', 'Chapter 4', 'Chapter 5', 'Chapter 6',
		'Chapter 7', 'Chapter 8', 'Chapter 9', 'Chapter 10', 'Chapter 11', 'Chapter 12',
		'Chapter 13', 'Chapter 14', 'Chapter 15', 'Chapter 16', 'Chapter 17', 'Chapter 18',
		'Chapter 19-1', '19-2', 'Chapter 19-2', 'Chapter 20', 'Chapter 21'
	]
	dataDict = {}
	for sheetName in tqdm(sheetNames):
		sheet = xls.sheet_by_name(sheetName)
		dataDict = dict(dataDict, **readSheet(sheet))
	cc = OpenCC('t2s')
	for code, infoDict in dataDict.items():
		infoDict['cns'] = cc.convert(infoDict['cns'])
	return dataDict


if __name__ == '__main__':
	from config import DATA_PATH
	import os
	import json
	folder = DATA_PATH+os.sep+'thesaurus'+os.sep+'cn'+os.sep+'ICD10'+os.sep+'cn-tw'
	dataDict = readICD10CM(folder+os.sep+'27651_1_1.1 中文版ICD-10-CM(106.01.11更新).xlsx')
	json.dump(dataDict, open(folder+os.sep+'27651_1_1.1 中文版ICD-10-CM(106.01.11更新).json', 'w'), indent=2, ensure_ascii=False)

	for code, infoDict in dataDict.items():
		print(code, ':', infoDict['cns'])
	print('size:', len(dataDict))


