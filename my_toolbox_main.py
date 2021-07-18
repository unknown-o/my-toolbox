#!/usr/bin/python
# coding: utf-8
# +--------------------------------------------------------------------------------
# | 我的工具箱                                                                   
# +--------------------------------------------------------------------------------
# | Copyright (c) 2015-2099 UnknownO(https://unknown-o.com) All rights reserved        
# +--------------------------------------------------------------------------------
# | Author: 吴先森 <i@mr-wu.top>
# +--------------------------------------------------------------------------------

import hashlib
import panelTask
import public
import sys
import os
import json
import time
import requests
import panelTask

os.chdir("/www/server/panel")

sys.path.append("class/")
if __name__ != '__main__':
    from BTPanel import cache, session, redirect

class my_toolbox_main:
    __plugin_path = "/www/server/panel/plugin/my_toolbox/"
    __config = None

    def __init__(self):
        pass

    def startScanPort(self, args):
        if(os.popen('command -v nmap').read() == '' or not os.path.exists("/www/server/panel/pyenv/bin/python")):
            return {'msg': '环境缺失，暂时不能使用本功能！', 'status': -1}
        public.ExecShell('kill -9 ' + str(os.popen("echo `ps ax | grep -i '/plugin/my_toolbox/nmap.py' | sed 's/^\([0-9]\{1,\}\).*/\1/g' | head -n 1`").read()))
        if(os.path.exists("/www/server/panel/plugin/my_toolbox/tmp/portScan.tmp")):
            os.remove('/www/server/panel/plugin/my_toolbox/tmp/portScan.tmp')
        if(not (int(args.portStart) > 0 and int(args.portEnd) < 65535) or args.serverIp == "" or args.portStart >= args.portEnd):
            return {'msg': '输入数据存在错误', 'status': -1}
        task = panelTask.bt_task()
        task.create_task("扫描端口",0,"/www/server/panel/pyenv/bin/python /www/server/panel/plugin/my_toolbox/nmap.py " + args.portStart + " " + args.portEnd + " " + args.serverIp)
        return {'msg': '成功创建任务', 'status': 1}

    def getScanResult(self, args):
        if(os.path.exists("/www/server/panel/plugin/my_toolbox/tmp/portScan.tmp")):
            portScanResult = open("/www/server/panel/plugin/my_toolbox/tmp/portScan.tmp")
            line = portScanResult.readline()
            portScanResultArr = []
            while line:
                if('open' in line):
                    portScanResultArr.append({"port":line.split()[0],"status":line.split()[1],"type":line.split()[2]})
                line = portScanResult.readline()
            portScanResult.close()
            os.remove('/www/server/panel/plugin/my_toolbox/tmp/portScan.tmp')
            return {'msg': "扫描完成", "data": portScanResultArr, 'status': 1}
        else:
            return {'msg': '扫描中...', 'status': -1}

    def getHostsList(self, args):
        hostsFile = open("/etc/hosts")
        hostsArr = []
        while 1:
            line = hostsFile.readline()
            if(not line):
                break
            if(not line == "\n"):
                hostsArr.append({"ip":line.split(" ", 1)[0].strip(), "domain":line.split(" ", 1)[1].strip(), "original":line.strip("\n")})
        return {'msg': "查询成功！", "data": hostsArr, 'status': 1}

    def addHosts(self, args):
        with open('/etc/hosts', 'a') as hostsFile:
            hostsFile.write('\n')
            hostsFile.write(args.ip+' '+args.domain)
        return {'msg': '编辑hosts成功！', 'status': 1}

    def delHosts(self, args):
        hostsFileOld = open("/etc/hosts")
        hostsNew = ''
        while(1):
            line = hostsFileOld.readline()
            if(not line):
                break
            if(not line == '\n'):
                if(not args.original in line):
                    hostsNew = hostsNew + line
        hostsFileOld.close()
        with open("/etc/hosts", 'w') as f:
            f.write(hostsNew)
        return {'msg': '成功删除此条hosts', 'status': 1}

    def short_url(self, args):
        url = 'https://api.unknown-o.com/shorturl/'
        nowTime = int(time.time())
        data = {'key': hashlib.md5(('KagamineYes!'+str(nowTime)).encode(
            "utf-8")).hexdigest(), 'timestamp': nowTime, 'type': args.type, 'url': args.url}
        r = json.loads(requests.post(url, data).text)
        return {'status': 1, 'result': r['result']}

    def get_shell_result(self, args):
        if(os.path.exists("/www/server/panel/plugin/my_toolbox/result.shell.tmp")):
            file = open("/www/server/panel/plugin/my_toolbox/result.shell.tmp")
            result = ''
            a = 0
            while 1:
                line = file.readline()
                if not line:
                    break
                result = result+line
            file.close()
            if(result == 'MyToolbox：It has been successfully obtained!'):
                return {'message': 'fail', 'status': 3}
            with open("/www/server/panel/plugin/my_toolbox/result.shell.tmp", 'w') as f:
                f.write('MyToolbox：It has been successfully obtained!')
            if(result == ''):
                return {'message': '执行成功!但是您执行的脚本并没有任何反馈哦!请自行确认是否执行成功!', 'status': 1}
            else:
                return {'message': result.replace("\n", "<br>"), 'status': 1}
        else:
            return {'message': 'execing', 'status': 0}

    def sitemap_made(self, args):
        if(os.path.exists("/www/server/panel/plugin/my_toolbox/static/sitemap.xml")):
            os.remove('/www/server/panel/plugin/my_toolbox/static/sitemap.xml')
        if(os.path.exists("/www/server/panel/pyenv/bin/python")):
            result = os.popen(
                '/www/server/panel/pyenv/bin/python /www/server/panel/plugin/my_toolbox/sitemap.py '+args.url).read()
        else:
            if(os.popen('command -v python3').read() == ''):
                return 'Python3环境缺失！请手动安装！'
            else:
                result = os.popen(
                    'python3 /www/server/panel/plugin/my_toolbox/sitemap.py '+args.url).read()
        if(result == ''):
            if(os.path.exists("/www/server/panel/plugin/my_toolbox/static/sitemap.xml")):
                file = open(
                    "/www/server/panel/plugin/my_toolbox/static/sitemap.xml")
                while 1:
                    line = file.readline()
                    if not line:
                        break
                    result = result+line
                file.close()
        return result

    def exec_d(self, args):
        if(os.path.exists("/www/server/panel/plugin/my_toolbox/result.shell.tmp")):
            os.remove('/www/server/panel/plugin/my_toolbox/result.shell.tmp')
        with open("/www/temp.sh", 'w') as f:
            f.write(args.input_r)
        f.close
        t = panelTask.bt_task()
        t.create_task(
            "命令执行", 0, 'python3 /www/server/panel/plugin/my_toolbox/exec_shell.py')
        return 1

    def request_page(self, args):
        try:
            response = requests.get(args.url)
            response.encoding = "utf-8"
            if(response.status_code == 200):
                return {'message': '请求网页成功！', 'result': "HttpCode: "+str(response.status_code)+"\n\n"+response.text, 'status': 1}
            else:
                return {'message': '警告！httpCode并非200！', 'result': "HttpCode: "+str(response.status_code)+"\n\n"+response.text, 'status': 7}
        except:
            return {'message': '错误！未知原因引起请求程序出错崩溃！', 'result': "HttpCode: "+str(response.status_code)+"\n\n"+response.text, 'status': 2}

    def addSoftLink(self, args):
        if(not (os.path.exists(args.source) and os.path.exists(args.softSource))):
            return {'msg': '输入数据存在错误！', 'status': -1}
        os.system('ln -s ' + args.source+' ' + args.softSource)
        return {'msg': '成功创建软链接！', 'status': 1}