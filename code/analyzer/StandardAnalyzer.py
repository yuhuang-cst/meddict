# encoding: UTF-8

"""
@author: hy
"""

import chardet

#状态机,标点用空格替代

class StandardAnalyzer(object):
	def __init__(self):
		self.currentType = self.__getType('')


	def split(self, s):
		s += '.'
		splitList = []
		begin = 0
		for i in range(len(s)):
			type = self.__getType(s[i])
			if self.currentType == 0:
				begin = i
			elif type > 2 or type != self.currentType:
				splitList.append(s[begin:i])
				begin = i
			self.currentType = type
		return splitList


	def __getType(self, c):
		if self.__isNum(c):			#连续
			return 1
		elif self.__isENG(c):		#连续
			return 2
		elif self.__isCNS(c):		#非连续
			return 3
		else:
			return 0

	def __isNum(self, c):
		return '\u0030' <= c <='\u0039'


	def __isENG(self, c):
		return ('\u0041' <= c <='\u005a') or ('\u0061' <= c <='\u007a')


	def __isCNS(self, c):
		return '\u4e00' <= c <= '\u9fff'


if __name__ == '__main__':
	analyzer = StandardAnalyzer()
	test = [
		'。是multi-ply打发了,23sf.。,维阿多少分、。223@*#(@#@&$*#).为何sjflds//)',
		'二棕榈酰卵磷脂',
		'Dipalmitoylphosphatidylcholine（物质）',
		'1,2双十六烷基锡甘油磷酸胆碱',
		'3,5,9-trioxa-4-phosphapentacosan-1-aminium，羟基，N，n-trimethyl-10-oxo-7 -（（1-oxohexadecyl）氧基）-内盐，4-oxide',
		'间质核的内侧纵束（博伊斯1895）',
		'后连合核的（KöKF）',
		'促性腺precocity家庭独立性（症）',
		'Pseudarthrobacter chlorophenolicus（Westerberg等人。2000）·2016',
		'甘油二酯激酶，Zeta 104-kd：dgkz',
		'总尿量尿病人的护理目标消除残余＜20%'
	]
	for s in test:
		print('--------------------------------')
		print('test:', s)
		for str in analyzer.split(s):
			print(str)
		print('')
