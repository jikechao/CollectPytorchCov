import tensorflow.keras as keras
# import keras.backend as K
import numpy as np
from PIL import Image
import pandas as pd
# from sklearn.preprocessing import MinMaxScaler
import os
import tvm 
from tvm import relay 
import subprocess
import logging

# x, y = get_data_by_exp('lenet5-fashion-mnist')
# batchsize = 16
logging.basicConfig(filename='coverage.log', level=logging.INFO)
def Red(string):
    return '\033[1;31m' + string + '\033[0m'

def Blue(string):
    return '\033[1;34m' + string + '\033[0m'

import sys
# modelname = sys.argv[1]
# order = sys.argv[2]

modelname = 'lenet5-mnist'

logging.info(f'modelname = {modelname}')

# keras_path = f'/share_container/share_host_hy2/lemon_outputs/{modelname}/mut_model/'
# keras_path = f'/share_container/share_host_hy2/MHYmutation_2021_5_13/{order}'
keras_path = f'/share_container/share_host_hy2/LEMON-lenet-mnist-2021_5_13/{modelname}/mut_model/'

keras_models = os.listdir(keras_path)
# shape_dict = {"input_1": data.shape}

srcpaths = ['/workplace/software/tvm/tvm8/build/CMakeFiles/tvm_objs.dir/src/',
            '/workplace/software/tvm/tvm8/build/CMakeFiles/tvm_runtime_objs.dir/src/runtime/']

def init():
    for gcdapath in srcpaths:
        try:
            cmd = 'find {} -name *.gcda -type f | xargs rm -rf'.format(gcdapath)
            # logging.info(f'cmd = {cmd}')
            subprocess.check_output(cmd, shell=True, )
        except subprocess.CalledProcessError as e:
            logging.warning(e)

# def init():

def deal(srcpath, sl):

    if sl.endswith('.gcno'):
        elename = sl.split('.gcno')[0]
        string = 'llvm-cov gcov -p ' + os.path.join(srcpath, elename)
        subprocess.run(string, shell=True, stdout=subprocess.PIPE )
    
    # elif sl.endswith('.o') or sl.endswith('.gcda') or sl.endswith('.gcov'):
    #     pass

    elif os.path.isdir(os.path.join(srcpath, sl)):
        path = os.path.join(srcpath, sl)
        elelist = os.listdir(path)

        for ele in elelist:

            # folder += sl + '/'
            deal(path, ele)

            # if ele.endswith('.gcno'):
            #     elename = ele.split('.gcno')[0]
            #     run2('llvm-cov gcov -f -b -m ' + os.path.join(path, elename))

def cov():
    res = ''

    for srcpath in srcpaths:
        srclist = os.listdir(srcpath)
        for sl in srclist:
            deal(srcpath, sl)

    return res

gcovpath = '/share_container/share_host_hy2/gcovtvmc_LEMON-lenet-mnist_2021_5_14/'

# record = open('recordcov.txt', 'w')

init()

# deletecmd = 'python deletegcda.py'
# subprocess.run(deletecmd, shell=True, stdout=subprocess.PIPE )


for keras_model in keras_models:
    
    # recordpath = gcovpath + f'{modelname}/{order}/' + keras_model
    recordpath = gcovpath + f'{modelname}/' + keras_model

    if not os.path.exists(recordpath):
        subprocess.run('mkdir -p {}'.format(recordpath), shell=True, stdout=subprocess.PIPE )

    model_path = os.path.join(keras_path, keras_model)
    logging.info(f'model_path: {model_path}')
    
    extra = ''

    if 'lenet5-fashion-mnist' in keras_model or 'alexnet-cifar10' in keras_model or 'mobilenet.1.00.224-imagenet' in keras_model\
        or 'vgg16-imagenet' in keras_model or 'densenet121-imagenet' in keras_model or 'lenet5-mnist' in keras_model or \
            'vgg19-imagenet' in keras_model or 'inception.v3-imagenet' in keras_model or 'resnet50-imagenet' in keras_model or \
                'xception-imagenet' in keras_model:
        extra = '--desired-layout \"NCHW\"'

    subprocess.check_call(f'python -m tvm.driver.tvmc tune --trials 1 --target \"llvm\" --output ./tvmc/{modelname}/{keras_model}.json {extra} {model_path}'\
    , shell=True, stdout=subprocess.PIPE)

    subprocess.check_call(f'python -m tvm.driver.tvmc compile --target \"llvm\" --tuning-records ./tvmc/{modelname}/{keras_model}.json  {extra} --output ./tvmc/{modelname}lenet-tvm-autotuned.tar {model_path}'\
    , shell=True, stdout=subprocess.PIPE)

    # subprocess.run(f'python script.py {model_path}', shell=True, stdout=subprocess.PIPE )

    res = cov()
    subprocess.run('mv *.gcov {}'.format(recordpath), shell=True, stdout=subprocess.PIPE )
    init()

    # subprocess.run(deletecmd, shell=True, stdout=subprocess.PIPE )

# init()

# record.close()


# keras_path = '/share_container/share_host_hy2/lemon_outputs/lenet5-fashion-mnist/mut_model/lenet5-fashion-mnist_origin0-ARem0.h5'

# model = keras.models.load_model(keras_path)
# mod, params = relay.frontend.from_keras(model)

logging.info('Finish.')
