#!/usr/bin/python
# coding: utf-8
import os
result=os.popen('bash /www/temp.sh').read()
with open('/www/server/panel/plugin/my_toolbox/tmp/executeCommand.tmp', 'w') as executeCommandResult:
    executeCommandResult.write(result)
os.remove('/www/temp.sh')