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
import re
import json
import time
import requests
import panelTask
import psutil
# import numpy as np

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

    def getDiskInfo(self, args):
        diskInfo = os.popen('fdisk -l |grep -E "Disk /dev/.*?:|磁盘 /dev/.*?："|grep -v  -E "/dev/loop|/dev/mapper"').read().strip().split('\n')
        dfInfo = os.popen('df -h').read()
        lvmInfo = os.popen('pvs').read()
        diskArr = []
        for item in diskInfo:
            tmp = {}
            item = item.split(' ')
            tmp['device'] = item[1].split(':')[0]
            tmp['partition'] = []
            partitionInfo = re.sub(' +', ' ', os.popen('lsblk -f -P %s'%tmp['device']).read()).strip().split('\n')
            for item1 in partitionInfo[1:]:
                partitionInfoP = item1.replace("\"","").split(" ")
                partitionInfoDict = {}
                for item2 in partitionInfoP:
                    keyName = item2.split("=")[0].lower()
                    keyName = (keyName, "device")[keyName == "name"]
                    if(len(item2.split("="))==1):
                        partitionInfoDict[keyName] = "-"
                    else:
                        partitionInfoDict[keyName] = (item2.split("=")[1], "-")[item2.split("=")[1] == ""]
                tmp['partition'].append(partitionInfoDict)
            tmp['mounted'] = tmp['device'] in dfInfo or tmp['device'] in lvmInfo
            tmp['has_lvm'] = tmp['device'] in lvmInfo
            tmp['warning'] = tmp['device'] in lvmInfo and len(tmp['partition']) == 0
            tmp['size_gb'] = item[2]
            tmp['size_bytes'] = item[4]
            tmp['sectors'] = item[6]
            diskArr.append(tmp)
        return {'msg': "查询成功", "data": diskArr, 'status': 1}

    def umountPartition(self, args):
        fstabFileOld = open("/etc/fstab")
        fstabNew = ''
        while 1:
            line = fstabFileOld.readline()
            if(not line):
                break
            if(not line == '\n'):
                if(not args.partition in line):
                    fstabNew = fstabNew + line
        fstabFileOld.close()
        with open("/etc/fstab", 'w') as f:
            f.write(fstabNew)
        os.popen("umount -v " + args.partition)
        if(not args.partition in os.popen("df -h").read()):
            return {'msg': '成功卸载分区[' + args.partition + ']！', 'status': 1}
        else:
            return {'msg': "出现了一个错误，卸载失败！", 'status': -1}

    def formatPartition(self, args):
        fileList = os.popen("ls -la " + args.mountPoint).read()
        os.popen('umount ' + args.partition)
        result = os.popen('mkfs -F -t ' + args.filesystem + " " + args.partition).read()
        os.popen("mount " + args.partition + " " + args.mountPoint)
        return {'msg': '格式化完成！', 'data':result, 'status': 1}

    def mountNewDisk(self, args):
        if(not args.disk.split("/dev/")[1] in os.popen("ls /dev").read()):
            return {'msg': '不存在指定磁盘', 'status': -1}
        if(args.disk in open("/etc/fstab").read()):
            return {'msg': '此磁盘已经被挂载！', 'status': -1}
        if(not args.filesystem in os.popen("cat /proc/filesystems").read()):
            return {'msg': '您的系统不支持文件系统[' + args.filesystem + ']', 'status': -1}
        if(args.disk + '1' in os.popen("fdisk -l " + args.disk).read()):
            return {'msg': '此硬盘已存在分区，不允许执行本操作！！', 'status': -1}
        if(args.mountPoint in os.popen("df -h").read() or args.disk in os.popen("df -h").read()):
            return {'msg': '磁盘或挂载点已被使用！', 'status': -1}
        result = os.popen('echo -e "n\\np\\n\\n\\n\\nw\\n" | fdisk ' + args.disk).read()
        result = result + "\n" + os.popen('mkfs -F -t ' + args.filesystem + ' ' + args.disk + '1').read()
        if(not os.path.exists(args.mountPoint)):
            os.makedirs(args.mountPoint) 
        with open("/etc/fstab", 'a') as f:
            f.write("\n" + args.disk + "1    " + args.mountPoint + "    " + args.filesystem + "    " + args.options + "    0    0")
        os.popen("mount -a")
        time.sleep(1)
        if(args.disk in os.popen("df -h").read()):
            return {'msg': "挂载成功！", "data": result, 'status': 1}
        else:
            return {'msg': "出现了一个错误，挂载失败！", "data": result, 'status': -1}

    def mountPartition(self, args):
        if(not args.partition in os.popen("ls /dev").read()):
            return {'msg': '不存在指定磁盘分区', 'status': -1}
        if(not args.filesystem in os.popen("cat /proc/filesystems").read()):
            return {'msg': '您的系统不支持文件系统[' + args.filesystem + ']', 'status': -1}
        if(args.mountPoint in os.popen("df -h").read() or args.partition in os.popen("df -h").read()):
            return {'msg': '磁盘或挂载点已被使用！', 'status': -1}
        if(not os.path.exists(args.mountPoint)):
            os.makedirs(args.mountPoint) 
        returnMsg = "挂载成功！此磁盘挂载信息已在[/etc/fstab]中存在，优先使用[/etc/fstab]中的挂载信息，忽略输入的挂载信息！"
        if(not args.partition in open("/etc/fstab").read()):
            returnMsg = "挂载成功！"
            with open("/etc/fstab", 'a') as f:
                f.write("\n" + args.partition + "    " + args.mountPoint + "    " + args.filesystem + "    " + args.options + "    0    0")
        os.popen("mount -a")
        time.sleep(1)
        if(args.partition in os.popen("df -h").read()):
            return {'msg': returnMsg, 'status': 1}
        else:
            return {'msg': "出现了一个错误，挂载失败！", 'status': -1}

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
        try:
            while 1:
                line = hostsFile.readline()
                if(not line):
                    break
                if(line != "\n" and line[0] != "#"):
                    hostsArr.append({"ip":line.split(" ", 1)[0].strip(), "domain":line.split(" ", 1)[1].strip(), "original":line.strip("\n")})
        except:
            return {'msg': "hosts文件存在语法错误！请手动修复错误！", "data": hostsArr, 'status': -1}
        return {'msg': "查询成功！", "data": hostsArr, 'status': 1}

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
        try:
            return {'msg': '成功创建任务', "logFileName":str(int(logList[-1].split(".")[0])+1)+".log", 'status': 1}
        except:
            return {'msg': '成功创建任务！获取执行日志文件名失败！', "logFileName":"", 'status': 1}

    def getSitemapGenerationStatus(self, args):
        if(os.path.exists("/www/server/panel/plugin/my_toolbox/static/sitemap.xml")):
            data = open("/www/server/panel/plugin/my_toolbox/static/sitemap.xml").read()
            return {'msg': "生成成功", "data": data, 'status': 1}
        else:
            return {'msg': '扫描中...', 'status': -1}

    def getExecuteResult(self, args):
        if(os.popen("echo $(ps -ef | grep '/www/temp.sh' | grep -v grep | awk '{print $2}')").read() == "\n"):
            if(os.path.exists("/www/server/panel/plugin/my_toolbox/tmp/executeCommand.tmp")):
                executeCommandResult = ""
                try:
                    executeCommandResult = open("/www/server/panel/tmp/" + args.logFileName).read()
                    if(executeCommandResult == ""):
                        msg = "执行成功？但是没有任何返回！请自行检查命令是否运行成功！"
                    else:
                        msg = "执行成功！" 
                except:
                    msg = "执行成功？获取执行结果失败！"
                return {"msg": msg, "result":executeCommandResult, "status":1}
            else:
                return {"msg": "抱歉，找不到运行结果！执行命令失败？", "result":"", "status":2}
        else:
            return {'msg': '正在执行中...', 'status': -1}

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