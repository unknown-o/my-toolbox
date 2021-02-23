#!/usr/bin/python
# coding: utf-8
import sys
import os
result=os.popen('nmap -p'+sys.argv[1]+'-'+sys.argv[2]+' '+sys.argv[3]).read()
with open('/www/server/panel/plugin/my_toolbox/result.tmp', 'w') as f:
    f.write(result)
f.close