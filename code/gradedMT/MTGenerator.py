# encoding: UTF-8

"""
@author: hy
"""

import json
import random
from tqdm import tqdm

from analyzer.StandardAnalyzer import StandardAnalyzer
from config import DATA_PATH, PKL_FILE_FORMAT, JSON_FILE_FORMAT
from config import MeSH_SOURCE, BAIDU_SOURCE, GOOGLE_SOURCE, ICIBA_SOURCE, UMLS_CHI_SOURCE
from common import containCNS, getSaveFunc, timer, checkLoadSave, dictListAdd, splitPath
from gradedMT.tool import tokenEqualList, bagOfWordsEqualList, negENGCount
from gradedMT.mapGenerator.HPOMapGenerator import HPOMapGenerator
from gradedMT.mapGenerator.ICD10MapGenerator import ICD10MapGenerator
from gradedMT.mapGenerator.ICIBAMapGenerator import ICIBAMapGenerator
from gradedMT.mapGenerator.MeSHMapGenerator import MeSHMapGenerator
from gradedMT.mapGenerator.SNOMEDMapGenerator import SNOMEDMapGenerator1, SNOMEDMapGenerator2
from gradedMT.mapGenerator.UMLSCHIMapGenerator import UMLSCHIMapGenerator
from read.UMLS.ReadMrConso import readMRCONSO_RRF


class MTGenerator(object):
	def __init__(self):
		super(MTGenerator, self).__init__()
		self.MRCONSO_RRF = DATA_PATH+'/umlsMT/umls/MRCONSO.RRF'
		self.AUI_JSON = DATA_PATH+'/umlsMT/translate/AUI.json'
		self.UMLS_ENG_JSON = DATA_PATH+'/umlsMT/translate/termENG.json'
		self.UMLS_BAIDU_JSON = DATA_PATH+'/umlsMT/translate/termCNSBaidu_2017.json'
		self.UMLS_GOOGLE_JSON = DATA_PATH+'/umlsMT/translate/termCNSGoogle_2017_1.1.json'
		self.SAVE_MT_PKL = None
		self.DEMO_TERM_NUM = 100000
		self.SAVE_MT_DEMO_JSON = None

		self.AUI_MAP_CUI_JSON = DATA_PATH+'/umlsMT/umls/AUIMapCUI.json'
		self.auiMapCui = None

		self.MedicalThesaurus = None


	def genMT(self):
		raise NotImplementedError


	@checkLoadSave('auiMapCui', 'AUI_MAP_CUI_JSON', JSON_FILE_FORMAT)
	def getAUIMapCUI(self):
		"""
		Returns:
			dict: {AUI: CUI}
		"""
		UMLSDataList = readMRCONSO_RRF(self.MRCONSO_RRF)
		return {uTermDict['AUI']:uTermDict['CUI'] for uTermDict in UMLSDataList}


	def getAUIList(self):
		return list(self.getAUIMapCUI().keys())


	def getAUIMapUmlsTerm(self):
		UMLSDataList = readMRCONSO_RRF(self.MRCONSO_RRF)
		return {uTermDict['AUI']: uTermDict['STR'] for uTermDict in UMLSDataList}


	def saveDemo(self):
		medicalThesaurus = self.genMT()
		smallMT = {AUI:medicalThesaurus[AUI] for AUI in random.sample(list(medicalThesaurus), self.DEMO_TERM_NUM)}
		getSaveFunc(JSON_FILE_FORMAT)(smallMT, self.SAVE_MT_DEMO_JSON)


	def getMapDictForMT(self, auiLists, engList, cnsList):
		"""
		Args:
			auiLists (list): [[AUI1.1, AUI1.2, ...], ...]
			engList (list): [ENG1, ...]
			cnsList (list): [CNS1, ...]
		Returns:
			dict: {AUI: {'code': code, 'eng': ENG, 'cns': CNS)}}
		"""
		mapDict = {}
		for auiList, eng, cns in zip(auiLists, engList, cnsList):
			for aui in auiList:
				mapDict[aui] = {'code': aui, 'eng': eng, 'cns': cns}
		return mapDict


	def addSource(self, retDict, sourceName, mapDict):
		print('Adding Source: {}'.format(sourceName))
		for AUI, item in tqdm(mapDict.items()):
			if AUI in retDict:
				retDict[AUI]['source'][sourceName] = item['cns']
			else:
				retDict[AUI] = {'source': {sourceName: item['cns']}}


	def addUmlsTerm(self, retDict, AUIMapUmlsTerm):
		for AUI, item in retDict.items():
			item['eng'] = AUIMapUmlsTerm[AUI]


	def getManualTransAUIList(self, mtDict):
		machineSet = {GOOGLE_SOURCE, BAIDU_SOURCE}
		return [aui for aui, item in mtDict.items() if len(set(item['source'].keys()) - machineSet) > 0]


	def printManualCUICoverRate(self, mtDict):
		auiMapCUI = self.getAUIMapCUI()
		allCUINum = len(set([auiMapCUI[aui] for aui in mtDict]))
		manualCUINum = len(set([auiMapCUI[aui] for aui in self.getManualTransAUIList(mtDict)]))
		print('Manual CUI Cover Rate = {}/{} = {}%'.format(manualCUINum, allCUINum, 100.0*manualCUINum/allCUINum))


	def printManualAUICoverRate(self, mtDict):
		allAUINum = len(mtDict)
		manualAUINum = len(self.getManualTransAUIList(mtDict))
		print('Manual AUI Cover Rate = {}/{} = {}%'.format(manualAUINum, allAUINum, 100.0*manualAUINum/allAUINum))


class SimpleMTGenerator(MTGenerator):
	def __init__(self):
		super(SimpleMTGenerator, self).__init__()
		self.SAVE_MT_PKL = DATA_PATH+'/umlsMT/SimpleMT_2017_1.1.pkl'
		self.SAVE_MT_DEMO_JSON = DATA_PATH+'/umlsMT/{}_{}.json'.format(splitPath(self.SAVE_MT_PKL)[1], self.DEMO_TERM_NUM)


	@checkLoadSave('MedicalThesaurus', 'SAVE_MT_PKL', PKL_FILE_FORMAT)
	def genMT(self):
		"""
		Returns:
			dict: {
				AUI: {
				'eng': eng,
				'source': {source: cns}
				}
			}
		"""
		allMapDict = {}
		priorityMapperList = [
			UMLSCHIMapGenerator(), HPOMapGenerator(), SNOMEDMapGenerator1(), ICD10MapGenerator(),
			ICIBAMapGenerator(), SNOMEDMapGenerator2(), MeSHMapGenerator()
		]
		for mapper in priorityMapperList:
			mapDict = mapper.getAUIMapDict()
			allMapDict[mapper.source] = mapDict
			print('{}: {}'.format(mapper.source, len(mapDict)))

		auiLists = json.load(open(self.AUI_JSON))
		termList = json.load(open(self.UMLS_ENG_JSON))
		baiduCNSList = json.load(open(self.UMLS_BAIDU_JSON))
		googleCNSList = json.load(open(self.UMLS_GOOGLE_JSON))
		allMapDict[BAIDU_SOURCE] = self.getMapDictForMT(auiLists, termList, baiduCNSList)
		allMapDict[GOOGLE_SOURCE] = self.getMapDictForMT(auiLists, termList, googleCNSList)

		retDict = {}   #
		for source, mapDict in allMapDict.items():
			self.addSource(retDict, source, mapDict)
		auiMapUmlsTerm = self.getAUIMapUmlsTerm()
		self.addUmlsTerm(retDict, auiMapUmlsTerm)

		self.printManualCUICoverRate(retDict)   # 339854/3436328 = 9.890033780244494%
		self.printManualAUICoverRate(retDict)   # 939979/9486137 = 9.90897559248828%

		return retDict


# {
# 		AUI: {
# 			eng: xxx,
# 			prefer: xxx,
# 			preferSource: HPO,
# 			confidence: 1,
# 			source: {
# 				HPO: xxx,
# 				ICIBA: xxx,
# 				baidu: xxx,
# 				google: xxx
# 			}
# 		}
# 	}
# 	confidence:
# 		1: 官方人工翻译(HPO, SNMI, ICD10)
# 		2: ICIBA带标签的翻译
# 		3: tokenEqual(baidu, google) & existCNS
# 		4: bagOfWordsEqual(baidu, google) & existCNS
# 		5: 非官方人工翻译(MeSH)
# 		6: 其他
class GradedMT(MTGenerator):
	def __init__(self):
		super(GradedMT, self).__init__()
		self.SAVE_MT_PKL = DATA_PATH+'/umlsMT/GradedMT_2017_1.1.pkl'
		self.SAVE_MT_DEMO_JSON = DATA_PATH+'/umlsMT/{}_{}.json'.format(splitPath(self.SAVE_MT_PKL)[1], self.DEMO_TERM_NUM)


	@checkLoadSave('MedicalThesaurus', 'SAVE_MT_PKL', PKL_FILE_FORMAT)
	def genMT(self):
		allMapDict = {}
		prtMapperList = [
			UMLSCHIMapGenerator(), HPOMapGenerator(), SNOMEDMapGenerator1(), ICD10MapGenerator(),
			ICIBAMapGenerator(), SNOMEDMapGenerator2(), MeSHMapGenerator()
		]
		for mapper in prtMapperList:
			mapDict = mapper.getAUIMapDict()
			allMapDict[mapper.source] = mapDict
			print('{}: {}'.format(mapper.source, len(mapDict)))

		retDict = {}   #
		for source, mapDict in allMapDict.items():
			self.addSource(retDict, source, mapDict)
		auiMapUmlsTerm = self.getAUIMapUmlsTerm()
		self.addUmlsTerm(retDict, auiMapUmlsTerm)

		for AUI, item in retDict.items():
			for mapper in prtMapperList: # 采用了mapDict的翻译
				source = mapper.source
				if source in retDict[AUI]['source']:
					retDict[AUI]['preferSource'] = source
					retDict[AUI]['prefer'] = retDict[AUI]['source'][source]
					break
			if retDict[AUI]['preferSource'] == MeSH_SOURCE:
				retDict[AUI]['confidence'] = 4
			elif retDict[AUI]['preferSource'] == ICIBA_SOURCE:
				retDict[AUI]['confidence'] = 2
			else:
				retDict[AUI]['confidence'] = 1

		auiLists = json.load(open(self.AUI_JSON))
		termList = json.load(open(self.UMLS_ENG_JSON))
		baiduCNSList = json.load(open(self.UMLS_BAIDU_JSON))
		googleCNSList = json.load(open(self.UMLS_GOOGLE_JSON))
		self.addSource(retDict, BAIDU_SOURCE, self.getMapDictForMT(auiLists, termList, baiduCNSList))
		self.addSource(retDict, GOOGLE_SOURCE, self.getMapDictForMT(auiLists, termList, googleCNSList))

		analyzer = StandardAnalyzer()
		for AUI, item in tqdm(retDict.items()):
			if not (BAIDU_SOURCE in item['source'] and GOOGLE_SOURCE in item['source']):
				continue
			baiduTerm = item['source'][BAIDU_SOURCE]
			googleTerm = item['source'][GOOGLE_SOURCE]
			wordListB = analyzer.split(baiduTerm)
			wordListG = analyzer.split(googleTerm)
			if 'confidence' not in retDict[AUI]:
				retDict[AUI]['confidence'] = 6
			if retDict[AUI]['confidence'] > 2 and tokenEqualList(wordListB, wordListG) and containCNS(baiduTerm):
				retDict[AUI]['confidence'] = 3
				retDict[AUI]['preferSource'] = BAIDU_SOURCE
				retDict[AUI]['prefer'] = retDict[AUI]['source'][BAIDU_SOURCE]

			if retDict[AUI]['confidence'] > 4 and bagOfWordsEqualList(wordListB, wordListG) and containCNS(baiduTerm):
				retDict[AUI]['confidence'] = 5
				retDict[AUI]['preferSource'] = BAIDU_SOURCE
				retDict[AUI]['prefer'] = retDict[AUI]['source'][BAIDU_SOURCE]

			if retDict[AUI]['confidence'] == 6:
				if negENGCount(wordListB) >= negENGCount(wordListG):
					retDict[AUI]['preferSource'] = BAIDU_SOURCE
					retDict[AUI]['prefer'] = retDict[AUI]['source'][BAIDU_SOURCE]
				else:
					retDict[AUI]['preferSource'] = GOOGLE_SOURCE
					retDict[AUI]['prefer'] = retDict[AUI]['source'][GOOGLE_SOURCE]

		auiMapUmlsTerm = self.getAUIMapUmlsTerm()
		self.addUmlsTerm(retDict, auiMapUmlsTerm)
		self.statistic(retDict)

		return retDict


	def statistic(self, mtDict):
		print('making statistics...')
		countDict = {i:0 for i in range(1, 7)}
		for AUI in mtDict:
			countDict[mtDict[AUI]['confidence']] += 1
		for confidence in countDict:
			print('confidence %d: %d/%d, %f' % (confidence, countDict[confidence], len(mtDict), countDict[confidence] * 1.0 / len(mtDict)))
		self.printManualCUICoverRate(mtDict)
		self.printManualAUICoverRate(mtDict)



if __name__ == '__main__':
	mtGenerator = GradedMT()
	# mtGenerator = SimpleMTGenerator()

	mtGenerator.genMT()
	mtGenerator.saveDemo()


