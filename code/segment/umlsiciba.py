# encoding: UTF-8

"""
@author: hy
"""

import pickle
import os
from tqdm import tqdm
import re
from config import DATA_PATH, RESULT_PATH
from common import uniqueList, removeBeginEnd, sortedByLength, containCNS, allDigit
from common import removeStopwords, removeUselessSpace, containPunc, containUselessDigitTerm


def isDescription(term):
	"""判断是否为叙述性的话语
	"""
	# q1 = re.match('^(是|为)?(一[种|条|根|个])', term)
	q2 = re.search('因为|由于|(一[种|条|根|个])|是|能将|属于|甚至|(用[于|来])', term) is not None
	return q2


def getICIBATermList():
	"""取金山词霸
	"""
	termList = []
	gradedMT = pickle.load(open(DATA_PATH+os.sep+'umlsMT'+os.sep+'GradedMT.pkl', 'rb'))
	for AUI, infoDict in tqdm(gradedMT.items()):
		if 'ICIBA' in infoDict['source']:
			termList.append(infoDict['source']['ICIBA'])
	termList = uniqueList(termList)
	return termList


def genSegmentTermList(termList):
	termList = uniqueList([removeUselessSpace(term) for term in termList]) # 去除无用空白符

	termList = [removeBeginEnd(term) for term in tqdm(termList)] # 去除首尾无效字符
	termList = [term for term in termList if not isDescription(term)]   # 去掉叙述性的语句

	temp = []   # 根据标点拆分词条
	for term in tqdm(termList):
		subList = [subword.strip() for subword in re.split('[，,]', term)]
		temp.extend(subList)
	termList = uniqueList(temp)
	print('size={}'.format(len(termList)))

	termList = [term for term in termList if not containPunc(term)] # 去掉包含标点的词
	termList = [term for term in termList if not allDigit(term)]   # 去掉纯数字
	termList = [term for term in termList if not containUselessDigitTerm(term)] # 去掉包含时间词、温度词的词

	termList = [term for term in termList if len(term) > 1 and len(term) < 20 and containCNS(term)]    # 长度大于1 且 长度小于20 且 包含中文
	termList = [term for term in termList if re.match('^见[\w]+', term) is None]

	termList = removeStopwords(termList)    # 去除停用词
	termList = uniqueList(termList) # 去重
	print('size={}'.format(len(termList)))
	return sortedByLength(termList)


if __name__ == '__main__':
	folder = RESULT_PATH+os.sep+'segment'+os.sep+'umls'
	termList = getICIBATermList()
	termList = genSegmentTermList(termList)
	print('\n'.join(termList), file=open(folder+os.sep+'umls_iciba.txt', 'w'))
