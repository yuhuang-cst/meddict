# encoding: UTF-8

"""
@author: hy
"""

from read.MeSH.ENGNLM import readMESH_ENGNLM_BIN

decideTrans = {
	'D006610': '高压性神经综合征',
	'D053648': '细胞因子受体公共β亚单位',
	'D016282': '天冬氨酸内肽酶',
	'D051762': 'PAX2转录因子',
	'D061065': '聚酮化合物',
	'D020805': '中枢神经系统病毒感染',
	'D051498': '受体，成纤维细胞生长因子，3型',
	'D051567': '原癌基因蛋白质c-vav',
	'D051757': 'B细胞特异性活化蛋白质',
	'D051922': 'PII氮调节蛋白质类',
	'D053472': 'Nod信号接头蛋白质类',
	'D051761': '成对盒转录因子类',
	'D053594': '髓样分化因子88'
}


def readMESH_CNSCHISC_TXT(path):
	treeDict = {}
	for line in open(path).readlines():
		if line.strip() == '':
			continue
		temp = [word for word in line.split(' ', maxsplit=1)]
		assert temp[0] not in treeDict		#检查重复性
		treeDict[temp[0]] = temp[1]
	return treeDict


def sameTerm(str1, str2):
	def normalize(str):
		return str.replace(' ', '').strip()
	return normalize(str1) == normalize(str2)


def readMESH_CNSCHISC(CNSCHISC_PATH, ENGNLM_PATH):
	CNSTreeDict = readMESH_CNSCHISC_TXT(CNSCHISC_PATH)
	ENGDataList = readMESH_ENGNLM_BIN(ENGNLM_PATH)
	treeMapCode = {}
	for mTermDict in ENGDataList:
		assert len(mTermDict['UI']) == 1		#检查UI唯一性
		UI = mTermDict['UI'][0]
		if 'MN' not in mTermDict:		#(D005260, Female) 与 (D008297, Male) 没有'MN'
			print('(%s, %s) lack MN' % (UI, mTermDict['MH'][0]))
			continue
		for treePos in mTermDict['MN']:
			assert treePos not in treeMapCode		#检查treePos唯一性
			treeMapCode[treePos] = UI
	dataDict = {}
	mapFailedTreePos = []
	emptyCount = 0
	for treePos, CNS in CNSTreeDict.items():
		if CNS.strip() == '':
			emptyCount += 1
			continue
		if treePos not in treeMapCode:
			mapFailedTreePos.append(treePos)
			continue
		code = treeMapCode[treePos]
		if code in dataDict:		#存在多个treePos对应同一个UI
			if not sameTerm(dataDict[code], CNS):		#若存在歧义, 则人工选择其翻译
				dataDict[code] = decideTrans[code]
			continue
		dataDict[code] = CNS
	print('%d/%d tree pos not match' % (len(mapFailedTreePos), len(CNSTreeDict)))
	print('empty CNS: %d' % (emptyCount))
	return dataDict


if __name__ == '__main__':
	def script1():
		dataDict = readMESH_CNSCHISC(
			'/Users/apple/Documents/coding/research/graduation_project/Mesh/cn/chisc/Mesh-医学主题词表.txt',
			'/Users/apple/Documents/coding/research/graduation_project/Mesh/en/NLM/ascii/d2017.bin'
		)

		for treePos in dataDict.keys()[0:10]:
			print(treePos, ':', dataDict[treePos])
		print(len(dataDict))

	def script2():
		from config import DATA_PATH
		import os
		folder = DATA_PATH+os.sep+'thesaurus'+os.sep+'cn'+os.sep+'MeSH'+os.sep+'chisc'
		dataDict = readMESH_CNSCHISC_TXT(folder+os.sep+'Mesh-医学主题词表.txt')
		for treeCode, cns in dataDict.items():
			print('{}: {}'.format(treeCode, cns))
		print('size: {}'.format(len(dataDict)))

	script2()
