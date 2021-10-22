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

    def getHostsFile(self, args):
        return {'msg': "查询成功！", "data": open("/etc/hosts").read(), 'status': 1}

    def saveHostsFile(self, args):
        os.system("cp /etc/hosts /etc/hosts.bak")
        with open('/etc/hosts', 'w') as hostsFile:
            hostsFile.write(args.data)
        return {'msg': '编辑hosts成功！', 'status': 1}

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

    def createShortLink(self, args):
        url = 'https://api.unknown-o.com/shorturl/'
        nowTime = int(time.time())
        data = {'key': hashlib.md5(('KagamineYes!'+str(nowTime)).encode("utf-8")).hexdigest(), 'timestamp': nowTime, 'type': "n", 'url': args.url}
        response = json.loads(requests.post(url, data).text)
        return {'status': 1, 'result': response['result']}

    def getExecuteResult(self, args):
        if(os.popen("echo $(ps -ef | grep '/www/temp.sh' | grep -v grep | awk '{print $2}')").read() == "\n"):
            if(os.path.exists("/www/server/panel/plugin/my_toolbox/tmp/executeCommand.tmp")):
                executeCommandResult = open("/www/server/panel/tmp/" + args.logFileName).read()
                if(executeCommandResult == ""):
                    msg = "执行成功？但是没有任何返回！请自行检查命令是否运行成功！"
                else:
                    msg = "执行成功！" 
                return {"msg": msg, "result":executeCommandResult, "status":1}
            else:
                return {"msg": "抱歉，找不到运行结果！执行命令失败？", "result":"", "status":2}
        else:
            return {'msg': '正在执行中...', 'status': -1}

    def getSitemapGenerationStatus(self, args):
        if(os.path.exists("/www/server/panel/plugin/my_toolbox/static/sitemap.xml")):
            data = open("/www/server/panel/plugin/my_toolbox/static/sitemap.xml").read()
            return {'msg': "生成成功", "data": data, 'status': 1}
        else:
            return {'msg': '扫描中...', 'status': -1}

    def sitemapGeneration(self, args):
        if(not os.path.exists("/www/server/panel/pyenv/bin/python")):
            return {'msg': '不是python3版本的宝塔，暂时无法使用本功能！', 'status': -1}
        public.ExecShell('kill -9 ' + str(os.popen("echo `ps ax | grep -i '/plugin/my_toolbox/sitemap.py' | sed 's/^\([0-9]\{1,\}\).*/\1/g' | head -n 1`").read()))
        if(os.path.exists("/www/server/panel/plugin/my_toolbox/static/sitemap.xml")):
            os.remove('/www/server/panel/plugin/my_toolbox/static/sitemap.xml')
        if(int(args.maxNumber) < 15 and args.url == ""):
            return {'msg': '输入数据存在错误', 'status': -1}
        task = panelTask.bt_task()
        task.create_task("创建网站地图",0,"/www/server/panel/pyenv/bin/python /www/server/panel/plugin/my_toolbox/sitemap.py '" + args.url + "' " + str(args.maxNumber))
        return {'msg': '成功创建任务', 'status': 1}

    def displayOnce(self, args):
        if(os.path.exists('/www/server/panel/plugin/my_toolbox/tmp/'+args.item)):
            return {'result': 0, 'status': 1}
        else:
            displayOnceFlag = open('/www/server/panel/plugin/my_toolbox/tmp/'+args.item, 'a')
            displayOnceFlag.write('showed')
            displayOnceFlag.close()
            return {'result': 1, 'status': 1}

    def logWrite(self, args):
        public.WriteLog(args.logType,args.logDetail)
        return {'msg': '写入成功', 'status': 1}

    def executeCommand(self, args):
        if(not os.path.exists("/www/server/panel/pyenv/bin/python")):
            return {'msg': '不是python3版本的宝塔，暂时无法使用本功能！', 'status': -1}
        if(os.path.exists("/www/server/panel/plugin/my_toolbox/tmp/executeCommand.tmp")):
            os.remove('/www/server/panel/plugin/my_toolbox/tmp/executeCommand.tmp')
        public.ExecShell('kill -9 ' + str(os.popen("echo $(ps -ef | grep '/www/temp.sh' | grep -v grep | awk '{print $2}')").read()))
        with open("/www/temp.sh", 'w') as bashCommandFile:
            bashCommandFile.write(args.bashCommand)
            bashCommandFile.write("\necho finsh > /www/server/panel/plugin/my_toolbox/tmp/executeCommand.tmp")
        task = panelTask.bt_task()
        logList = os.listdir('/www/server/panel/tmp/')
        logList.sort(key=lambda x:int(x[:-4]))
        task.create_task("命令执行", 0, 'bash /www/temp.sh')
        return {'msg': '成功创建任务', "logFileName":str(int(logList[-1].split(".")[0])+1)+".log", 'status': 1}

    def requestPage(self, args):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.70',
            }
            response = requests.get(args.url, headers=headers, timeout=(60,60))
            response.encoding = "utf-8"
            result = "HTTP状态码:" + str(response.status_code) + "\n"
            result = result + "页面打开耗时:" + str(response.elapsed.total_seconds()*1000) + "ms\n"
            result = result + "页面HTML内容:\n" + response.text
            return {'msg': '成功创建任务',"data": result ,'status': 1}
        except:
            return {'message': '错误！未知原因引起请求程序出错崩溃！', 'result': "HttpCode: "+str(response.status_code)+"\n\n"+response.text, 'status': 2}

    def addSoftLink(self, args):
        if(not (os.path.exists(args.source) and os.path.exists(args.softSource))):
            return {'msg': '输入数据存在错误！', 'status': -1}
        os.system('ln -s ' + args.source+' ' + args.softSource)
        return {'msg': '成功创建软链接！', 'status': 1}