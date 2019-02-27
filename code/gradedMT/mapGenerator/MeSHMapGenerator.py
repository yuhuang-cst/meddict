# encoding: UTF-8

"""
@author: hy
"""

from gradedMT.mapGenerator.MapGenerator import MapGenerator
from common import checkLoadSave
from config import DATA_PATH, JSON_FILE_FORMAT, MeSH_SOURCE
from read.MeSH.CNSCHISC import readMESH_CNSCHISC
from read.UMLS.ReadMrConso import readUMLS_ENG


class MeSHMapGenerator(MapGenerator):
	def __init__(self):
		super(MeSHMapGenerator, self).__init__()
		self.source = MeSH_SOURCE
		self.MAP_JSON = DATA_PATH + '/umlsMT/map/UMLSMapMeSH_CHISC.json'
		self.mapDict = None


	@checkLoadSave('mapDict', 'MAP_JSON', JSON_FILE_FORMAT)
	def getAUIMapDict(self):
		"""
		Returns:
			dict: {AUI: {'code': code, 'eng': ENG, 'cns': CNS)}
		"""
		MeSHDataDict = readMESH_CNSCHISC(
			DATA_PATH+'/thesaurus/cn/MeSH/chisc/Mesh-医学主题词表.txt',
			DATA_PATH+'/thesaurus/en/NLM/ascii/d2017.bin'
		)
		UMLSDataList = readUMLS_ENG(DATA_PATH+'/umlsMT/umls/MRCONSO.RRF')
		mapDict = {}
		for uTermDict in UMLSDataList:
			if uTermDict['SAB']== 'MSH' and uTermDict['CODE'] in MeSHDataDict:
				AUI = uTermDict['AUI']
				code = uTermDict['CODE']
				ENG = uTermDict['STR']
				CNS = MeSHDataDict[code]
				assert AUI not in mapDict		#检查是否有多个AUI映射到同一个hpo
				mapDict[AUI] = ({'code': code, 'eng': ENG, 'cns': CNS})
		return mapDict

