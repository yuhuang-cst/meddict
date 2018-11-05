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