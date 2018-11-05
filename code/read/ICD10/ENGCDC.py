# encoding: UTF-8

"""
@author: hy
"""

def addPoint(code):
	if len(code) > 3:
		return code[:3] + '.' + code[3:]
	else:
		return code

def readICD_ENSCDC_TXT(path):
	dict = {}
	for line in open(path).readlines():
		code = addPoint(line[6:14].strip())
		entry = line[77:].strip()
		dict[code] = entry
	return dict


if __name__ == '__main__':
	ensDict = readICD_ENSCDC_TXT('/Users/apple/Documents/coding/research/graduation_project/ICD10/en/CDC/icd10cm_order_2017.txt')

	print('size:', len(ensDict))
	for key in ensDict:
		print(key, ':', ensDict[key])
	pass