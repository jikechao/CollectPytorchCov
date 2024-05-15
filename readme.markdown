## Introduction

This rough tool is designed for collecting coverage of PyTorch.  After you run `python main.py`, you can receive the coverage of python&& c++ coverage result. The tool is extremely rough, you need a major revision to run it successfully.



## Notices

1. You can't run it successfully unless you modify the absolute path in these scripts.
2. The coverage about Python is collected using `coverage.py`, you must install it by  `pip install coverage`  and execute it to collect Python coverage. After you gain the Python coverage info, you should put the value into `main.py`. otherwise, you will get the wrong total coverage result.
