import os

gcovpath = '/share_container/pycharmProjects/DLLTesting/CovByLemon/lemon_cov_mx_08_18/lenet5-fashion-mnist/c/'
# gcovpath = '/share_container/pycharmProjects/DLLTesting/CovByLemon/lemon_cov_mx_08_22/'
model_names = os.listdir(gcovpath)


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


def which_package(file_path=''):
    # if file_path.startwith('#workplace#software#pytorch3#'):
    #     file_path = file_path.split('#workplace#software#pytorch3#')[1]
    # "Graph_Level"
    for k in ['cc/saved_model', 'c/eager/_objs', 'core', 'stream_executor']:    # 'graph',
        if k in file_path:
            return 1
    # "Operation"
    for k in ['cc/ops', 'c/_objs/ops', 'c/kernels/_objs/*_op', '_op']:
        if k in file_path:
            return 2
    # "General_Utility"
    for k in ['c/_objs/tf_tensor', '']:
        if k in file_path:
            return 3
    # "Environment_Dependent"
    for k in ['tools', ]:  # 'cpu', 'gpu', 'cuda',
        if k in file_path:
            return 4

    print(f"No match component: {file_path}")
    return -1


def is_pytorch_gcov_file(file):
    if '3rdparty' in file or '#usr#bin' in file or 'include#dmlc' in file or 'include#dlpack' in file \
            or 'include#mshadow' in file or 'include#nnvm' in file or 'test' in file:
        return False
    if 'src#' in file or file.startswith('include'):
        return True
    return False


print(f'project \t all_source_LOC \t covered_LOC \t cov_line_rate \t all_branch_num \t covered_branch \t branch_rate '
      f'\t all_fun_num \t covered_fun \t fun_rate \t all_file \t cov_file \t file_rate')
for model in model_names:
    # model = 'lenet5-fashion-mnist_origin0.h5_1'
    all_source_LOC = 0  # calc the LOC in the source code
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
    package_cov[0].all_line = 30467
    package_cov[0].cov_line = 21774
    package_cov[0].all_branch = 10939
    package_cov[0].cov_branch = 6462
    package_cov[0].all_fun = 4093
    package_cov[0].cov_fun = 3853
    package_cov[0].all_file = 189
    package_cov[0].cov_file = 182

    cov_path = gcovpath + model + '/'
    stmt_info_path = cov_path + 'stmt_info.txt'
    stmtfile = open(stmt_info_path, 'w')

    temp = []

    gcovfilepaths = os.listdir(cov_path)
    for gcovfilepath in gcovfilepaths:
        fullpath = cov_path + gcovfilepath
        # if not is_pytorch_gcov_file(gcovfilepath):
        #     continue

        package_item = which_package(gcovfilepath)
        all_file_num += 1
        package_cov[package_item].all_file += 1

        if package_item == -1:  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!! need to be improved.
            continue
        gcovfile = open(fullpath, 'r')
        gcovlines = gcovfile.readlines()

        tmp = []
        for gcovline in gcovlines:
            gcovline = gcovline.strip()
            if gcovline.startswith('function'):
                all_function_num += 1
                package_cov[package_item].all_fun += 1
                # SF_ called 0 returned 0% blocks executed 0% , judge function cov according to call number != 0
                is_called = gcovline.split(" ")[-6].strip() != '0'
                covered_fun += is_called
                package_cov[package_item].cov_fun += is_called
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
        if not tmp:
            continue
        temp += tmp
        # print(gcovfilepath, tmp)
        stmtfile.write(gcovfilepath+':'+','.join(tmp)+'\n')
        covered_LOC += len(tmp)

    # print('=={}=='.format(cov_path))
    # print(temp)
    if all_source_LOC == 0:
        continue

    # print(f'{model}\t{all_source_LOC}\t{covered_LOC}\t{covered_LOC/all_source_LOC}'
    #       f'\t{all_branch_num}\t{covered_branch}\t{covered_branch/all_branch_num}'
    #       f'\t{all_function_num}\t{covered_fun}\t{covered_fun/all_function_num}'
    #       f'\t{all_file_num}\t{covered_file}\t{covered_file/all_file_num}')
    stmtfile.close()
    # for i in range(len(package_cov)):
    #     print(package_cov[i].name, package_cov[i].all_line, package_cov[i].cov_line, package_cov[i].cov_line/package_cov[i].all_line,
    #           package_cov[i].all_branch, package_cov[i].cov_branch, package_cov[i].cov_branch/package_cov[i].all_branch,
    #           package_cov[i].all_fun, package_cov[i].cov_fun, package_cov[i].cov_fun/package_cov[i].all_fun,
    #           package_cov[i].all_file, package_cov[i].cov_file, package_cov[i].cov_file/package_cov[i].all_file,
    #           )
    # for i in range(len(package_cov)):
    #     print(package_cov[i].name,
    #           package_cov[i].cov_line/package_cov[i].all_line,
    #           package_cov[i].cov_branch/package_cov[i].all_branch,
    #           package_cov[i].cov_fun/package_cov[i].all_fun,
    #           package_cov[i].cov_file/package_cov[i].all_file,
    #           )
    # calc the total coverage by each line/branch/method/file
    # total_line_cov = (package_cov[0].cov_line + covered_LOC ) / (package_cov[0].all_line + all_source_LOC)

    total_cov_line = (sum([package_cov[i].cov_line for i in range(len(package_cov))])) / sum([package_cov[i].all_line for i in range(len(package_cov))])
    total_cov_branch = (sum([package_cov[i].cov_branch for i in range(len(package_cov))])) / sum([package_cov[i].all_branch for i in range(len(package_cov))])
    total_cov_method = (sum([package_cov[i].cov_fun for i in range(len(package_cov))])) / sum([package_cov[i].all_fun for i in range(len(package_cov))])
    total_cov_file = (sum([package_cov[i].cov_file for i in range(len(package_cov))])) / sum([package_cov[i].all_file for i in range(len(package_cov))])
    print(model, total_cov_line, total_cov_branch, total_cov_method, total_cov_file)
    # break

