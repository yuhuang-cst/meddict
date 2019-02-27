# encoding: UTF-8

"""
@author: hy
"""

from common import isCNS, isENG

def tokenEqualList(wordList1, wordList2):
	return wordList1 == wordList2


def tokenEqual(s1, s2, analyzer):
	return tokenEqualList(analyzer.split(s1), analyzer.split(s2))


def bagOfWords01EqualList(wordList1, wordList2):
	return set(wordList1) == set(wordList2)


def bagOfWords01Equal(s1, s2, analyzer):
	return bagOfWords01EqualList(analyzer.split(s1), analyzer.split(s2))


def bagOfWordsEqualList(wordList1, wordList2):
	def genBagOfWords(wordList):
		wordDict = {}
		for word in wordList:
			if word in wordDict:
				wordDict[word] += 1
			else:
				wordDict[word] = 1
		return wordDict
	return genBagOfWords(wordList1) == genBagOfWords(wordList2)


def bagOfWordsEqual(s1, s2, analyzer):
	bagOfWordsEqualList(analyzer.split(s1), analyzer.split(s2))


def calCNSRate(wordList):
	if len(wordList) == 0:
		return 0.0
	return sum(map(lambda x: 1 if isCNS(x) else 0, wordList)) * 1.0 / len(wordList)


def negENGCount(wordList):
	return -sum(map(lambda x: 1 if isENG(x) else 0, wordList))