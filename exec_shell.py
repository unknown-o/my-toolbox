#!/usr/bin/python
# coding: utf-8
import sys
import os
result=os.popen('bash /www/temp.sh').read()
with open('/www/server/panel/plugin/my_toolbox/result.shell.tmp', 'w') as f:
    f.write(result)
f.close
os.remove('/www/temp.sh')