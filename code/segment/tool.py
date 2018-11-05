# encoding: UTF-8

"""
@author: hy
"""

import re
import os
from zhon import hanzi
import string

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


def dictSetAdd(k, v, d):
	if k in d:
		d[k].add(v)
	else:
		d[k] = set([v])


if __name__ == '__main__':
	pass