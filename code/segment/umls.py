# encoding: UTF-8

"""
@author: hy
"""

import re
from tqdm import tqdm
import pickle
import json
import random
import os
import requests
from multiprocessing import Pool
from common import uniqueList, removeBracket, removeBeginEnd, sortedByLength, containUselessDigitTerm
from common import  termListStatic, removeStopwords, removeUselessSpace, containCNS, allCNS, allDigit
from common import dictListAdd
from config import DATA_PATH, RESULT_PATH
from script.wiki import readWikiTermList


def genAllTermList():
	gradedMT = pickle.load(open(DATA_PATH+os.sep+'umlsMT'+os.sep+'GradedMT.pkl', 'rb'))
	termDict = {}
	for AUI, infoDict in tqdm(gradedMT.items()):
		for term in infoDict['source'].values():
			dictListAdd(term, AUI, termDict)
	termList, mapInfo = zip(*termDict.items())
	folder = RESULT_PATH+os.sep+'preprocess'+os.sep+'umls'; os.makedirs(folder, exist_ok=True)
	pickle.dump(termList, open(folder+os.sep+'allTerms.pkl', 'wb'))
	print(random.sample(termList, 10000), file=open(folder+os.sep+'allTerms_10000.json', 'w'))
	pickle.dump(mapInfo, open(folder+os.sep+'allTermsMapInfo.pkl', 'wb'))


def genSegmentTermList(termList):
	termList = uniqueList([removeUselessSpace(term) for term in termList]) # 去除无用空白符
	print('size={}'.format(len(termList)))
	termList = [term for term in tqdm(termList) if len(term) > 1 and containCNS(term)]   # 初筛: 长度大于1 且 包含中文
	print('size={}'.format(len(termList)))

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
		subList = re.split('[，；;]', term) # 按标点切分(考查了中英符号: 逗号,句号,冒号,分号)
		subList = [subword.strip() for subword in subList]
		temp.extend(subList)
	termList = uniqueList(temp)
	print('size={}'.format(len(termList)))

	termList = [term for term in tqdm(termList) if not allDigit(term)]   # 去掉纯数字
	termList = [term for term in tqdm(termList) if not containUselessDigitTerm(term)] # 去掉包含时间词、温度词的词

	termList = [removeBeginEnd(term) for term in tqdm(termList)] # 去除首尾无效字符
	print('size={}'.format(len(termList)))
	termList = [term for term in tqdm(termList) if len(term) > 1 and len(term) < 20 and allCNS(term)]    # 终筛: 长度大于1 且 长度小于20 且 全中文
	print('size={}'.format(len(termList)))

	termList = removeStopwords(termList)    # 去除停用词
	termList = uniqueList(termList) # 去重
	print('size={}'.format(len(termList)))
	return sortedByLength(termList) # 按长度排序


def baiduBaikeCheck(term):
	url = 'https://baike.baidu.com/item/{}'.format(term)
	headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
	r = requests.get(url, headers=headers)
	r.raise_for_status()
	return term if r.text.startswith('<!DOCTYPE html>\n<!--STATUS OK-->') else None


def baiduBaikeFilter(termList, baikeSet=None):
	def onlineCheck():
		retTermList = []
		with Pool() as pool:
			for term in tqdm(pool.imap_unordered(baiduBaikeCheck, termList), total=len(termList), leave=False):
				if term is not None:
					retTermList.append(term)
		return retTermList
	def offlineCheck(baikeSet):
		if not isinstance(baikeSet, set):
			baikeSet = set(baikeSet)
		return [term for term in termList if term in baikeSet]
	if baikeSet is None:
		return onlineCheck()
	else:
		return offlineCheck(baikeSet)


def wikiPediaFilter(termList):
	wikiSet = set( readWikiTermList(DATA_PATH+os.sep+'wiki'+os.sep+'sim_zhwiki-20181020-all-titles') )
	return [term for term in tqdm(termList) if term in wikiSet]


if __name__ == '__main__':
	folder = RESULT_PATH+os.sep+'segment'+os.sep+'umls'; os.makedirs(folder, exist_ok=True)
	def umlsSegmentScript():
		umls = pickle.load(open(RESULT_PATH+os.sep+'preprocess'+os.sep+'umls'+os.sep+'allTerms.pkl', 'rb'))
		termList = genSegmentTermList(umls)
		print('\n'.join(termList), file=open(folder+os.sep+'umls.txt', 'w'))
		print('\n'.join(random.sample(termList, 10000)), file=open(folder+os.sep+'umls_10000.json', 'w'))
		# json.dump(termList, open(folder+os.sep+'umls.json', 'w'), indent=2, ensure_ascii=False)

	def baiduBaikeScript():
		import logging
		logging.getLogger("requests").setLevel(logging.WARNING)
		logging.getLogger("urllib3").setLevel(logging.WARNING)
		termList = json.load(open(folder+os.sep+'umls.json'))
		termList = sortedByLength(baiduBaikeFilter(termList))
		print('\n'.join(termList), file=open(folder+os.sep+'umls_baidubaike.txt', 'w'))

	def wikiPediaScript():
		termList = open(folder+os.sep+'umls.txt').read().splitlines()
		termList = sortedByLength(wikiPediaFilter(termList))
		print('\n'.join(termList), file=open(folder+os.sep+'umls_wikipedia.txt', 'w'))

	def baikeScript():
		termList = uniqueList(open(folder+os.sep+'umls_wikipedia.txt').read().splitlines() + open(folder+os.sep+'umls_baidubaike.txt').read().splitlines())
		termList = sortedByLength(termList)
		print('size={}'.format(len(termList)))
		print('\n'.join(termList), file=open(folder+os.sep+'umls_baike.txt', 'w'))

	def statScript():
		termList = open(folder+os.sep+'umls.txt').read().splitlines()
		termListStatic(termList, folder+os.sep+'umls.stat', folder+os.sep+'umls.png')

	# genAllTermList()
	# umlsSegmentScript()
	statScript()
	# baiduBaikeScript()
	# wikiPediaScript()
	# baikeScript()



