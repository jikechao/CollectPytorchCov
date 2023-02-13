import os


def get_api_cov_line_branch(xml_dir, workplace):
    all_branch = 0
    all_line = 0
    branch_cov = 0
    line_cov = 0

    xml_file = os.path.join(xml_dir, "coverage.xml")
    # print(xml_file)
    if not os.path.exists(xml_file):
        os.chdir(xml_dir)
        os.system("coverage combine")
        os.system("coverage xml")
        os.chdir(workplace)
    with open(xml_file, mode='r', encoding='utf-8') as f:
        lines = f.readlines()
    # print(len(lines))
    cov_infos = lines[1].split(" ")
    for info in cov_infos:
        info = info.strip()
        if 'branches-covered=' in info:
            branch_cov = int(info.split('\"')[1])
        elif 'lines-covered=' in info:
            line_cov = int(info.split('\"')[1])
        elif 'branches-valid=' in info:
            all_branch = int(info.split('\"')[1])
        elif 'lines-valid=' in info:
            all_line = int(info.split('\"')[1])
    return branch_cov
