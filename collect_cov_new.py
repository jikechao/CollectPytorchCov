'''
use mutated model generate by LEMON,
to collect the coverage of PyTorch.
by Coverage.py
'''
import os
import subprocess
# from Inference import inference
import collect_cov_c
import multiprocessing as mp
# import multiprocessing


def exccmd(com):
    print(f"run commend: {com}")
    res = []
    p = os.popen(com, 'r')
    lines = p.readlines()  # return a list, but each item end with '\n'
    for line in lines:
        res.append(line.strip())
    return res


def single_work(model_path):
    if not os.path.exists(model_path):
        print(f"file path {model_path} is not exist!")
    cmd_str = f"coverage run -p {script} {model_path}"
    exccmd(cmd_str)


if __name__ == '__main__':
    # clear C coverage info
    collect_cov_c.init()

    script = 'Inference/inference.py'
    dir_path = '/share_container/data/audee_outputs_pt/'

    all_models = ['vgg16-imagenet',  'lenet5-mnist', 'lenet5-fashion-mnist', 'alexnet-cifar10', 'resnet50-imagenet', 'mobilenet.1.00.224-imagenet',]  # 'lstm2-price', 'lstm0-sinewave',


    exccmd(f'rm  .coverage')
    exccmd(f'rm  .coverage.*')  # remove history .coverage
    exccmd(f"rm ./*.gcov")

    # pool = multiprocessing.Pool(processes=40)
    for count in range(0, 101):
        print(count)
        # res_path = './lemon_cov_mx_08_22/' + str(count)
        res_path = './audee_cov_pt_6models/' + str(count)
        res_path_python = os.path.join(res_path, 'python')
        res_path_c = os.path.join(res_path, 'c')
        if not os.path.exists(res_path_python):
            os.makedirs(res_path_python)
        if not os.path.exists(res_path_c):
            os.makedirs(res_path_c)

        # collect coverage of the total 8 models each time
        p_list = []
        for sub_dir in all_models:
            sub_path = os.path.join(dir_path, sub_dir)
            # sub_path = os.path.join(sub_path, 'mut_model')
            # CRADLE coverage
            if count == 0:
                model_path = os.path.join("/share_container/data/pytorch_model_DLLTesting/", f"{sub_dir}_origin.pt")
            else:
                i = (count-1) // 10
                j = (count-1) % 10
                model_path = os.path.join(sub_path, f"{sub_dir}_origin.h5_{i}_{j}.pt")
                if not os.path.exists(model_path):
                    print("model not existing:", model_path)
                    continue
                else:
                    print("run:", model_path)
            single_work(model_path)
            # pool.apply(single_work, (model_path,))
            # pool.close()
            # pool.join()
            p1 = mp.Process(target=single_work, args=(model_path,))
            p_list.append(p1)
            p1.start()
            #
            for p in p_list:
                p.join()
            # if count == 3:
            #     assert False
            # continue

            print(f"finish count {count}, next count...")
            if count == 0 or count == 99:
                # collect python coverage here
                exccmd(f'coverage combine')

                exccmd(f'cp .coverage {res_path_python}/.coverage.{count}')
                exccmd(f'mv .coverage .coverage.2')

                # collect c/c++ coverage
                collect_cov_c.cov()
                # os.chdir("/workplace/software/pytorch3")
                subprocess.run(f'cp *.gcov {res_path_c}', shell=True, stdout=subprocess.PIPE)
                # os.chdir("/share_container/pycharmProjects/DLLTesting/pytorch_cov")
