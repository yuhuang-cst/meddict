# encoding: UTF-8

"""
@author: hy
"""

import os
import json
from tqdm import tqdm
import shutil
import time

from config import JSON_FILE_FORMAT, GOOGLE_API, BAIDU_API, DATA_PATH, TEMP_PATH
from common import getSaveFunc, getFileList, splitPath, Config, sameTerm

class TranslateConfig(Config):
	def __init__(self):
		super(TranslateConfig, self).__init__()
		self.SLICE_LENGTH = 1000
		self.SLICE_TIME_SLEEP = 1
		self.PALL_VISIT = 100
		self.JS_PATH = '~/translate/translateAPI.js'


class BaiduConfig(TranslateConfig):
	def __init__(self):
		"""Failed Translated: 65/10024 = 0.6484437350359138%
		"""
		super(BaiduConfig, self).__init__()
		self.SLICE_LENGTH = 100


class GoogleCNConfig(TranslateConfig):
	def __init__(self):
		super(GoogleCNConfig, self).__init__()
		self.SLICE_LENGTH = 100


def divideListJson(inputJson, sliceLen, folder):
	"""切分list并以json文件的形式存储于folder文件夹
	Args:
		list (list): 待切分列表
		sliceNum (int): 切分后每个子列表的长度
		folder (str): 文件夹路径
	Returns:
		list: [jsonPath1, jsonPath2, ...]
	"""
	ll = json.load(open(inputJson))
	saveJsonFunc = getSaveFunc(JSON_FILE_FORMAT)
	count = 0
	savePathList = []
	for i in range(0, len(ll), sliceLen):
		count += 1
		savepath = folder+os.sep+str(count)+'.json'
		saveJsonFunc(ll[i: i+sliceLen], savepath)
		savePathList.append(savepath)
	return savePathList


def mergeListJson(saveJson, folder):
	fileList = getFileList(folder, lambda fpath: splitPath(fpath)[2] == '.json')
	orderList = [int(splitPath(fpath)[1]) for fpath in fileList]
	orderList, fileList = zip(*sorted(zip(orderList, fileList)))

	retList = []
	for fpath in fileList:
		retList.extend(json.load(open(fpath)))
	getSaveFunc(JSON_FILE_FORMAT)(retList, saveJson)


def _translate(API, fileList, outFolder, c=TranslateConfig()):
	for injson in tqdm(fileList):
		outjson = os.path.join(outFolder, os.path.split(injson)[1])
		if os.path.exists(outjson):
			continue
		os.system('node {} {} {} {} {}'.format(c.JS_PATH, API, injson, outjson, c.PALL_VISIT))
		time.sleep(c.SLICE_TIME_SLEEP)


def translate(API, inputJson, outputJson, inputDividedFolder=None, outputDividedFolder=None, trace=True, c=TranslateConfig()):
	if inputDividedFolder is None:
		inputDividedFolder = TEMP_PATH+'/{}-{}'.format(splitPath(inputJson)[1], API)
	if outputDividedFolder is None:
		outputDividedFolder = TEMP_PATH+'/{}-{}'.format(splitPath(outputJson)[1], API)

	# divide
	if not os.path.exists(inputDividedFolder):
		os.makedirs(inputDividedFolder, exist_ok=True)
		divideListJson(inputJson, c.SLICE_LENGTH, inputDividedFolder)

	# translate
	os.makedirs(outputDividedFolder, exist_ok=True)
	fileList = getFileList(inputDividedFolder, lambda fpath: splitPath(fpath)[2] == '.json')
	_translate(API, fileList, outputDividedFolder, c)

	# merge
	mergeListJson(outputJson, outputDividedFolder)

	# check
	check(inputJson, outputJson)

	# delete
	if not trace:
		shutil.rmtree(inputDividedFolder)
		shutil.rmtree(outputDividedFolder)


def update(API, inputJson, outputJson, needUpdateFunc, c=TranslateConfig()):
	inputList = json.load(open(inputJson))
	outputList = json.load(open(outputJson))

	assert len(inputList) == len(outputList)
	posEngList = [] # [(rank, eng), ...]
	for i in range(len(inputList)):
		inTerm, outTerm = inputList[i], outputList[i]
		if needUpdateFunc(inTerm, outTerm):
			posEngList.append((i, inTerm))

	ufname = splitPath(outputJson)[1]
	updateInJson = TEMP_PATH + '/{}-update-input.json'.format(ufname)
	updateOutJson = TEMP_PATH + '/{}-update-output.json'.format(ufname)
	getSaveFunc(JSON_FILE_FORMAT)([engTerm for i, engTerm in posEngList], updateInJson)
	translate(API, updateInJson, updateOutJson, trace=False, c=c)

	updateOutList = json.load(open(updateOutJson))
	for ui, uTerm in enumerate(updateOutList):
		print('{} -> {}'.format(outputList[posEngList[ui][0]], uTerm))    # debug
		outputList[posEngList[ui][0]] = uTerm
	getSaveFunc(JSON_FILE_FORMAT)(outputList, outputJson)


def check(injson, outjson):
	inList = json.load(open(injson))
	outList = json.load(open(outjson))
	assert len(inList) == len(outList)


def transFailed(inTerm, outTerm):
	return sameTerm(inTerm, outTerm)


def statistic(injson, outjson):
	inList = json.load(open(injson))
	outList = json.load(open(outjson))
	failNum = 0
	for inTerm, outTerm in zip(inList, outList):
		if transFailed(inTerm, outTerm):
			failNum += 1
	total = len(inList); succNum = total-failNum
	print('Successfully Translated: {}/{} = {}%'.format(succNum, total, 100.0*succNum/total))
	print('Failed Translated: {}/{} = {}%'.format(failNum, total, 100.0*failNum/total))


if __name__ == '__main__':
	def google():
		print('Google Translate...')
		API = GOOGLE_API
		tlconfig = GoogleCNConfig()
		inputJson = DATA_PATH+'/umlsMT/translate/termENG.json'
		outputJson = DATA_PATH+'/umlsMT/translate/termCNSGoogle.json'
		# translate(API, inputJson, outputJson, c=tlconfig, trace=False)
		# statistic(inputJson, outputJson)
		update(API, inputJson, outputJson, lambda inTerm, outTerm: transFailed(inTerm, outTerm), c=tlconfig)
		statistic(inputJson, outputJson)

	def baidu():
		print('Baidu Translate...')
		API = BAIDU_API
		tlconfig = BaiduConfig()
		inputJson = DATA_PATH+'/umlsMT/translate/termENG.json'
		outputJson = DATA_PATH+'/umlsMT/translate/termCNSBaidu.json'
		# translate(API, inputJson, outputJson, c=tlconfig, trace=False)
		# statistic(inputJson, outputJson)
		update(API, inputJson, outputJson, lambda inTerm, outTerm: transFailed(inTerm, outTerm), c=tlconfig)
		statistic(inputJson, outputJson)

	def googleUpdate():
		print('Google Update...')
		API = GOOGLE_API
		tlconfig = GoogleCNConfig()
		inputJson = DATA_PATH+'/umlsMT/translate/termENG.json'
		outputJson = DATA_PATH+'/umlsMT/translate/termCNSGoogle_2017_1.1.json'

		# update(API, inputJson, outputJson, lambda inTerm, outTerm: ';' in inTerm, c=tlconfig)
		# statistic(inputJson, outputJson)

		update(API, inputJson, outputJson, lambda inTerm, outTerm: ';' in inTerm and transFailed(inTerm, outTerm), c=tlconfig)
		statistic(inputJson, outputJson)

	pass
	# google()
	baidu()
	# googleUpdate()








