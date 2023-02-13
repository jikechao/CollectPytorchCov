import os
import json


def file2dict(file):
    res = dict()
    with open(file) as f:
        lines = f.readlines()
    for l in lines:
        l = l.strip()
        name = l.split(':')[0]
        value = l.split(':')[1]
        if name not in res.keys():
            res[name] = []
        for v in value.split(','):
            res[name].append(v)
    return res


def get_method_line(file):
    line_list = []
    line_num = 0
    with open(file, 'r+', encoding="utf-8") as f:
        all_lines = f.readlines()
        for line in all_lines:
            line_num += 1
            line = line.strip()
            if 'def ' == line[:4]:
                line_list.append(line_num)
            continue
    return line_list


def get_all_method_line(base_dir):
    all_fun = 0
    method_line = dict()
    for dir_path, dir_name, files in os.walk(base_dir):
        for file in files:
            if not file.endswith('.py'):
                continue
            if '__init__.py' in file:
                continue
            file_path = os.path.join(dir_path, file)
            temp_list = get_method_line(file_path)
            all_fun += len(temp_list)
            if temp_list and len(temp_list) > 0:
                method_line[file_path] = temp_list
    print(base_dir)
    print("debug___: all python method line is ", all_fun)
    return method_line


def json2dict(file, granularity='line'):
    res = dict()
    # if granularity == 'line' or granularity == 'file':
    with open(file, 'r') as f:
        json_dict = json.load(f)
        json_dict = json_dict['files']
        for file_name in json_dict.keys():
            if '__init__.py' in file_name:
                continue
            temp = json_dict[file_name]['executed_lines']
            cov_lines_num = json_dict[file_name]["summary"]["covered_lines"]
            # executed line not equeal to covered line
            # assert int(cov_lines_num) == len(temp),
            # f'true number is {len(temp)}, while the report say it is {cov_lines_num}; file name is:{file_name}'
            # if file_name.startswith('/workplace/software/mxnet/'):
            #     file_name = '/workplace/software/mxnet2/' + file_name[len('/workplace/software/mxnet/'):]
            if len(temp) == 0:
                continue
            res[file_name] = temp

    if granularity == 'fun':
        all_cov_lines_dict = res
        res = dict()
        base_dir = '/workplace/software/pytorch3/torch/'
        method_line = get_all_method_line(base_dir)

        for file, line in method_line.items():
            if file not in all_cov_lines_dict.keys():
                continue
            for def_line in line:
                if def_line in all_cov_lines_dict[file]:
                    if file not in res.keys():
                        res[file] = []
                    res[file].append(def_line)
    return res


def xml2dict(file):
    from xml.dom import minidom
    res = dict()
    dom = minidom.parse(file)
    data = dom.documentElement
    classes = data.getElementsByTagName('class')
    for clazz in classes:
        tmp = []
        class_name = clazz.getAttribute('filename')
        all_lines = clazz.getElementsByTagName('line')
        for line in all_lines:
            if line.getAttribute('branch').strip() != '' and line.getAttribute('hits').strip() == '1':
                line_num = line.getAttribute('number')
                # print(line_num)
                cov_state = line.getAttribute('condition-coverage')
                cov_state = cov_state.strip().split(' ')[1][1:-1]
                total_branch_this = int(cov_state.split('/')[1])
                cov_branch_this = int(cov_state.split('/')[0])
                missing_state = line.getAttribute('missing-branches').strip()
                missing_branch_list = missing_state.split(',')
                # 手动分析发现，对于部分覆盖，都是only缺少一个branch
                for i in range(cov_branch_this):
                    if str(int(line_num)+1) in missing_branch_list:
                        tmp.append(f'{line_num}_{i+1}')
                        # print(missing_state)
                    else:
                        tmp.append(f'{line_num}_{i}')
                        # print(missing_state)
        if len(tmp) != 0:
            # if class_name.startswith('/workplace/software/pytorch3/'):
            #     class_name = '/workplace/software/mxnet2/' + class_name[len('/workplace/software/mxnet/'):]
            res[class_name] = tmp
    return res


def dict2set(dict, granularity='line'):
    res = set()
    if granularity == 'file':
        for k in dict.keys():
            res.add(k)
    else:
        for k, v in dict.items():
            for t in v:
                res.add(k+f'_{t}')
    return res


# def calc_unique(dict_a, dict_b, granularity='line'):
#     diff_num = 0
#     # the unique of b related to a
#     if granularity == 'line':
#         for k, value in dict_b.items():
#             if k not in dict_a:
#                 diff_num += len(value)
#                 continue
#             for v_item in value:
#                 if v_item not in dict_a[k]:
#                     diff_num += 1
#
#     elif granularity == 'file':
#         diff_file = set()
#         for k, value in dict_b.items():
#             if k not in dict_a:
#                 diff_file.add(k)  # unique file
#                 continue
#         diff_num = len(diff_file)
#     return diff_num
#
#
# def get_unique_cov_c(file_a, file_b, granularity='line'):
#     dict_a = file2dict(file_a)
#     dict_b = file2dict(file_b)
#     diff_num = calc_unique(dict_a, dict_b)
#     return diff_num
#
#
# def get_unique_cov_python(file_a, file_b, granularity='line'):
#     dict_a = json2dict(file_a)
#     dic_b = json2dict(file_b)
#     diff_num = calc_unique(dict_a, dic_b)
#     return diff_num
#
#
# def get_unique_coverage(pro_a, pro_b, granularity='line'):
#     pro_a_c = pro_a + 'c'
#     pro_a_python = pro_a + 'python/coverage.json'
#
#     pro_b_c = pro_b + 'c'
#     pro_b_python = pro_b + 'python/coverage.json'
#
#     if granularity == 'line':
#         file_name = 'stmt_info.txt'
#     else:
#         assert False, "not support yet!"
#
#     diff_num_c = get_unique_cov_c(os.path.join(pro_a_c, file_name), os.path.join(pro_b_c, file_name))
#     diff_num_python = get_unique_cov_python(pro_a_python, pro_b_python)
#     diff_num = diff_num_c + diff_num_python
#     return diff_num


def get_all_set(pro, granularity="line"):
    pro_c = pro + 'c'
    pro_python = pro + 'python/coverage.json'
    if granularity == 'line' or granularity == 'file':
        file_name = 'stmt_info.txt'
    elif granularity == 'fun':
        file_name = 'fun_info.txt'
    elif granularity == 'branch':
        file_name = 'branch_info.txt'
        pro_python = pro + 'python/coverage.xml'
    else:
        assert False, "not support yet!"
    pro_c = os.path.join(pro_c, file_name)
    dict_c = file2dict(pro_c)
    if granularity == 'branch':
        dict_python = xml2dict(pro_python)
    else:
        dict_python = json2dict(pro_python, granularity)
        # print("the total cov python file number is ", len(dict_python))
        import numpy as np
        print("the total cov line of python is ", np.sum([len(i) for i in dict_python.values()]))
    set_c = dict2set(dict_c, granularity)
    set_python = dict2set(dict_python, granularity)
    return set_c, set_python


if __name__ == '__main__':
    # testsuite_cov = '../pytorch_cov/unit_cov/mxnet/res_cov_08_03/0/'
    cradle_cov = './audee_cov_pt_6models/0/'
    # lemon_cov = './CovByLemon/lemon_cov_pt_8models/99/'
    audee_cov = './audee_cov_pt_6models/99/'

    all_pro = [cradle_cov, audee_cov]  #  lemon_cov,

    # cradle_audee = get_unique_coverage(cradle_cov, audee_cov, granularity="line")
    # cradle_lemon = get_unique_coverage(cradle_cov, lemon_cov, granularity="line")
    # cradle_testsuite = get_unique_coverage(cradle_cov, testsuite_cov, granularity="line")
    #
    # lemon_audee = get_unique_coverage(lemon_cov, audee_cov, granularity='line')
    # audee_lemon = get_unique_coverage(audee_cov, lemon_cov, granularity='line')
    #
    # print(cradle_lemon, cradle_audee, cradle_testsuite)
    # print(lemon_audee, audee_lemon)
    # granularity = 'fun'
    granularity = 'line'
    # granularity = 'branch'
    for pro in all_pro:
        pro_name = pro.split('/')[1].split('_')[0]
        if '/audee_cov_pt_6models/0/' in pro:
            pro_name = 'cradle'
        elif 'res_cov_08_03' in pro:
            pro_name = 'testsuite'
        print(pro_name)
        c, python = get_all_set(pro, granularity)
        with open(f'{granularity}_{pro_name}_set.txt', mode='w') as f:
            for i in c:
                f.write(i+'\n')
            for j in python:
                # if j.startswith('/workplace/software/mxnet/'):
                #     j = '/workplace/software/mxnet2/' + j[len('/workplace/software/mxnet/'):]
                f.write(j+'\n')
        print(len(c) + len(python))
