# encoding: UTF-8

"""
@author: hy
"""

import pickle
import json
import numpy as np
from scipy.sparse import save_npz, load_npz
import re
import os
from zhon import hanzi
import string
import pandas as pd
import time
import sys

from config import JSON_FILE_FORMAT, PKL_FILE_FORMAT, NPY_FILE_FORMAT, SPARSE_NPZ_FILE_FORMAT, NPZ_FILE_FORMAT


def splitPath(path):
	"""'a/b.json' -> ('a', 'b', '.json')
	"""
	folder, fullname = os.path.split(path)
	prefix, postfix = os.path.splitext(fullname)
	return folder, prefix, postfix


def isNum(c):
	return '\u0030' <= c <='\u0039'


def isENG(c):
	return ('\u0041' <= c <='\u005a') or ('\u0061' <= c <='\u007a')


def isCNS(c):
	return '\u4e00' <= c <= '\u9fff'


def containCNS(s):
	for c in s:
		if isCNS(c):
			return True
	return False


def containENG(s):
	for c in s:
		if isENG(c):
			return True
	return False


def allCNS(s):
	return re.match('^[\u4e00-\u9fff]+$', s) is not None


def allDigit(s):
	return re.match('^[\d零一二三四五六七八九十百千万亿]+$', s) is not None


def removeBracket(term):
	"""提取括号内容
	"""
	bracketPatten = '\[.*?\]|\(.*?\)|（.*?）|【.*?】|〔.*?〕'
	bracketTerms = [s[1:-1] for s in re.findall(bracketPatten, term)]
	return re.sub(bracketPatten, '', term), bracketTerms


def removeBeginEnd(term):
	"""去除首尾无效字符
	"""
	invalid = '([\s{cnsPunc}{engPunc}]|(NOS))+'.format(cnsPunc=hanzi.punctuation, engPunc=string.punctuation)
	term = re.sub('^'+invalid, '', term)
	term = re.sub(invalid+'$', '', term)
	return term


def removeUselessSpace(term):
	"""去除标点符号两侧的空格; 去掉[英文数字]和[汉字]之间的空白符; 连续多个空白符, 变为1个
	"""
	term = re.sub('\s*([{cnsPunc}{engPunc}]+)\s*'.format(cnsPunc=hanzi.punctuation, engPunc=string.punctuation), '\g<1>', term)
	term = re.sub('\s*([\u4e00-\u9fff]+)\s*', '\g<1>', term)
	term = re.sub('\s{2,}', ' ', term)
	return term


def containTime(term):
	"""包含时间词
	"""
	return re.search('(\d|一|二|两|三|四|五|六|七|八|九|十)+个?([秒|分|时|天|日|周|月|年]|小时)+', term) is not None


def containTemperature(term):
	"""包含温度词
	"""
	return re.search('\d+(度|摄氏度|华氏度)+', term) is not None


def containUselessDigitTerm(term):
	return containTime(term) or containTemperature(term)


def containPunc(term):
	return re.search('[{cnsPunc}{engPunc}]+'.format(cnsPunc=hanzi.punctuation, engPunc=string.punctuation), term) is not None


def uniqueList(l):
	return list(set(l))


def sortedByLength(termList):
	_, termList = zip(*sorted([(len(term), term) for term in termList]))
	return termList


def drawBarPlot(x, y, xOrder, xLabel, yLabel, figPath):
	import matplotlib.pyplot as plt
	import seaborn as sns
	plt.switch_backend('agg')   # ubuntu
	dirName = os.path.dirname(figPath); os.makedirs(dirName, exist_ok=True)
	fig, ax = plt.subplots()
	fig.set_size_inches(16, 8)
	sns.barplot(x=x, y=y, order=xOrder, ax=ax)
	plt.xlabel(xLabel)
	plt.ylabel(yLabel)
	plt.savefig(figPath)
	plt.close()


def termListStatic(termList, logPath, figPath):
	from collections import Counter
	counter = Counter()
	counter.update([len(term) for term in termList])
	x, y = zip(*counter.items())
	drawBarPlot(x, y, None, 'Length', 'Count', figPath)
	s = ''
	total = len(termList)
	accuNumber = 0
	for length, number in counter.items():
		accuNumber += number
		s += 'Length {length}: {number}/{total} = {ratio}%; accumulate={accuRatio}\n'.format(
			length=length, number=number, total=total, ratio=100.0*number/total, accuRatio=100.0*accuNumber/total
		)
	print(s, file=open(logPath, 'w'))


def removeStopwords(termList, stopwords=None):
	if stopwords is None:
		from config import DATA_PATH
		stopwords = set(open(DATA_PATH+os.sep+'stopwords'+os.sep+'stopwords.txt').read().splitlines())
	if not isinstance(stopwords, set):
		stopwords = set(stopwords)
	stopwords.add('')
	return [term for term in termList if term not in stopwords]


def dictListAdd(k, v, d):
	if k in d:
		d[k].append(v)
	else:
		d[k] = [v]


def dictSetAdd(k, v, d):
	if k in d:
		d[k].add(v)
	else:
		d[k] = {v}


def sameTerm(str1, str2):
	def normalize(str):
		return str.replace(' ', '').strip()
	return normalize(str1) == normalize(str2)


def getLoadFunc(fileFormat):
	if fileFormat == JSON_FILE_FORMAT:
		return lambda path: json.load(open(path))
	if fileFormat == PKL_FILE_FORMAT:
		return lambda path: pickle.load(open(path, 'rb'))
	if fileFormat == NPY_FILE_FORMAT or fileFormat == NPZ_FILE_FORMAT:
		return lambda path: np.load(path)
	if fileFormat == SPARSE_NPZ_FILE_FORMAT:
		return lambda path: load_npz(path)
	assert False


def getSaveFunc(fileFormat):
	if fileFormat == JSON_FILE_FORMAT:
		return lambda obj, path: json.dump(obj, open(path, 'w'), indent=2, ensure_ascii=False)
	if fileFormat == PKL_FILE_FORMAT:
		return lambda obj, path: pickle.dump(obj, open(path, 'wb'))
	if fileFormat == NPY_FILE_FORMAT:
		return lambda obj, path: np.save(path, obj)
	if fileFormat == NPZ_FILE_FORMAT:
		return lambda obj, path: np.savez_compressed(path, obj)
	if fileFormat == SPARSE_NPZ_FILE_FORMAT:
		return lambda obj, path: save_npz(path, obj)
	assert False


def loadSaveForFunc(filePath, fileFormat):
	def outerWrapper(func):
		def wrapper(*args, **kwargs):
			if os.path.exists(filePath):
				loadFunc = getLoadFunc(fileFormat)
				return loadFunc(filePath)
			obj = func(*args, **kwargs)
			saveFunc = getSaveFunc(fileFormat)
			saveFunc(obj, filePath)
			return obj
		return wrapper
	return outerWrapper


def checkLoadSave(attrCollector, attrPath, fileFormat):
	"""ref: http://lib.csdn.net/article/python/62942; https://blog.csdn.net/wait_for_eva/article/details/78036101
	"""
	def outerWrapper(func):
		def wrapper(cls):
			coll, path = getattr(cls, attrCollector), getattr(cls, attrPath)
			if coll is not None:
				return coll
			if os.path.exists(path):
				loadFunc = getLoadFunc(fileFormat)
				coll = loadFunc(path)
				setattr(cls, attrCollector, coll)
				return coll
			coll = func(cls)
			setattr(cls, attrCollector, coll)
			saveFunc = getSaveFunc(fileFormat)
			saveFunc(coll, path)
			return coll
		return wrapper
	return outerWrapper


def readFileFolder(dir, filterFunc, handleFunc):
	"""读取指定文件夹下所有指定扩展名的文件并进行处理
	Args:
		dir (string): 文件夹或文件路径
		filter (func): 筛选函数, 若 fileter(文件名) == True, 则执行handleFunc
		fileExtension (string): 文件扩展名
		handleFunc (func): 处理每个文件的函数; 参数: 文件名;
	"""
	if os.path.isfile(dir):
		if filterFunc(dir):
			handleFunc(dir)
	else:
		for fileName in os.listdir(dir):
			fileDir = os.path.join(dir,fileName)
			readFileFolder(fileDir, filterFunc, handleFunc)


def getFileList(dir, filter):
	"""获取dir目录下的所有符合条件的文件
	Args:
		dir (string): 文件夹或文件路径
		filter (func): 筛选函数, 若 fileter(文件名) == True, 则将文件路径加进返回列表; i.e. filter=lambda filePath: filePath.split('.').pop() == 'json'
	Returns:
		list: 文件名列表
	"""
	def handleFunc(filePath):
		fileList.append(filePath)
	fileList = []
	readFileFolder(dir, filter, handleFunc)
	return fileList


def isJsonable(x):
	try:
		json.dumps(x)
		return True
	except:
		return False


class Config(object):
	def __init__(self):
		pass

	def __str__(self):
		return '\n'.join('%s: %s' % item for item in self.__dict__.items())


	def save(self, path, deleteUnjson=False):
		if deleteUnjson:
			json.dump(self.jsonableFilter(self.__dict__), open(path, 'w'), indent=2)
		else:
			json.dump(self.__dict__, open(path, 'w'), indent=2)


	def load(self, path):
		self.assign(json.load(open(path)))


	def assign(self, valueDict):
		for key in valueDict:
			setattr(self, key, valueDict[key])


	def jsonableFilter(self, d):
		return {k:v for k, v in d.items() if isJsonable(v)}


def xlsxToList(path):
	"""
	Returns:
		list: [row1, row2, ...]; row={col1: value1, col2: value2}
	"""
	df = pd.read_excel(path)
	return df.to_dict(orient='records')


def xlsxToJson(inpath, outpath):
	json.dump(xlsxToList(inpath), open(outpath, 'w'), indent=2, ensure_ascii=False)


def timer(func):
	def wrapper(*args, **kwargs):
		print('{0} starts running...'.format(func.__name__))
		startTime = time.time()
		ret = func(*args, **kwargs)
		print('Function {0} finished. Total time cost: {1} seconds'.format(func.__name__, time.time()-startTime))
		return ret
	return wrapper


def printAtFixPos(text):
	print(text, end='\r')


if __name__ == '__main__':
	from config import DATA_PATH
	xlsxPath = DATA_PATH+'/thesaurus/cn/SNOMED/BDWK/snomed对照表100.xlsx'
	jsonPath = DATA_PATH+'/thesaurus/cn/SNOMED/BDWK/snomed对照表100.json'
	xlsxToJson(xlsxPath, jsonPath)
	pass


