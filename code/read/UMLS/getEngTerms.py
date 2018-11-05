# encoding: UTF-8

"""
@author: hy
"""

from ReadMrConso import *

def examineAUI(dataList):
	"""检查AUI是否重复"""
	judger = set()
	for termDict in dataList:
		if termDict['AUI'] not in judger:
			judger.add(termDict['AUI'])
		else:
			print('warning:', termDict['AUI'], 'repeated')


def getEngTerms(dataList):
	AUIs = []
	terms = []
	rankRecorder = {}
	for termDict in dataList:
		if termDict['LAT'] == 'ENG':
			if termDict['STR'] not in rankRecorder:
				rankRecorder[termDict['STR']] = len(terms)
				terms.append(termDict['STR'])
				AUIs.append([termDict['AUI']])
			else:
				AUIs[rankRecorder[termDict['STR']]].append(termDict['AUI'])
	return AUIs, terms


def countCharactersNum(termList):
	count = 0
	for term in termList:
		count += len(term)
	return count


def countCUI(dataList):
	CUISet = set()
	for termDict in dataList:
		if termDict['CUI'] in CUISet:
			continue
		CUISet.add(termDict['CUI'])
	return len(CUISet)


def countIsPref(dataList):
	countPref = 0
	countPrefCharacter = 0
	for termDict in dataList:
		if termDict['ISPREF'] == 'Y':
			countPref += 1
			countPrefCharacter += len(termDict['STR'])
	return countPref, countPrefCharacter


if __name__ == '__main__':
	import json
	sourcePath = '/Users/apple/Documents/coding/research/graduation_project/UMLS/Metathesaurus/2016AB-full/2016AB/2016AB/META/MRCONSO_HY_SMALL.RRF'

	print('reading', sourcePath)
	dataList = readMRCONSO_RRF(sourcePath)
	print('read complete, total terms:', len(dataList))

	# print 'counting charactersNum'
	# print 'characters number:', countCharactersNum([termDict['STR'] for termDict in dataList])

	# print 'examining AUI...'
	# examineAUI(dataList)
	# print 'done'

	# print 'counting CUI'
	# print 'CUI Number:', countCUI(dataList)
	#
	# print 'counting isPreffer'
	# prefNum, prefCharacNum = countIsPref(dataList)
	# print 'isPreffer number:', prefNum
	# print 'characters number:', prefCharacNum

	print('getting unique English terms')
	AUIList, termList = getEngTerms(dataList)
	assert len(AUIList) == len(termList)
	print('total unique English terms:', len(AUIList))

	print('counting characters')
	charactersNum = countCharactersNum(termList)
	print('character number:',charactersNum)

	print('saving as json')
	json.dump(AUIList, open('AUI.json', 'w'), indent=2, ensure_ascii=False)
	json.dump(termList, open('termENG.json', 'w'), indent=2, ensure_ascii=False)
	print('done')

