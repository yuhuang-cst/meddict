# encoding: UTF-8

"""
@author: hy
"""

from gradedMT.mapGenerator.MapGenerator import MapGenerator
from common import checkLoadSave
from config import DATA_PATH, JSON_FILE_FORMAT, HPO_SOURCE
from read.HPO.readCHPO import readCHPO
from read.UMLS.ReadMrConso import readUMLS_ENG


class HPOMapGenerator(MapGenerator):
	def __init__(self):
		super(HPOMapGenerator, self).__init__()
		self.source = HPO_SOURCE
		self.MAP_JSON = DATA_PATH + '/umlsMT/map/UMLSMapHPO.json'
		self.mapDict = None


	@checkLoadSave('mapDict', 'MAP_JSON', JSON_FILE_FORMAT)
	def getAUIMapDict(self):
		"""
		Returns:
			dict: {AUI: {'code': code, 'eng': ENG, 'cns': CNS)}
		"""
		HPODataDict = readCHPO(DATA_PATH+'/thesaurus/cn/HPO/chpo.2016-10.xls')
		UMLSDataList = readUMLS_ENG(DATA_PATH+'/umlsMT/umls/MRCONSO.RRF')
		mapDict = {}
		for uTermDict in UMLSDataList:
			if uTermDict['SAB']== 'HPO' and uTermDict['CODE'] in HPODataDict:
				AUI = uTermDict['AUI']
				code = uTermDict['CODE']
				ENG = uTermDict['STR']
				CNS = HPODataDict[code]['cns']
				assert AUI not in mapDict		#检查是否有多个AUI映射到同一个hpo
				mapDict[AUI] = ({'code': code, 'eng': ENG, 'cns': CNS})
		return mapDict
