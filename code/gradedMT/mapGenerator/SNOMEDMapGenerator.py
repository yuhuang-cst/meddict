# encoding: UTF-8

"""
@author: hy
"""

from gradedMT.mapGenerator.MapGenerator import MapGenerator
from common import checkLoadSave, sameTerm
from config import DATA_PATH, JSON_FILE_FORMAT, SNOMED_SNMI_SOURCE, SNOMED_BDWK_SOURCE
from read.SNOMED.CNSCMIA import readSNOMED_CNSCMIA_TXT
from read.SNOMED.ENGNLM_MAP import readSNOMED_ENGCMIA_MAP_TXT
from read.SNOMED.CNSBDWK import readSNOMED_CNSBDWK_XLSX
from read.UMLS.ReadMrConso import readUMLS_ENG


class SNOMEDMapGenerator(MapGenerator):
	def __init__(self):
		super(SNOMEDMapGenerator, self).__init__()


	def getAUIMapDict(self):
		raise NotImplementedError


	def getAUIMapDict1(self, SNOMEDDataDict, UMLSDataList):
		"""SAB == 'SNMI
		"""
		UMLSMapSNMI = {}
		for uTermDict in UMLSDataList:
			if uTermDict['SAB']== 'SNMI' and uTermDict['CODE'] in SNOMEDDataDict:
				AUI = uTermDict['AUI']
				code = uTermDict['CODE']
				ENG = uTermDict['STR']

				for d in SNOMEDDataDict[code]:
					if sameTerm(d['eng'], ENG):
						CNS = d['cns']
						UMLSMapSNMI[AUI] = ({'code': code, 'eng': ENG, 'cns': CNS})
		return UMLSMapSNMI


	def getAUIMapDict2(self, SNOMEDDataDict, UMLSDataList):
		"""SAB == 'SNOMEDCT_US'
		"""
		CSCodeMap = readSNOMED_ENGCMIA_MAP_TXT(DATA_PATH+'/thesaurus/en/SNOMED/NLM/SnomedCT_InternationalRF2_Production_20170131T120000/Full/Refset/Map/der2_sRefset_SimpleMapFull_INT_20170131.txt')
		UMLSMapSNOMED_US = {}
		for uTermDict in UMLSDataList:
			if uTermDict['SAB'] == 'SNOMEDCT_US' and uTermDict['CODE'] in CSCodeMap:
				AUI = uTermDict['AUI']
				code = uTermDict['CODE']
				ENG = uTermDict['STR']
				for simpleID in CSCodeMap[code]:
					if simpleID not in SNOMEDDataDict:
						continue
					for d in SNOMEDDataDict[simpleID]:
						if sameTerm(d['eng'], ENG):
							CNS = d['cns']
							UMLSMapSNOMED_US[AUI] = ({'code': code, 'eng': ENG, 'cns': CNS})
		return UMLSMapSNOMED_US


class SNOMEDMapGenerator1(SNOMEDMapGenerator):
	def __init__(self):
		super(SNOMEDMapGenerator1, self).__init__()
		self.source = SNOMED_SNMI_SOURCE
		self.MAP_JSON = DATA_PATH + '/umlsMT/map/UMLSMapSNMI.json'
		self.mapDict = None


	@checkLoadSave('mapDict', 'MAP_JSON', JSON_FILE_FORMAT)
	def getAUIMapDict(self):
		"""
		Returns:
			dict: {AUI: {'code': code, 'eng': ENG, 'cns': CNS)}
		"""
		SNOMEDDataDict = readSNOMED_CNSCMIA_TXT(DATA_PATH+'/thesaurus/cn/SNOMED/CMIA/英汉对照国际医学规范术语全集-精选本.txt')
		UMLSDataList = readUMLS_ENG(DATA_PATH+'/umlsMT/umls/MRCONSO.RRF')
		mapDict = {}
		mapDict.update(self.getAUIMapDict1(SNOMEDDataDict, UMLSDataList))
		mapDict.update(self.getAUIMapDict2(SNOMEDDataDict, UMLSDataList))
		return mapDict


class SNOMEDMapGenerator2(SNOMEDMapGenerator):
	def __init__(self):
		super(SNOMEDMapGenerator2, self).__init__()
		self.source = SNOMED_BDWK_SOURCE
		self.MAP_JSON = DATA_PATH + '/umlsMT/map/UMLSMapSnomedBDWK.json'
		self.mapDict = None


	@checkLoadSave('mapDict', 'MAP_JSON', JSON_FILE_FORMAT)
	def getAUIMapDict(self):
		"""
		Returns:
			dict: {AUI: {'code': code, 'eng': ENG, 'cns': CNS)}
		"""
		SNOMEDDataDict = readSNOMED_CNSBDWK_XLSX(DATA_PATH+'/thesaurus/cn/SNOMED/BDWK/snomed对照表.xlsx')
		UMLSDataList = readUMLS_ENG(DATA_PATH+'/umlsMT/umls/MRCONSO.RRF')
		mapDict = {}
		mapDict.update(self.getAUIMapDict1(SNOMEDDataDict, UMLSDataList))
		mapDict.update(self.getAUIMapDict2(SNOMEDDataDict, UMLSDataList))
		return mapDict


if __name__ == '__main__':
	mapper = SNOMEDMapGenerator2()
	mapper.getAUIMapDict()

