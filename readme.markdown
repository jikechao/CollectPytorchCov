## Introduction

This rough tool is design for collecting coverage of PyTorch.  After you run `python main.py`, you can receive the coverage of python&& c++ coverage result. The tool is rough enough, you need a major revision to run it successfully.



## Notices

1. You can't run it success unless you modify the absolute path in these scripts.
2. The coverage about python is collected using `coverage.py` , you must install it by  `pip install coverage`  and execute it to collect python coverage. After you gain the python coverage info, you should put the value into `main.py`. otherwise, you will get wrong total coverage result.