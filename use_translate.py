#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
Author:   Jimu Yang
Contact:  17621660286@163.com
这是一个python2脚本 import workflow以及调用 yd-translate来工作
1. ascii cannot decote byte... 将默认编码设置为utf-8
2. 不要瞎写print alfred读取的就是sys.stdout
'''

from workflow import Workflow, ICON_INFO
import sys
import subprocess
import json

reload(sys)
sys.setdefaultencoding('utf-8')


def call_yd_translate(src):
    '''
    try use subprocess to invoke yd-translate.py
    '''
    obj = subprocess.Popen(['./translate.py', src], stdout=subprocess.PIPE)
    stdout = obj.stdout.read()
    obj.stdout.close()
    return stdout


def main(wf):
    trans_results = call_yd_translate(sys.argv[1])
    arr = trans_results.strip()[1:-1].split(',')
    for result in arr:
        result = result.strip()[1:-1]
        wf.add_item(title=result, subtitle='...',
                    arg=result, valid=True, icon=ICON_INFO)
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
