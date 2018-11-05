# encoding: UTF-8

"""
@author: hy
"""

from common import *
import requests
from bs4 import BeautifulSoup


def readRawCookies(path):
	rawCookies = open(path).read()
	cookies = {}
	for pair in rawCookies.split(';'):
		key, value = map(lambda x: x.strip(), pair.split('=', 1))
		cookies[key] = value
	return cookies


def getNextUrl(readerDetails):
	readertDetailLink = readerDetails.find('div', class_='readertdetaillink')
	next = readertDetailLink.p.next_sibling.next_sibling
	if next:
		nextUrl = 'http://mall.cnki.net/reference/' + next.a['href']
	else:
		nextUrl = ''
	return nextUrl


def addTerm(engTerm, cnsTerm, list):
	list.append(utf8(engTerm + u'\u3000' + cnsTerm))


def splitString(str, sep, times):
	return map(lambda x: x.strip(), str.split(sep, times))


def fileWrite(f, code, termList):
	print code
	f.write(code + '\n')
	for line in termList:
		f.write(line + '\n')
	f.write('\n')


def getString(node):
	return u''.join(node.strings)

def readUrl(url, cookiesDict):
	global f
	termList = []
	htmlDoc = requests.get(url, cookies=cookiesDict).text
	soup = BeautifulSoup(htmlDoc)

	readerDetails = soup.find('div', class_='readerdetails')
	code, engTerm = splitString(getString(readerDetails.h1), u'\u3000', 1)

	readerDetailsCon = readerDetails.find('div', class_='readerdetailscon')
	pList = readerDetailsCon.find_all('p')
	cnsTerm = getString(pList[0]).strip()
	termList.append(utf8(engTerm + u'\u3000' + cnsTerm))
	for i in range(1, len(pList)):
		line = getString(pList[i]).strip()
		if line:
			termList.append(utf8(line))

	fileWrite(f, code, termList)
	return getNextUrl(readerDetails)


url = 'http://mall.cnki.net/reference/ref_readerItem.aspx?bid=R200908044&recid=R2009080440000004'
cookiesDict = readRawCookies('rawCookie.txt')
f = file('英汉对照国际医学规范术语全集-精选本.txt', 'w')

#for i in range(10):
while url:
	url = readUrl(url, cookiesDict)

f.close()










