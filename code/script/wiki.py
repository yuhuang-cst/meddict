# encoding: UTF-8

"""
@author: hy
"""


def readWikiTermList(filepath):
	lines = open(filepath).read().splitlines()
	return [line.split('\t', maxsplit=1).pop().strip() for line in lines]


def convert():
	import os
	from opencc import OpenCC
	from tqdm import tqdm
	from config import DATA_PATH
	folder = DATA_PATH+os.sep+'wiki'
	wikiList = open(folder+os.sep+'zhwiki-20181020-all-titles').read().splitlines()
	cc = OpenCC('t2s')
	simpleList = []
	for term in tqdm(wikiList):
		simpleList.append(cc.convert(term))
	print('\n'.join(simpleList), file=open(folder+os.sep+'sim_zhwiki-20181020-all-titles', 'w'))


if __name__ == '__main__':
	convert()