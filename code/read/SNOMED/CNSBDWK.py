# encoding: UTF-8

"""
@author: hy
"""

from common import xlsxToList, dictListAdd


def readSNOMED_CNSBDWK_XLSX(path):
	"""
	Returns:
		dict: {code: [{'eng': engTerm1, 'cns': cnsTerm1}]}
	"""
	dataList = xlsxToList(path)
	retDict = {}
	for rowItem in dataList:
		dictListAdd(rowItem['TERMCODE'], {'cns': rowItem['CNOMEN'], 'eng': rowItem['ENOMEN']}, retDict)
	return retDict



if __name__ == '__main__':
	pass





