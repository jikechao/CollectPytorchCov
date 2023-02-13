# import tvm
# from tvm import relay
# from tvm.contrib import graph_runtime

import torch
from torchvision import transforms
import torchvision.models as models

import os
import numpy as np
from PIL import Image

base_dir = '/share_container/data/'


def pic_process(x, shape):
    my_preprocess = transforms.Compose(
        [
            transforms.Resize(256),
            transforms.CenterCrop(shape),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )
    x_return = []
    for x_test in x:
        tmp = np.copy(x_test)
        img = Image.fromarray(tmp.astype('uint8')).convert('RGB')
        img = img.resize(shape, Image.ANTIALIAS)
        img = my_preprocess(img)
        x_return.append(np.array(img))
    return np.array(x_return)


# def getTestData(dataset_dir, input_layer_shape):
#     print("input_layer_shape",input_layer_shape)
#     data_path = os.path.join(dataset_dir, "imagenet-val-100.npz")
#     data = np.load(data_path)
#     x, y = data['x_test'], data['y_test']
#     x = x[:input_layer_shape[0]]
#     y = y[:input_layer_shape[0]]
#
#     input_shape = input_layer_shape[2:4]
#     x = pic_process(np.copy(x), input_shape)
#     return x, y


def getTestData(model_name):
    input_shape = ()
    if "mnist" in model_name:  # fashion-mnist
        input_shape = (1,28, 28, 1)
    elif "cifar100" in model_name:  # must judge cifar100 before cifar10 ;because "cifar10" in "cifar100"
        input_shape = (1,32,32,3)
    elif "cifar10" in model_name:
        input_shape = (1,32, 32, 3)
    elif "imagenet" in model_name:
        input_shape = (1,224, 224, 3)
    torch_img = torch.ones(input_shape)
    return torch_img


def run(model_name):
    model = torch.load(model_name)

    torch_img = getTestData(model_name)
    with torch.no_grad():
        frame_output = model(torch_img).numpy()
        print(np.argmax(frame_output))


if __name__ == '__main__':
    import sys
    model_name = sys.argv[1]
    # if model_name == 'mobilenet_v2':  # crash , find a bug
    #     assert False
    print('\033[1;32;43m model_name = ', model_name, '\033[0m')
    print(model_name)

    run(model_name)
    print('\033[1;34;45m---------------------------------------------------\033[0m')
    # assert False

