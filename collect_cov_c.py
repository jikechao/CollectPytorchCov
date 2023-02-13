import torch
import numpy as np
# from PIL import Image
# import pandas as pd
import os
import subprocess
import logging

def exccmd(com):
    # print(f"run commend: {com}")
    r = []
    p = os.popen(com, 'r')
    lines = p.readlines()  # return a list, but each item end with '\n'
    for line in lines:
        r.append(line.strip())
    return r


logging.basicConfig(filename='coverage.log', level=logging.INFO)
def Red(string):
    return '\033[1;31m' + string + '\033[0m'

def Blue(string):
    return '\033[1;34m' + string + '\033[0m'


base_dir = '/workplace/software/pytorch3/'
srcpaths = [
    '/workplace/software/pytorch3/build/c10/CMakeFiles/c10.dir/',
    '/workplace/software/pytorch3/build/caffe2/CMakeFiles/torch_cuda.dir/__/aten/src',
    '/workplace/software/pytorch3/build/caffe2/CMakeFiles/torch_cuda.dir/__/torch/csrc',
    '/workplace/software/pytorch3/build/caffe2/CMakeFiles/torch_cpu.dir',
    '/workplace/software/pytorch3/build/caffe2/CMakeFiles/torch_cuda.dir',
    '/workplace/software/pytorch3/build/caffe2/torch/CMakeFiles/torch_python.dir',

]


def init():
    for gcdapath in srcpaths:
        cmd = 'find {} -name *.gcda -type f | xargs rm -rf'.format(gcdapath)
        print(cmd)
        status = os.system(cmd)
        if status:
            raise Exception('Fail in deleting gcda files')

        #     subprocess.check_output(cmd, shell=True, )
        # except subprocess.CalledProcessError as e:
        #     logging.warning(e)


def deal(srcpath, sl):
    if sl.endswith('.gcno'):
        elename = sl[:-5]
        string = 'llvm-cov gcov -p -b -f ' + os.path.join(srcpath, elename+".o")  # -p : get full path/
        # string = 'gcov -p ' + os.path.join(srcpath, elename)
        # subprocess.run(string, shell=True, stdout=subprocess.PIPE)
        exccmd(string)

    elif os.path.isdir(os.path.join(srcpath, sl)):
        path = os.path.join(srcpath, sl)
        elelist = os.listdir(path)

        for ele in elelist:
            deal(path, ele)


def cov():
    res = ''
    for srcpath in srcpaths:
        srclist = os.listdir(srcpath)
        for sl in srclist:
            deal(srcpath, sl)
    return res


'''
run this script after : conda activate torch_3
# coverage run Inference/inference2.py /share_container/data/audee_outputs_pt/mobilenet.1.00.224-imagenet/mobilenet.1.00.224-imagenet_origin.h5_0_0.pt 
'''


if __name__ == '__main__':
    init()
    script = 'Inference/inference.py'
    gcovpath = '/share_container/pycharmProjects/DLLTesting/pytorch_cov/gcov_06-10'
    model_dir = "/share_container/data/audee_outputs_pt"
    model_pro = os.listdir(model_dir)
    for pro in model_pro:
        pro_path = os.path.join(model_dir, pro)
        recordpath = gcovpath + f'/{pro_path}/'
        print(recordpath)
        if not os.path.exists(recordpath):
            os.makedirs(recordpath)
        for model_name in os.listdir(pro_path):
            model_path = os.path.join(pro_path, model_name)
            # subprocess.run(f'python Inference/inference.py {model_name}', shell=True, stdout=subprocess.PIPE)
            exccmd(f'coverage run Inference/inference.py {model_path}')

            print("begin collect coverage:")
            os.chdir("/workplace/software/pytorch3/build/")
            print(exccmd('pwd'))
            res = cov()

            print(exccmd('pwd'))
            # subprocess.run('mv *.gcov {}'.format(recordpath), shell=True, stdout=subprocess.PIPE)
            exccmd('mv *.gcov {}'.format(recordpath))
            os.chdir("/share_container/pycharmProjects/DLLTesting/pytorch_cov")
            init()
            break

    logging.info('Finish ALL.')
