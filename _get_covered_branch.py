import os
import logging
logging.basicConfig(level=logging.ERROR)


def get_covered_branch(file_name):
    # print(file_name)
    res_list = []

    with open(file_name) as f:
        lines = f.readlines()
    i = 1
    while i < len(lines):
        line = lines[i]
        if ":" not in line or line.startswith('-'):
            i += 1
            continue
        line_id = line.split(":")[1].strip()
        line_id = int(line_id)
        j = i + 1
        while j < len(lines) and lines[j].startswith("branch"):
            last_word = lines[j].split(' ')[-1].strip()
            if last_word != 'executed' and last_word != '0%':
                # branch_id = lines[j].split(' ')[2].strip()
                branch_id = lines[j][len("branch "):].strip().split(" ")[0]
                res_list.append(f'{line_id}_{branch_id}')
            j += 1
        i = j
    return res_list


if __name__ == '__main__':
    cov_file = "lemon_cov_mx_08_22/99/c/src#storage#storage.cc.gcov"
    print(cov_file)
    res = get_covered_branch(cov_file)
    print(res)
