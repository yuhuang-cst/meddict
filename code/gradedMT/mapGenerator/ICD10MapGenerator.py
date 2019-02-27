# encoding: UTF-8

"""
@author: hy
"""

import json

from gradedMT.mapGenerator.MapGenerator import MapGenerator
from common import checkLoadSave, sameTerm
from config import DATA_PATH, JSON_FILE_FORMAT, ICD10_SOURCE
from read.ICD10.CNSGOV import readICD10_4Digit
from read.ICD10.ENGCDC import readICD_ENSCDC_TXT
from read.UMLS.ReadMrConso import readUMLS_ENG


class ICD10MapGenerator(MapGenerator):
	def __init__(self):
		super(ICD10MapGenerator, self).__init__()
		self.source = ICD10_SOURCE
		self.MAP_JSON = DATA_PATH + '/umlsMT/map/UMLSMapICD10.json'
		self.mapDict = None


	@checkLoadSave('mapDict', 'MAP_JSON', JSON_FILE_FORMAT)
	def getAUIMapDict(self):
		"""
		Returns:
			dict: {AUI: {'code': code, 'eng': ENG, 'cns': CNS)}
		"""
		ICD10_CNSGOV = readICD10_4Digit(DATA_PATH+'/thesaurus/cn/ICD-10/cn-gov/4位代码亚目表(ICD-10).xls')
		ICD10CM_CNSTW = json.load(open(DATA_PATH+'/thesaurus/cn/ICD-10/cn-tw/CNSTW.json'))
		ICD10CM_ENGCDC = readICD_ENSCDC_TXT(DATA_PATH+'/thesaurus/en/ICD10/CDC/icd10cm_order_2017.txt')
		UMLSDataList = readUMLS_ENG(DATA_PATH+'/umlsMT/umls/MRCONSO.RRF')
		mapDict = {}
		for uTermDict in UMLSDataList:
			if (uTermDict['SAB']== 'ICD10AM' or uTermDict['SAB'] == 'ICD10CM' or uTermDict['SAB'] == 'ICD10' or uTermDict['SAB'] == 'ICD10AMAE'):
				AUI = uTermDict['AUI']
				code = uTermDict['CODE']
				ENG = uTermDict['STR']
				CNS = None
				if code in ICD10_CNSGOV:		#优先采用ICD10_CNSGOV
					if code in ICD10CM_ENGCDC:		#能双保险验证则双保险验证
						if sameTerm(ENG, ICD10CM_ENGCDC[code]):
							CNS = ICD10_CNSGOV[code]
					else:
						CNS = ICD10_CNSGOV[code]
				elif code in ICD10CM_CNSTW:
					if sameTerm(ENG, ICD10CM_CNSTW[code]['eng']):		#双保险
						CNS = ICD10CM_CNSTW[code]['cns']
				if CNS:
					mapDict[AUI] = ({'code': code, 'eng': ENG, 'cns': CNS})
		return mapDict


