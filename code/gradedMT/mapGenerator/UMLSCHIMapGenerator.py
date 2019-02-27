# encoding: UTF-8

"""
@author: hy
"""

from gradedMT.mapGenerator.MapGenerator import MapGenerator
from common import checkLoadSave
from config import DATA_PATH, JSON_FILE_FORMAT, UMLS_CHI_SOURCE
from read.UMLS.ReadMrConso import readMRCONSO_RRF


class UMLSCHIMapGenerator(MapGenerator):
	def __init__(self):
		super(UMLSCHIMapGenerator, self).__init__()
		self.source = UMLS_CHI_SOURCE
		self.MAP_JSON = DATA_PATH + '/umlsMT/map/UMLSMapUMLSCHI.json'
		self.mapDict = None


	@checkLoadSave('mapDict', 'MAP_JSON', JSON_FILE_FORMAT)
	def getAUIMapDict(self):
		"""实际上'eng'一栏亦为中文
		Returns:
			dict: {AUI: {'code': code, 'eng': ENG, 'cns': CNS)}
		"""
		UMLSDataList = readMRCONSO_RRF(DATA_PATH+'/umlsMT/umls/MRCONSO.RRF')
		mapDict = {}
		for uTermDict in UMLSDataList:
			if uTermDict['LAT'] == 'CHI':
				AUI = uTermDict['AUI']
				code = uTermDict['CODE']
				ENG = uTermDict['STR']
				CNS = uTermDict['STR']
				assert AUI not in mapDict		# 检查是否有多个AUI映射到同一个hpo
				mapDict[AUI] = ({'code': code, 'eng': ENG, 'cns': CNS})
		return mapDict


if __name__ == '__main__':
	mapper = UMLSCHIMapGenerator()
	mapper.getAUIMapDict()





