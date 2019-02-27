# encoding: UTF-8

"""
@author: hy
"""

from common import printAtFixPos

def readMRCONSO_RRF(path):
	"""
	Args:
		path (str): .RRF
	Returns:
		list: [rowItem, ...]; rowItem={'CUI': CUI, 'LAT': LAT, ...}
	"""
	colNames = ['CUI', 'LAT', 'TS', 'LUI', 'STT', 'SUI', 'ISPREF', 'AUI', 'SAUI', 'SCUI', 'SDUI', 'SAB', 'TTY', 'CODE', 'STR', 'SRL', 'SUPPRESS', 'CVF']
	colNum = len(colNames)
	list = []
	count = 0
	for line in open(path).readlines():
		valueList = line.split('|')
		valueList.pop()
		list.append({colNames[i]:valueList[i] for i in range(colNum)})
		count += 1
		if count % 100000 == 0:
			printAtFixPos('UMLS RRF READ: {}'.format(count))
	return list


def readUMLS_ENG(path):
	"""
	Args:
		path (str): .RRF
	Returns:
		list: [rowItem, ...]; rowItem={'CUI': CUI, 'LAT': LAT, ...}
	"""
	dataList = readMRCONSO_RRF(path)
	return [termDict for termDict in dataList if termDict['LAT'] == 'ENG']


def readMRDEF_RRF(path):
	colNames = ['CUI', 'AUI', 'ATUI', 'SATUI', 'SAB', 'DEF', 'SUPPRESS', 'CVF']
	colNum = len(colNames)
	list = []
	for line in open(path).readlines():
		valueList = line.split('|')
		valueList.pop()
		list.append({colNames[i]:valueList[i] for i in range(colNum)})
	return list


if __name__ == '__main__':
	sourcePath = '/Users/apple/Documents/coding/research/graduation_project/UMLS/Metathesaurus/2016AB-full/2016AB/2016AB/META/MRCONSO_HY_SMALL.RRF'

	print('reading', sourcePath)
	dataList = readMRCONSO_RRF(sourcePath)
	print('read complete, total terms:', len(dataList))

