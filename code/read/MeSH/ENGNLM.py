# encoding: UTF-8

"""
@author: hy
"""

def handleLine(line):
	"""
	Args:
		line (str): 'a = b'
	Returns:
		str, str: 'a', 'b'
	"""
	list = line.split('=')
	return list[0].strip(), list[1].strip()


def readMESH_ENGNLM_BIN(path):
	def addKey(l):
		key, value = handleLine(l)
		if key in term:
			term[key].append(value)
		else:
			term[key] = [value]

	def addTerm():
		data.append(term)
		# if len(data) % 1000 == 0:
		# 	print len(data)

	data = []
	term = {}
	lastLine = ''
	for line in open(path).readlines():
		if line == '\n':
			continue
		if line == '*NEWRECORD\n':
			if term:
				addKey(lastLine)
				addTerm()
				term = {}
				lastLine = ''
		else:
			if line.find('=') == -1 or not lastLine:		#该行无等于号
				lastLine += line
			else:
				addKey(lastLine)
				lastLine = line
	if term:
		addKey(lastLine)
		addTerm()
	return data


if __name__ == '__main__':
	import json
	dataList = readMESH_ENGNLM_BIN('/Users/apple/Documents/coding/research/graduation_project/Mesh/en/NLM/ascii/d2017.bin')
	json.dump(dataList, open('/Users/apple/Documents/coding/research/graduation_project/Mesh/en/NLM/ascii/d2017.json', 'w'), indent=2, ensure_ascii=False)

	# ensDict = {term['UI'][0]:term['MH'][0] for term in dataList}
	#
	# print 'size:', len(ensDict)
	# for key in ensDict:
	# 	print key, ':', ensDict[key]