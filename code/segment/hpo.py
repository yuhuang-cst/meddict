# encoding: UTF-8

"""
@author: hy
"""

from tqdm import tqdm
import re
from segment.tool import removeBracket, uniqueList, sortedByLength, removeBeginEnd, allDigit
from segment.tool import removeStopwords, removeUselessSpace, containPunc, containUselessDigitTerm


def genSegmentTermList(termList):
	termList = uniqueList([removeUselessSpace(term) for term in termList]) # 去除无用空白符

	temp = []   # 提取括号内容
	for term in tqdm(termList):
		newTerm, bracketTerm = removeBracket(term)
		temp.append(newTerm)
		temp.extend(bracketTerm)
	termList = uniqueList(temp)
	print('size={}'.format(len(termList)))

	termList = [removeBeginEnd(term) for term in tqdm(termList)] # 去除首尾无效字符

	termList = [term for term in termList if not containPunc(term)] # 去掉包含标点的词
	termList = [term for term in termList if not allDigit(term)]   # 去掉纯数字
	termList = [term for term in termList if not containUselessDigitTerm(term)] # 去掉包含时间词、温度词的词

	termList = removeStopwords(termList)    # 去除停用词
	termList = uniqueList(termList)
	print('size={}'.format(len(termList)))
	return sortedByLength(termList)


if __name__ == '__main__':
	from read.HPO.readCHPO import readCHPO
	from config import RESULT_PATH, DATA_PATH
	import os
	folder = RESULT_PATH+os.sep+'segment'+os.sep+'thesaurus'; os.makedirs(folder, exist_ok=True)
	dataDict = readCHPO(DATA_PATH+os.sep+'thesaurus'+os.sep+'cn'+os.sep+'HPO'+os.sep+'chpo.2016-10.xls')
	termList = [infoDict['cns'] for k, infoDict in dataDict.items()]
	termList = genSegmentTermList(termList)
	print('\n'.join(termList), file=open(folder+os.sep+'hpo.txt', 'w'))