#!/usr/bin/python
# coding: utf-8
import sys
import os
result = os.popen('nmap -p' + sys.argv[1] + '-' + sys.argv[2] + ' '+sys.argv[3]).read()
with open('/www/server/panel/plugin/my_toolbox/tmp/portScan.tmp', 'w') as resultFile:
    resultFile.write(result)