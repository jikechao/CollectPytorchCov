import os
import logging
logging.basicConfig(level=logging.ERROR)


def is_branch_line(l):
    if l.startswith('//') or l.startswith('#'):
        return False
    if l.startswith("if") or 'else if' in l or l.startswith('switch') \
            or l.startswith('while') or l.startswith('for'):
        return True
    elif 'while' in l and '(' in l and ')' in l:  # do... while
        return True
    elif '?' in l and ':' in l:
        return True
    return False


def get_branch_num_for_single_file(file_name, source_dir):
    print(file_name)
    branch_num = 0
    branch_cov_num = 0
    with open(file_name) as f:
        lines = f.readlines()
    source_file = lines[0].split(':')[-1].strip()
    source_file = os.path.join(source_dir, source_file)
    print(source_file)

    source_branch_pos = []
    with open(source_file) as f:
        ls = f.readlines()
    for num, l in enumerate(ls):
        l = l.strip()
        num += 1
        if is_branch_line(l):
            # print(l)
            source_branch_pos.append(num)
    #  ------------------------------------
    # print(source_branch_pos)
    i = 5
    while i < len(lines):
        line = lines[i]
        if ":" not in line or line.startswith('-'):
            i += 1
            continue
        line_id = line.split(":")[1].strip()
        line_id = int(line_id)
        if line_id in source_branch_pos:
            this_branch = 0
            j = i + 1
            while j < len(lines) and lines[j].startswith("branch"):
                this_branch += 1
                last_word = lines[j].split(' ')[-1].strip()
                if last_word != 'executed' and last_word != '0%':
                    branch_cov_num += 1
                j += 1
            if this_branch == 0:
                # logging.error(f"the line {line_id} have no branch! Content is : {ls[line_id-1].strip()}")
                pass
            if this_branch > 2:
                # if not switch and branch>2, this may have some error
                pass
            branch_num += this_branch
            i = j
        else:
            i += 1
    return branch_cov_num, branch_num


if __name__ == '__main__':
    cov_file = "res_cov_08_03/cpp_cov/src#profiler#profiler.cc.gcov"
    print(cov_file)
    branch_cov, branch_all = get_branch_num_for_single_file(cov_file,
                                                            '/workplace/software/mxnet2')