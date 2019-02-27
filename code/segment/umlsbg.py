# encoding: UTF-8

"""
@author: hy
"""

import pickle
import os
import re
from tqdm import tqdm
from config import DATA_PATH, RESULT_PATH
from analyzer.StandardAnalyzer import StandardAnalyzer
from common import removeBracket, uniqueList, removeBeginEnd, sortedByLength, containCNS, allDigit, allCNS
from common import removeStopwords, removeUselessSpace, containPunc, containUselessDigitTerm

def genBGUnorderEqual():
	"""取百度翻译和谷歌翻译无序相等
	"""
	gradedMT = pickle.load(open(DATA_PATH+os.sep+'umlsMT'+os.sep+'GradedMT.pkl', 'rb'))
	termList = []
	analyzer = StandardAnalyzer()
	for AUI, infoDict in tqdm(gradedMT.items()):
		if infoDict['confidence'] > 5:
			continue
		baidu = infoDict['source'].get('baidu', '')
		google = infoDict['source'].get('google', '')
		if set(analyzer.split(baidu)) == set(analyzer.split(google)):   # 百度翻译与谷歌翻译无序相等
			termList.append(baidu)
			termList.append(google)
	termList = uniqueList(termList)
	return termList


def genSegmentTermList(termList):
	termList = uniqueList([removeUselessSpace(term) for term in termList]) # 去除无用空白符

	termList = [removeBeginEnd(term) for term in tqdm(termList)] # 去除首尾无效字符
	termList = [term for term in termList if not allDigit(term)]   # 去掉纯数字
	termList = [term for term in termList if not containUselessDigitTerm(term)] # 去掉包含时间词、温度词的词
	termList = [term for term in termList if len(term) > 1 and len(term) < 20 and allCNS(term)]    # 终筛: 长度大于1 且 长度小于20 且 仅包含中文

	termList = removeStopwords(termList)    # 去除停用词
	termList = uniqueList(termList) # 去重
	print('size={}'.format(len(termList)))
	return sortedByLength(termList)


if __name__ == '__main__':
	folder = RESULT_PATH+os.sep+'segment'+os.sep+'umls'
	def script1():
		termList = genBGUnorderEqual()
		termList = genSegmentTermList(termList)
		print('\n'.join(termList), file=open(folder+os.sep+'umls_bgequal.txt', 'w'))

	def script2():
		from segment.umls import baiduBaikeFilter, wikiPediaFilter
		termList = open(folder+os.sep+'umls_bgequal.txt').read().splitlines()
		baiduTermList = baiduBaikeFilter(termList, open(folder+os.sep+'umls_baidubaike.txt').read().splitlines())
		wikiTermList = wikiPediaFilter(termList)
		termList = sortedByLength(uniqueList(baiduTermList + wikiTermList))
		print('size: {}'.format(len(termList)))
		print('\n'.join(termList), file=open(folder+os.sep+'umls_bgequal_baike.txt', 'w'))

	script1()
	script2()