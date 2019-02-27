# encoding: UTF-8

"""
@author: hy
"""

# export PYTHONPATH=`pwd`:$PYTHONPATH
# export PYTHONPATH=/home/yhuang/meddict/code:$PYTHONPATH
# export PYTHONPATH=/Users/apple/Documents/coding/research/meddict/code:$PYTHONPATH

import os

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
CODE_PATH = PROJECT_PATH + '/code'
DATA_PATH = PROJECT_PATH + '/data'
RESULT_PATH = PROJECT_PATH + '/result'
LOG_PATH = PROJECT_PATH + '/log'
TEMP_PATH = PROJECT_PATH + '/temp'


JSON_FILE_FORMAT = 'JSON'
PKL_FILE_FORMAT = 'PKL'
NPY_FILE_FORMAT = 'NPY'
NPZ_FILE_FORMAT = 'NPZ'
SPARSE_NPZ_FILE_FORMAT = 'SPARSE_NPZ'

BAIDU_API = 'BaiDu'
GOOGLE_API = 'GoogleCN'
ICIBA_API = 'iCIBA'
YOUDAO_API = 'YouDao'
BING_API = 'Bing'


HPO_SOURCE = 'HPO'
ICD10_SOURCE = 'ICD10'
MeSH_SOURCE = 'MeSH'
SNOMED_SNMI_SOURCE = 'SNMI'
SNOMED_BDWK_SOURCE = 'SNOMED_BDWK'
UMLS_CHI_SOURCE = 'UMLS_CHI'
ICIBA_SOURCE = 'ICIBA'
BAIDU_SOURCE = 'Baidu'
GOOGLE_SOURCE = 'Google'

