# encoding: UTF-8

"""
@author: hy
"""

from tool import uniqueList, sortedByLength
from config import RESULT_PATH
import os


def combine(pathList):
	termList = []
	for path in pathList:
		termList.extend(open(path).read().splitlines())
	return sortedByLength(uniqueList(termList))


if __name__ == '__main__':
	THESAURUS_PATH = RESULT_PATH+os.sep+'segment'+os.sep+'thesaurus'
	UMLS_PATH = RESULT_PATH+os.sep+'segment'+os.sep+'umls'
	COMBINE_PATH = RESULT_PATH+os.sep+'segment'+os.sep+'combine'

	def scriptHuman():
		pathList = [
			THESAURUS_PATH+os.sep+'hpo.txt',
			THESAURUS_PATH+os.sep+'icd10_gov.txt',
			THESAURUS_PATH+os.sep+'mesh.txt',
			THESAURUS_PATH+os.sep+'snomed.txt',
			THESAURUS_PATH+os.sep+'snomedct.txt',
		]
		termList = combine(pathList)
		print('size={}'.format(len(termList)))
		print('\n'.join(termList), file=open(COMBINE_PATH+os.sep+'meddict_human.txt', 'w'))

	def scriptHumanMachine():
		pathList = [
			THESAURUS_PATH+os.sep+'hpo.txt',
			THESAURUS_PATH+os.sep+'icd10_gov.txt',
			THESAURUS_PATH+os.sep+'mesh.txt',
			THESAURUS_PATH+os.sep+'snomed.txt',
			THESAURUS_PATH+os.sep+'snomedct.txt',
			UMLS_PATH+os.sep+'umls_iciba.txt',
			UMLS_PATH+os.sep+'umls_bgequal.txt',
			UMLS_PATH+os.sep+'umls_baike.txt',
		]
		termList = combine(pathList)
		print('size={}'.format(len(termList)))
		print('\n'.join(termList), file=open(COMBINE_PATH+os.sep+'meddict_human_machine.txt', 'w'))

	scriptHuman()
	scriptHumanMachine()















