import os

gcovpath = '/share_container/pycharmProjects/DLLTesting/pytorch_cov/gcov_06-10/'

model_names = os.listdir(gcovpath)

print(f'project \t all_source_LOC \t all_source_LOC \t cov_line_rate')
for model in model_names:
    all_source_LOC = 0  # calc the LOC in the source code
    covered_LOC = 0
    cov_path = gcovpath + model + '/'
    stmt_info_path = cov_path + 'stmt_info.txt'
    stmtfile = open(stmt_info_path, 'w')

    temp = []

    gcovfilepaths = os.listdir(cov_path)
    for gcovfilepath in gcovfilepaths:
        fullpath = cov_path + gcovfilepath
        gcovfile = open(fullpath, 'r')
        gcovlines = gcovfile.readlines()

        tmp = []
        for gcovline in gcovlines:
            if ':' not in gcovline:
                continue
            covcnt = gcovline.strip().split(':')[0].strip()
            linenum = gcovline.strip().split(':')[1].strip()
            if covcnt != '-' and covcnt != '#####':
                tmp.append(linenum)
            if covcnt != '-':
                all_source_LOC += 1

        if not tmp:
            continue
        temp += tmp
        # print(gcovfilepath, tmp)
        stmtfile.write(gcovfilepath+':'+','.join(tmp)+'\n')
        covered_LOC += len(tmp)

    # print('=={}=='.format(cov_path))
    # print(temp)
    if all_source_LOC ==0:
        continue
    print(f'{model}\t{all_source_LOC}\t{covered_LOC}\t{covered_LOC/all_source_LOC}')
    stmtfile.close()
