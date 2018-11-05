# encoding: UTF-8

"""
@author: hy
"""

try:
	import xml.etree.cElementTree as ET
except ImportError:
	import xml.etree.ElementTree as ET


def readICD_ENSWHO_XML(path):
	"""读取ICD-10英文XML文件
	Args:
		path(str): 文件路径
	Return:
		dict: {'A00': 'Cholera', ...}, utf-8
	"""
	def getLabelText(l):
		str = ''
		for child in l.getchildren():
			str += (child.text if child.text else '')
			str += (child.tail if child.tail else '')
		str += (l.text if l.text else '')
		return str

	if path.split('.').pop() != 'xml':
		return
	tree = ET.parse(path)
	root = tree.getroot()
	dict = {}
	for Class in root.iter('Class'):
		if 'code' in Class.attrib:
			Rubrics = Class.findall('Rubric')
			chooseRubrics = None
			for Rubric in Rubrics:
				if 'kind' in Rubric.attrib and Rubric.attrib['kind'] == 'preferredLong':
					chooseRubrics = Rubric
				if 'kind' in Rubric.attrib and Rubric.attrib['kind'] == 'preferred' and chooseRubrics == None:
					chooseRubrics = Rubric
			if chooseRubrics:
				Label = chooseRubrics.find('Label')
				key, value = Class.attrib['code'], getLabelText(Label)
				dict[key] = value
	return dict


if __name__ == '__main__':
	ensDict = readICD_ENSWHO_XML('/Users/apple/Documents/coding/research/graduation_project/ICD10/en/WHO/icdClaML2016ens/icdClaML2016ens.xml')

	print('size:', len(ensDict))
	for key in ensDict:
		print(key, ':', ensDict[key])