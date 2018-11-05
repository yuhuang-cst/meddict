# encoding: UTF-8

"""
@author: hy
"""

def readSNOMED_ENGCMIA_MAP_TXT(path):
	def addMap(conceptID, simpleID):
		if conceptID in mapDict:
			mapDict[conceptID].append(simpleID)
		else:
			mapDict[conceptID] = [simpleID]
	lines = open(path).readlines()
	mapDict = {}
	for i in range(1, len(lines)):
		ref = lines[i].split('\t')
		conceptID, simpleID = ref[5].strip(), ref[6].strip()
		addMap(conceptID, simpleID)
	return mapDict

if __name__ == '__main__':
	mapDict = readSNOMED_ENGCMIA_MAP_TXT('/Users/apple/Documents/coding/research/graduation_project/SNOMED/en/NLM/SnomedCT_InternationalRF2_Production_20170131T120000/Full/Refset/Map/der2_sRefset_SimpleMapFull_INT_20170131.txt')

	print('size:', len(mapDict))
	for key in mapDict:
		print(key, ':', mapDict[key])

