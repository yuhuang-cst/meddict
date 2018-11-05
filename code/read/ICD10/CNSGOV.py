# encoding: UTF-8

"""
@author: hy
"""

import xlrd

def readXLS3(xlsPath):
	sheet = xlrd.open_workbook(xlsPath).sheet_by_name('类目')
	dataDict = {}
	for row in range(2, sheet.nrows):
		key, value = sheet.cell(row, 0).value, sheet.cell(row, 1).value
		key, value = key.strip(), value.strip()
		dataDict[key] = value
	return dataDict


def readXLS4(xlsPath):
	sheet = xlrd.open_workbook(xlsPath).sheet_by_name('亚目')
	dataDict = {}
	for row in range(2, sheet.nrows):
		key, value = sheet.cell(row, 1).value, sheet.cell(row, 2).value
		key, value = key.strip(), value.strip()
		dataDict[key] = value
	return dataDict


def readXLS6(xlsPath):
	sheet = xlrd.open_workbook(xlsPath).sheet_by_name('kue')
	dataDict = {}
	for row in range(2, sheet.nrows):
		key1, key2, value = sheet.cell(row, 1).value, sheet.cell(row, 2).value, sheet.cell(row, 3).value
		key1, key2, value = key1.strip(), key2.strip(), value.strip()
		if key1:
			dataDict[key1] = value
		elif key2:
			dataDict[key2] = value
	return dataDict


def readTumourXLS(xlsPath):
	sheet = xlrd.open_workbook(xlsPath).sheet_by_name('icd4m')
	dataDict = {}
	for row in range(2, sheet.nrows):
		key, value = sheet.cell(row, 0).value, sheet.cell(row, 1).value
		key, value = key.strip(), value.strip()
		dataDict[key] = value
	return dataDict


def readICD10_4Digit(filename):
	dataDict = readXLS4(filename)
	return {k: v for k, v in dataDict.items() if len(v.strip()) != 0}


def readICD10():
	from config import DATA_PATH
	import os
	folder = DATA_PATH+os.sep+'thesaurus'+os.sep+'cn'+os.sep+'ICD10'+os.sep+'cn-gov'+os.sep+'ICD-10'
	cnsDict = {}
	cnsDict = dict(cnsDict, **readXLS3(folder+os.sep+'3位代码类目表(ICD-10).xls'))
	cnsDict = dict(cnsDict, **readXLS4(folder+os.sep+'4位代码亚目表(ICD-10).xls'))
	cnsDict = dict(cnsDict, **readXLS6(folder+os.sep+'6位扩展代码表.xls'))
	cnsDict = dict(cnsDict, **readTumourXLS(folder+os.sep+'肿瘤形态学编码(ICD-10字典库).xls'))
	return cnsDict


if __name__ == '__main__':
	cnsDict = readICD10()

	for key in cnsDict:
		print(key, ':', cnsDict[key])
	print('size:', len(cnsDict))






