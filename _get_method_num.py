import os
import json
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')


method_line = dict()
all_cov_lines_dict = dict()


def get_method_line(file):
    line_num = 0
    with open(file, 'r+', encoding="utf-8") as f:
        all_lines = f.readlines()
        for line in all_lines:
            line_num += 1
            line = line.strip()
            if 'def ' == line[:4]:
                if file not in method_line.keys():
                    method_line[file] = []
                method_line[file].append(line_num)
            continue
    return


def get_all_method_line(base_dir):
    for dir_path, dir_name, files in os.walk(base_dir):
        for file in files:
            if not file.endswith('.py'):
                continue
            file_path = os.path.join(dir_path, file)
            # print(file_path)
            get_method_line(file_path)
    return method_line


def get_all_cov_lines(json_path):
    cov_lines = dict()
    with open(json_path, 'r+', encoding="utf-8") as f:
        json_dict = json.load(f)
        json_dict = json_dict['files']
        for file_name in json_dict.keys():
            # print(file_name)
            cov_lines[file_name] = json_dict[file_name]['executed_lines']
    # print(cov_lines)
    return cov_lines


def get_method_num(json_dir, base_dir, workplace):
    # print("workplace is:", workplace)
    json_file = os.path.join(json_dir, 'coverage.json')
    if not os.path.exists(json_file):
        os.chdir(json_dir)
        os.system('coverage combine')
        os.system('coverage json')
        os.chdir(workplace)

    global all_cov_lines_dict, method_line
    all_cov_lines_dict = {}
    method_line = {}

    all_cov_lines_dict = get_all_cov_lines(json_file)

    method_line = get_all_method_line(base_dir)
    # print(method_line)

    # calc method coverage
    all_method_num = 0
    cov_method_num = 0
    for file, line in method_line.items():
        # if '__init__' in file:
        #     continue
        all_method_num += len(line)
        if file not in all_cov_lines_dict.keys():
            # print(file, len(line))
            continue
        for def_line in line:
            if def_line in all_cov_lines_dict[file]:
                cov_method_num += 1

    return cov_method_num, all_method_num


if __name__ == '__main__':
    json_file = './lemon_cov_mx_08_22/0/python/coverage.json'
    base_dir = '/share_container/tensorflow/tensorflow/python'
    cov_method_num, all_method_num = get_method_num(json_file, base_dir)
    print(all_method_num, cov_method_num, cov_method_num / all_method_num)
