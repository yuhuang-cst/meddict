# encoding: UTF-8

"""
@author: hy
"""

def splitString(str, sep, times):
	return map(lambda x: x.strip(), str.split(sep, times))

def readSNOMED_CNSCMIA_TXT(path):
	"""
	Args:
		dict: {}
	"""
	import re
	dataDict = {}
	code = ''
	pattern = re.compile('(.*?)(C?[0-9]+(\.\.?)([0-9]|-)+(.*))?$')		#example: ['Third degree burn injury 949.3', 'Fourth ventricle，NOS C71.7', 'Blighted ovum 631.-', 'Pulmonary alveolar microlithiasis 516..2', 'Pseudogout，NOS 275.4 —712.3*', 'Atheromatous plaque，NOS', 'Intracranial subdural space']

	for line in open(path).readlines():
		if line == '\n':
			code = ''
			continue
		if not code:
			code = line.strip()
			dataDict[code] = []
		else:
			if line[0] == '(':
				continue
			wordList = line.split('|')
			eng = ''.join(wordList[:-1]).strip(); cns = wordList[-1].strip()
			eng = pattern.match(eng).group(1).strip()
			eng = eng.replace('，', ', ')
			dataDict[code].append({'eng': eng, 'cns': cns})
	return dataDict


if __name__ == '__main__':
	from config import DATA_PATH
	import os
	dataDict = readSNOMED_CNSCMIA_TXT(DATA_PATH+os.sep+'thesaurus'+os.sep+'cn'+os.sep+'SNOMED'+os.sep+'CMIA'+os.sep+'英汉对照国际医学规范术语全集-精选本.txt')
	print('size:', len(dataDict))
	for key in dataDict:
		print(key)
		for d in dataDict[key]:
			print(d['eng'], ':', d['cns'])
		print('')


