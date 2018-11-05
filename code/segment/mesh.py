# encoding: UTF-8

"""
@author: hy
"""

from tqdm import tqdm
import re
from segment.tool import removeBracket, uniqueList, sortedByLength, removeBeginEnd, isCNS, allDigit
from segment.tool import removeStopwords, removeUselessSpace, containPunc, containUselessDigitTerm

def genSegmentTermList(termList):
	termList = uniqueList([removeUselessSpace(term) for term in termList]) # 去除无用空白符

	termList = [removeBeginEnd(term) for term in tqdm(termList)] # 去除首尾无效字符

	temp = []   # 根据标点拆分词条
	for term in tqdm(termList):
		subList = [subword.strip() for subword in re.split('[，,]', term)]
		temp.extend(subList)
	termList = uniqueList(temp)
	print('size={}'.format(len(termList)))

	termList = [term for term in termList if not containPunc(term)] # 去掉包含标点的词
	termList = [term for term in termList if not allDigit(term)]   # 去掉纯数字
	termList = [term for term in termList if not containUselessDigitTerm(term)] # 去掉包含时间词、温度词的词
	termList = [term for term in termList if not (len(term) == 1 and not isCNS(term))]  # 去掉非汉字单字

	termList = removeStopwords(termList)    # 去除停用词
	termList = uniqueList(termList)
	print('size={}'.format(len(termList)))
	return sortedByLength(termList)


if __name__ == '__main__':
	from read.MeSH.CNSCHISC import readMESH_CNSCHISC_TXT
	from config import DATA_PATH, RESULT_PATH
	import os
	folder = RESULT_PATH+os.sep+'segment'+os.sep+'thesaurus'; os.makedirs(folder, exist_ok=True)
	dataDict = readMESH_CNSCHISC_TXT(DATA_PATH+os.sep+'thesaurus'+os.sep+'cn'+os.sep+'MeSH'+os.sep+'chisc'+os.sep+'Mesh-医学主题词表.txt')
	termList = list(dataDict.values())
	termList = genSegmentTermList(termList)
	print('\n'.join(termList), file=open(folder+os.sep+'mesh.txt', 'w'))
