#-*- coding : utf-8-*-
import os
import xlwt
from _get_method_num import get_method_num
from _get_python_line_branch import get_api_cov_line_branch
from _get_covered_branch import get_covered_branch
from get_unique_cov import xml2dict, json2dict, dict2set

all_packages = ["User_Level_API", "Graph_Level", "Operation", "General_Utility", "Environment_Dependent"]


class Package:
    def __init__(self, name):
        self.name = name
        self.all_line = 0
        self.cov_line = 0
        self.all_branch = 0
        self.cov_branch = 0
        self.all_fun = 0
        self.cov_fun = 0
        self.all_file = 0
        self.cov_file = 0
        self.cov_line_set = set()
        self.cov_branch_set = set()
        self.cov_fun_set = set()


def which_package(file_path=''):
    # if file_path.startwith('#workplace#software#pytorch3#'):
    #     file_path = file_path.split('#workplace#software#pytorch3#')[1]
    # "Graph_Level"
    for k in ["csrc#distributed#", 'csrc#fx', 'csrc#jit', 'torch#csrc#autograd#', 'aten#src#ATen#quantized',
              'torch#csrc#multiprocessing', '#optim']:
        if k in file_path:
            return 1
    # "Operation"
    for k in ["aten#src#ATen#native", 'torch#csrc#api#include#torch#nn', '#nn#']:
        if k in file_path:
            return 2
    # "General_Utility"
    for k in ['aten#src#TH#', 'aten#src#THC#', 'aten#src#THCUNN#', 'c10#core#', 'c10#util#', '#csrc#utils#',
              'torch#lib#c10d#', 'torch#csrc#Dtype', '#util', '#torch#custom_class.h', 'torch#library.h',
              'torch#custom_class_detail', 'torch#custom_class.h']:
        if k in file_path:
            return 3
    # "Environment_Dependent"
    for k in ['c10#cuda#', 'c10#mobile#', 'csrc#cuda#', 'aten#src#ATen#cpu', 'aten#src#ATen#cuda',
              'aten#src#ATen#cudnn', 'aten#src#ATen#metal', 'aten#src#ATen#miopen', 'aten#src#ATen#mkl',
              'aten#src#ATen#nnapi', 'aten#src#ATen#vulkan',
              'torch#csrc#cuda', 'torch#lib#libshm']:
        if k in file_path:
            return 4
    for k in ['aten#src#ATen#', '#torch#csrc#']:
        if k in file_path:
            return 3
    print(f"No match package: {file_path}")
    return -1


def is_pytorch_gcov_file(file):
    if '#workplace#software#pytorch3#cmake#^#third_party#' in file \
            or '#workplace#software#pytorch3#third_party#' in file \
            or '#workplace#software#pytorch3#caffe2' in file \
            or '#workplace#software#pytorch3#build#caffe2' in file\
            or '#workplace#software#pytorch3#test' in file:
        return False
    if '#workplace#software#pytorch3' in file or file.startswith('aten#'):  # 为啥不以workplace开头？？
        return True
    return False


print(f'project \t all_source_LOC \t covered_LOC \t cov_line_rate \t all_branch_num \t covered_branch \t branch_rate '
      f'\t all_fun_num \t covered_fun \t fun_rate \t all_file \t cov_file \t file_rate')


def collect_all(project_name, gcovpath):
    book = xlwt.Workbook()
    sheet = book.add_sheet(project_name)
    workplace = gcovpath
    if project_name == 'testsuite':
        gcovpath = os.path.join(gcovpath, '/unit_cov/res_cov_07_29/')
    elif project_name == 'lemon':
        gcovpath = os.path.join(gcovpath, 'CovByLemon/lemon_cov_pt_8models')
    elif project_name == 'cradle' or project_name == 'audee':
        gcovpath = os.path.join(gcovpath, 'audee_cov_pt_6models')  # audee_cov_mx_08_22
    # for model in os.listdir(gcovpath):
    for model in range(1):
        if project_name == 'cradle' or project_name == 'testsuite':
            model = 0
        elif project_name == 'lemon':
            model = 99
        elif project_name == 'audee':
            model = 99
        else:
            assert False, f"this project {project_name} is not support! Check the name!"
        all_source_LOC = 0   # calc the LOC in the source code
        all_function_num = 0
        all_branch_num = 0
        all_file_num = 0

        covered_LOC = 0
        covered_fun = 0
        covered_branch = 0
        covered_file = 0

        package_cov = []
        for p in all_packages:
            package_cov.append(Package(p))

        python_cov_dir = os.path.join(gcovpath, str(model) + '/python/')

        dict_python_cov_line = json2dict(os.path.join(python_cov_dir, 'coverage.json'), 'line')
        package_cov[0].cov_line_set = dict2set(dict_python_cov_line, 'line')
        dict_python_cov_branch = xml2dict(os.path.join(python_cov_dir, 'coverage.xml'))
        package_cov[0].cov_branch_set = dict2set(dict_python_cov_branch, 'branch')
        dict_python_cov_fun = json2dict(os.path.join(python_cov_dir, 'coverage.json'), 'fun')
        package_cov[0].cov_fun_set = dict2set(dict_python_cov_fun, 'fun')

        package_cov[0].cov_line = len(package_cov[0].cov_line_set)
        package_cov[0].cov_branch = len(package_cov[0].cov_branch_set)
        package_cov[0].cov_fun = len(package_cov[0].cov_fun_set)

        package_cov[0].all_line = 77676
        package_cov[0].all_branch = 26144
        package_cov[0].all_file = 1
        package_cov[0].all_fun = 15129  # remove __init__.py
        if project_name == 'testsuite':
            # the below should be same in mxnet, however ,have a little difference.
            package_cov[0].all_line = 30467
            package_cov[0].all_branch = 10939
            package_cov[0].cov_file = 1
        else:
            package_cov[0].all_line = 77676
            package_cov[0].all_branch = 26144
            package_cov[0].cov_file = 1  # file number is always same

        stmt_info_path = f'line_{project_name}.txt'
        fun_info_path = f'fun_{project_name}.txt'
        branch_info_path = f'branch_{project_name}.txt'
        stmtfile = open(stmt_info_path, 'w')
        funfile = open(fun_info_path, 'w')
        branchfile = open(branch_info_path, 'w')

        stmt_cov_set = set()
        branch_cov_set = set()
        fun_cov_set = set()

        for t in package_cov[0].cov_line_set:
            stmt_cov_set.add(t)
            stmtfile.write(f'{t}\n')
        for t in package_cov[0].cov_branch_set:
            branch_cov_set.add(t)
            branchfile.write(f'{t}\n')
        for t in package_cov[0].cov_fun_set:
            fun_cov_set.add(t)
            funfile.write(f'{t}\n')

        cov_path = gcovpath + f'/{model}/c/'
        gcovfilepaths = os.listdir(cov_path)
        for gcovfilepath in gcovfilepaths:
            fullpath = cov_path + gcovfilepath
            if not is_pytorch_gcov_file(gcovfilepath):
                continue

            package_item = which_package(gcovfilepath)
            all_file_num += 1
            package_cov[package_item].all_file += 1

            # assert package_item != -1, f"need to be improved. {gcovfilepath}"
            if package_item == -1:
                print(f"need to be improved. {gcovfilepath}")
            gcovfile = open(fullpath, 'r')
            gcovlines = gcovfile.readlines()

            tmp = []
            tmp_fun = []
            tmp_branch = get_covered_branch(fullpath)

            for gcovline in gcovlines:
                gcovline = gcovline.strip()
                if gcovline.startswith('function'):
                    all_function_num += 1
                    package_cov[package_item].all_fun += 1
                    # SF_ called 0 returned 0% blocks executed 0% , judge function cov according to call number != 0
                    is_called = gcovline.split(" ")[-6].strip() != '0'
                    covered_fun += is_called
                    package_cov[package_item].cov_fun += is_called
                    if is_called:
                        fun_name = gcovline.split(' ')[1].strip()
                        tmp_fun.append(fun_name)
                elif gcovline.startswith('branch'):
                    all_branch_num += 1
                    package_cov[package_item].all_branch += 1
                    # example: branch  0 never executed ;;or ;; branch  0 taken 0%;; branch  0 taken 100%
                    last_word = gcovline.split(' ')[-1].strip()
                    if last_word != 'executed' and last_word != '0%':
                        covered_branch += 1
                        package_cov[package_item].cov_branch += 1
                else:  # line
                    if ':' not in gcovline:
                        continue
                    covcnt = gcovline.split(':')[0].strip()
                    linenum = gcovline.split(':')[1].strip()
                    if covcnt != '-' and covcnt != '#####':
                        tmp.append(linenum)
                        package_cov[package_item].cov_line += 1
                    if covcnt != '-':
                        all_source_LOC += 1
                        package_cov[package_item].all_line += 1
            if len(tmp) != 0:
                covered_file += 1
                package_cov[package_item].cov_file += 1
                covered_LOC += len(tmp)
            for t in tmp:
                stmt_cov_set.add(f"{gcovfilepath}_{t}")
                package_cov[package_item].cov_line_set.add(f"{gcovfilepath}_{t}")
                stmtfile.write(f'{gcovfilepath}_{t}\n')
            for t in tmp_branch:
                branch_cov_set.add(f"{gcovfilepath}_{t}")
                package_cov[package_item].cov_branch_set.add(f"{gcovfilepath}_{t}")
                branchfile.write(f'{gcovfilepath}_{t}\n')
            for t in tmp_fun:
                fun_cov_set.add(f"{gcovfilepath}_{t}")
                package_cov[package_item].cov_fun_set.add(f"{gcovfilepath}_{t}")
                funfile.write(f'{gcovfilepath}_{t}\n')

        if all_source_LOC == 0:
            continue
        stmtfile.close()
        funfile.close()
        branchfile.close()
        # print("debug", covered_fun, package_cov[0].cov_fun, '.../..')
        # for i in range(len(package_cov)):
        #     print(package_cov[i].name,
        #           package_cov[i].all_line, package_cov[i].cov_line, package_cov[i].cov_line/package_cov[i].all_line,
        #           package_cov[i].all_branch, package_cov[i].cov_branch, package_cov[i].cov_branch/package_cov[i].all_branch,
        #           package_cov[i].all_fun, package_cov[i].cov_fun, package_cov[i].cov_fun/package_cov[i].all_fun,
        #           package_cov[i].all_file, package_cov[i].cov_file, package_cov[i].cov_file/package_cov[i].all_file,
        #           )
        for i in range(len(package_cov)):
            print(package_cov[i].name,
                  package_cov[i].cov_line/package_cov[i].all_line,
                  package_cov[i].cov_branch/package_cov[i].all_branch,
                  package_cov[i].cov_fun/package_cov[i].all_fun,
                  # package_cov[i].cov_file/package_cov[i].all_file,
                  )
        # calc the total coverage by each line/branch/method/file
        # total_line_cov = (package_cov[0].cov_line + covered_LOC ) / (package_cov[0].all_line + all_source_LOC)

        total_cov_line = (sum([package_cov[i].cov_line for i in range(len(package_cov))])) / sum([package_cov[i].all_line for i in range(len(package_cov))])
        total_cov_branch = (sum([package_cov[i].cov_branch for i in range(len(package_cov))])) / sum([package_cov[i].all_branch for i in range(len(package_cov))])
        total_cov_method = (sum([package_cov[i].cov_fun for i in range(len(package_cov))])) / sum([package_cov[i].all_fun for i in range(len(package_cov))])
        total_cov_file = (sum([package_cov[i].cov_file for i in range(len(package_cov))])) / sum([package_cov[i].all_file for i in range(len(package_cov))])
        print(model, total_cov_line, total_cov_branch, total_cov_method)

        # sheet.write(model, 0, total_cov_line)
        # sheet.write(model, 1, total_cov_branch)
        # sheet.write(model, 2, total_cov_method)
        # sheet.write(model, 3, total_cov_file)
    book.save("cov_increase2.xls")
    return package_cov


if __name__ == '__main__':
    gcovpath = '/share_container/pycharmProjects/DLLTesting/pytorch_cov/'

    # project = 'testsuite'
    project = 'cradle'
    # project = 'lemon'
    # project = 'audee'
    collect_all(project, gcovpath)
    # collect_all(project, gcovpath)
    package_cov_lemon = collect_all('lemon', gcovpath)
    package_cov_audee = collect_all('audee', gcovpath)

    #
    for i in range(len(package_cov_audee)):
        package_cov_audee[i].cov_line_set = package_cov_audee[i].cov_line_set | package_cov_lemon[i].cov_line_set
        package_cov_audee[i].cov_branch_set = package_cov_audee[i].cov_branch_set | package_cov_lemon[i].cov_branch_set
        package_cov_audee[i].cov_fun_set = package_cov_audee[i].cov_fun_set | package_cov_lemon[i].cov_fun_set

        package_cov_audee[i].cov_line = len(package_cov_audee[i].cov_line_set)
        package_cov_audee[i].cov_branch = len(package_cov_audee[i].cov_branch_set)
        package_cov_audee[i].cov_fun = len(package_cov_audee[i].cov_fun_set)

    package_cov = package_cov_audee

    for i in range(len(package_cov)):
        print(package_cov[i].name,
              package_cov[i].cov_line/package_cov[i].all_line,
              package_cov[i].cov_branch/package_cov[i].all_branch,
              package_cov[i].cov_fun/package_cov[i].all_fun,
              )

    total_cov_line = (sum([package_cov[i].cov_line for i in range(len(package_cov))])) / sum(
        [package_cov[i].all_line for i in range(len(package_cov))])
    total_cov_branch = (sum([package_cov[i].cov_branch for i in range(len(package_cov))])) / sum(
        [package_cov[i].all_branch for i in range(len(package_cov))])
    total_cov_method = (sum([package_cov[i].cov_fun for i in range(len(package_cov))])) / sum(
        [package_cov[i].all_fun for i in range(len(package_cov))])
    total_cov_file = (sum([package_cov[i].cov_file for i in range(len(package_cov))])) / sum(
        [package_cov[i].all_file for i in range(len(package_cov))])
    print("Total", total_cov_line, total_cov_branch, total_cov_method)






