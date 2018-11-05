# encoding: UTF-8

"""
@author: hy
"""


import numpy as np
from tqdm import tqdm
import re
from segment.tool import removeBracket, uniqueList, removeBeginEnd, sortedByLength, containCNS, allDigit
from segment.tool import removeStopwords, removeUselessSpace, containPunc, containUselessDigitTerm

def genSnomedctSegment(termList):
	termList = uniqueList([removeUselessSpace(term) for term in termList]) # 去除无用空白符
	temp = []   # 提取括号内容
	for term in tqdm(termList):
		newTerm, bracketTerm = removeBracket(term)
		temp.append(newTerm)
		temp.extend(bracketTerm)
	termList = uniqueList(temp)
	print('size={}'.format(len(termList)))

	termList = [removeBeginEnd(term) for term in tqdm(termList)] # 去除首尾无效字符
	print('size={}'.format(len(termList)))

	temp = []   # 根据标点拆分词条
	for term in tqdm(termList):
		subList = [subword.strip() for subword in re.split('[，,:：]', term)]
		temp.extend(subList)
	termList = uniqueList(temp)
	print('size={}'.format(len(termList)))

	termList = [term for term in termList if not containPunc(term)] # 去掉包含标点的词
	termList = [term for term in termList if not allDigit(term)]   # 去掉纯数字
	termList = [term for term in termList if not containUselessDigitTerm(term)] # 去掉包含时间词、温度词的词
	print('size={}'.format(len(termList)))

	termList = [term for term in termList if len(term) > 1 and containCNS(term)]    # 长度大于1 且 包含中文
	print('size={}'.format(len(termList)))

	termList = removeStopwords(termList)    # 去除停用词
	termList = uniqueList(termList) # 去重
	print('size={}'.format(len(termList)))
	return sortedByLength(termList)


def genSnomedSegment(termList):
	termList = uniqueList([removeUselessSpace(term) for term in termList]) # 去除无用空白符

	termList = [removeBeginEnd(term) for term in tqdm(termList)] # 去除首尾无效字符
	print('size={}'.format(len(termList)))

	temp = []   # 根据标点拆分词条, 取第一段
	for term in tqdm(termList):
		temp.append(re.split('[，,]', term, maxsplit=1)[0])
	termList = uniqueList(temp)
	print('size={}'.format(len(termList)))

	termList = [term for term in termList if not containPunc(term)] # 去掉包含标点的词
	termList = [term for term in termList if not allDigit(term)]   # 去掉纯数字
	termList = [term for term in termList if not containUselessDigitTerm(term)] # 去掉包含时间词、温度词的词

	termList = removeStopwords(termList)    # 去除停用词
	termList = uniqueList(termList) # 去重
	print('size={}'.format(len(termList)))
	return sortedByLength(termList)



if __name__ == '__main__':
	from read.SNOMED.CNSCMIA import readSNOMED_CNSCMIA_TXT
	from config import DATA_PATH, RESULT_PATH
	import os
	import pandas as pd
	folder = RESULT_PATH+os.sep+'segment'+os.sep+'thesaurus'; os.makedirs(folder, exist_ok=True)

	def snomedct():
		df = pd.read_csv(DATA_PATH+os.sep+'thesaurus'+os.sep+'cn'+os.sep+'SNOMED'+os.sep+'wenku'+os.sep+'snomed对照表.csv')
		termSet = set(df['CNOMEN'].tolist()); termSet.remove(np.nan)
		termList = list(termSet)
		termList = genSnomedctSegment(termList)
		print('\n'.join(termList), file=open(folder+os.sep+'snomedct.txt', 'w'))

	def snomed():
		dataDict = readSNOMED_CNSCMIA_TXT(DATA_PATH+os.sep+'thesaurus'+os.sep+'cn'+os.sep+'SNOMED'+os.sep+'CMIA'+os.sep+'英汉对照国际医学规范术语全集-精选本.txt')
		termList = [infoDict['cns'] for k, infoList in dataDict.items() for infoDict in infoList]
		termList = genSnomedSegment(termList)
		print('\n'.join(termList), file=open(folder+os.sep+'snomed.txt', 'w'))

	snomedct()
	snomed()












