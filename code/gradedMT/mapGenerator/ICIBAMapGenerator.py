# encoding: UTF-8

"""
@author: hy
"""

import json
import re

from gradedMT.mapGenerator.MapGenerator import MapGenerator
from common import checkLoadSave
from config import DATA_PATH, JSON_FILE_FORMAT, ICIBA_SOURCE
from read.UMLS.ReadMrConso import readUMLS_ENG


class ICIBAMapGenerator(MapGenerator):
	def __init__(self):
		super(ICIBAMapGenerator, self).__init__()
		self.source = ICIBA_SOURCE
		self.MAP_JSON = DATA_PATH + '/umlsMT/map/UMLSMapICIBA.json'
		self.mapDict = None

		#取所有标签
		self.allLableP = re.compile('^(\[.*?\])(.+)$')

		#取出现次数不小于30且经人工验证较可靠的标签
		self.qualifiedP = re.compile('^(\[医\]|\[化\]|\[植物\]|\[植\]|\[动物\]|\[动\]|\[鸟类\]|\[解剖\]|\[中医\]|\[昆\]|\[药\]|\[化学\])(.+)$')
		self.annotationP = re.compile('[:：].+$')
		self.uselessP = re.compile('((\[.+?\])|(【.+?】)|(\(.+?\))|（.+?）|(<.+?>)|(〔.+?〕))')


	@checkLoadSave('mapDict', 'MAP_JSON', JSON_FILE_FORMAT)
	def getAUIMapDict(self):
		"""
		Returns:
			dict: {AUI: {'code': code, 'eng': ENG, 'cns': CNS)}
		"""
		termCNSICIBA = json.load(open(DATA_PATH+'/umlsMT/translate/termCNSICIBA.json'))
		AUI = json.load(open(DATA_PATH+'/umlsMT/translate/AUI.json'))
		UMLSDataList = readUMLS_ENG(DATA_PATH+'/umlsMT/umls/MRCONSO.RRF')
		getContentFunc = self.getUsefulContent   # getFullContent

		UMLSDataDict = {termDict['AUI']:termDict for termDict in UMLSDataList}
		mapDict = {}
		for i in range(len(termCNSICIBA)):
			CNS = getContentFunc(termCNSICIBA[i])
			if CNS:
				for aui in AUI[i]:
					code = UMLSDataDict[aui]['CODE']
					ENG = UMLSDataDict[aui]['STR']
					mapDict[aui] = {'code': code, 'eng': ENG, 'cns': CNS}
		return mapDict


	def getFullContent(self, str):
		m = self.allLableP.match(str)
		return m.group().strip() if m else None


	def getUsefulContent(self, str):
		def cutPostfix(s, target):
			pos = s.find(target)
			return s[:pos] if pos != -1 else s

		m = self.qualifiedP.match(str)
		if not m:
			return None
		content = m.group(2)
		content = cutPostfix(content, '：')
		content = cutPostfix(content, ':')
		content, number = self.uselessP.subn('', content)
		return content.strip()


	def countLables(self, termCNSICIBA):
		print('filtering...')
		lableDict = {}
		for str in termCNSICIBA:
			m = self.allLableP.match(str)
			if m:
				lableDict[m.group(1)] = lableDict[m.group(1)] + 1 if m.group(1) in lableDict else 1
				print(m.group())

		print('###############################')
		for lable, count in sorted(lableDict.items(), key=lambda item: item[1]):
			print(lable, ':', count)
		print('lable number: %d; lable occur times: %d' % (len(lableDict), sum(lableDict.values())))


def testPattern():
	testList = [
		'[医]组织蛋白酶E',
		'[医]3-异丁基-1-甲基黄嘌呤',
		'[医]a-萘胺',
		'[医]17-酮甾类，17-酮类固醇',
		'[医]小鼠c型肿瘤病毒，鼠白血病病毒',
		'[医]口腔康复，口腔整（修）复（康复），口腔修复',
		'[医]拉他头孢，双钠羟羧氧酰氨菌素，头孢羟羧氧，注射用噻吗氧，拉塔莫塞，拉氧头孢，氧杂头霉素二钠，羟羧氧酰胺菌素，噻吗氧酰胺菌素，噻吗灵，噻马灵',
		'[医]胎盘催乳激素，胎盘催乳素，胎盘催乳物',
		'[医]切开活组织[采取]检查，生体活组织检查',

		'[医][=dipalmitoyl phosphatidylcholine]二棕榈酰磷脂酰胆碱',
		'[医][=gamma hydroxybutyrate]γ-羟基丁酸盐',
		'[医][=dihydroxy-phenyl acetic acid]二羟苯乙酸',
		'[医][=5-hydroxytryptophan]5-羟色氨酸',

		'[医]〔EC 3。4。22。16〕组织蛋白酶H:半胱氨酸肽链内切酶，还能促使肽链N端的氨酸脱除，而使终端解脱，大多数哺乳类动物组织中皆有此酶',
		'[医]2，4，5-tricholorophenoxyacetic acid2，4，5-三氯苯氧乙酸：一种毒性氯苯氧基除莠剂，可以其生长调节激素作用，使阔叶植物因刺激过度而死亡',
		'[医]盐酸噻氯匹定：血小板抑制剂，C14H14ClNS·HCl',
		'[医]小螺菌，鼠咬热螺旋体：大鼠和小鼠鼻咽部正常寄生微生物的一种，是鼠咬热的病因',
		'[医]Sutton 病：〔Richard Lightburn Sutton,美国皮肤病学家，1878～1952〕晕轮痣(halonevus)',
		'[医]眼虫属：眼虫目(Euglenoidina)眼虫亚目(Euglenina)中的绿色植物样具鞭毛的原生动物，停滞的死水中常能大量发现，一般皆有具螺旋形或纵行条纹的表膜',
		'[医]〔EC 4。3。1。3〕组氨酸裂氨酶：一种裂解酶，催化L-组氨酸=尿刊酸+NH3。此反应是组氨酸分解代谢的第一步。该酶的遗传缺陷由常染色体隐性方式传递，引起组氨酸血症(histidinemia)',

		'[医]羟色氨酸（抗抑郁药，抗癫痫药）',
		'[医]屈昔多巴（抗震颤麻痹药）',
		'[医]替苯丙胺（中枢兴奋药）',
		'[医]β-丙氨酸，β-氨基丙酸，3-氨基丙酸[氨基酸类药]',
		'[医]6-氨基己酸，氨己酸，氨基己酸，ε-氨基己酸[促凝血药]',
		'[医]巯嘌呤，6-巯基嘌呤[抗代谢抗肿瘤药]',
		'[医]植物固醇[植物]',
		'[医]氨吡啶<钾通道阻滞药>',
		'[医]二棕榈酰磷脂酰胆碱<肺表面活性剂>',
		'[医]6-氨基己酸<止血药>',

		'[医]Latamoxef',
		'[医][=latamoxef]羟酸氧酰胺菌素',

		'[医] 心[动]电[流]图',

		'[化] 对氨基苯酸，对氨基苯甲酸',
		'[化] 1-萘胺',

		'[地名] [美国] 康塔克特',
		'[地名] [泰国] 沙县',
		'[地名] [南亚美利加洲] 英属圭亚那（圭亚那的旧称）',

		'[植物]海滨刺芹',
		'[植物]香根鸢尾',
		'[植物]香杨梅(myrica gale)[亦作 bog myrtle,moor myrtle]',
		'[植物]缬草(Valeriana offiinalis)',

		'[动物]摺鳃蜥;澳洲热带蜥蜴(chlamydosaurus kingi)',

		'[鱼类]美绒杜父鱼（Hemitripterus americanus）',
		'[鱼类]',
		'[加]醋酸泼尼松龙泼尼松龙滴眼液',
	]
	mapper = ICIBAMapGenerator()
	for str in testList:
		content = mapper.getUsefulContent(str)
		print(content)


if __name__ == '__main__':
	pass
	mapper = ICIBAMapGenerator()
	mapper.getAUIMapDict()
	# testPattern()
	# mapper.countLables(json.load(open(DATA_PATH+'/umlsMT/translate/termCNSICIBA.json')))