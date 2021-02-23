#!/usr/bin/python
# coding: utf-8
# +-------------------------------------------------------------------
# | 我的工具箱
# +-------------------------------------------------------------------
# | Copyright (c) 2015-2099 宝塔软件(https://www.wunote.cn) All rights reserved.
# +-------------------------------------------------------------------
# | Author: 吴先森 <i@mr-wu.top>
# +-------------------------------------------------------------------

import hashlib
import panelTask
import public
import sys
import os
import json
import time
import requests

os.chdir("/www/server/panel")

sys.path.append("class/")
if __name__ != '__main__':
    from BTPanel import cache, session, redirect


def try_a(variable, a):
    try:
        if(variable[a] == ''):
            return 0
        else:
            return 1
    except:
        return 0


class my_toolbox_main:
    __plugin_path = "/www/server/panel/plugin/my_toolbox/"
    __config = None

    def __init__(self):
        pass

    def _check(self, args):
        return True

    def index(self, args):
        return self.get_logs(args)

    # 由于...如果直接扫描的话,扫描时间过长可能会阻塞宝塔进程,所以..只能这么干了
    def start_scan(self, args):
        PID = str(os.popen(
            "echo `ps ax | grep -i '/plugin/my_toolbox/nmap.py' | sed 's/^\([0-9]\{1,\}\).*/\1/g' | head -n 1`").read())
        public.ExecShell('kill -9 '+PID)
        if(args.port_start == ''):
            port_start = '1'
        else:
            port_start = args.port_start
        if(args.port_end == ''):
            port_end = '65535'
        else:
            port_end = args.port_end
        if(os.path.exists("/www/server/panel/plugin/my_toolbox/result.tmp")):
            os.remove('/www/server/panel/plugin/my_toolbox/result.tmp')
        if(os.popen('command -v nmap').read() == ''):
            return {'message': '软件包nmap似乎并未安装！请手动安装nmap后再次使用本功快捷工具', 'status': 0}
        os.popen('python3 /www/server/panel/plugin/my_toolbox/nmap.py ' +
                 port_start+' '+port_end+' '+args.ip+' &')
        return {'message': 'Start port scan', 'status': 1}

    def get_scan_result(self, args):
        #result=os.popen('nmap -p'+args.port_start+'-'+args.port_end+' '+args.ip)
        if(os.path.exists("/www/server/panel/plugin/my_toolbox/result.tmp")):
            file = open("/www/server/panel/plugin/my_toolbox/result.tmp")
            line = file.readline()
            port_list = '<div class="divtable"><table class="table table-hover"><thead><tr><th>端口</th><th>状态</th><th>服务类型（仅参考）</th></tr></thead><tbody>'
            while line:
                if('open' in line):
                    port_list = port_list+'<tr><td>' + \
                        line.split()[0]+'</td><td>'+line.split()[1] + \
                        '</td><td>'+line.split()[2]+'</td></tr>'
                line = file.readline()
            file.close()
            return {'message': port_list+'</tbody></table></div>', 'status': 1}
        else:
            return {'message': 'scaning', 'status': 0}

    def read_hosts(self, args):
        file = open("/etc/hosts")
        hosts = ''
        a = 0
        while 1:
            line = file.readline()
            if not line:
                break
            if(not line == '\n'):
                hosts = hosts+line
        file.close()
        return hosts

    def add_hosts(self, args):
        file = r'/etc/hosts'
        with open(file, 'a') as f:
            f.write('\n')
            f.write(args.ip+' '+args.domain)
        return {'message': '添加hosts成功！', 'status': 1}

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

    def five_star(self, args):
        return 0

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

    def add_link(self, args):
        if(not os.path.exists(args.s_fl)):
            return {'message': '不存在源目录"'+args.s_fl+'"!', 'status': 0}
        if(not os.path.exists(args.m_fl)):
            return {'message': '不存在目标目录"'+args.m_fl+'"!', 'status': 0}
        os.system('ln -s '+args.s_fl+' '+args.m_fl)
        return {'message': '成功创建软链接！', 'status': 1}

    def del_hosts(self, args):
        os.system('rm -rf /etc/hosts.t.bak')
        os.system('cp /etc/hosts /etc/hosts.t.bak')
        file = open("/etc/hosts")
        hosts = ''
        a = 0
        while 1:
            line = file.readline()
            if(not line == '\n'):
                if(not a == int(args.line)):
                    hosts = hosts+line
                a += 1
            if not line:
                break
        file.close()
        with open("/etc/hosts", 'w') as f:
            f.write(hosts)
            f.write('\n')
        return {'message': '删除hosts成功！', 'status': 1}

    def __get_config(self, key=None, force=False):
        if not self.__config or force:
            config_file = self.__plugin_path + 'config.json'
            if not os.path.exists(config_file):
                return None
            f_body = public.ReadFile(config_file)
            if not f_body:
                return None
            self.__config = json.loads(f_body)

        if key:
            if key in self.__config:
                return self.__config[key]
            return None
        return self.__config

    def __set_config(self, key=None, value=None):
        if not self.__config:
            self.__config = {}

        if key:
            self.__config[key] = value

        config_file = self.__plugin_path + 'config.json'
        public.WriteFile(config_file, json.dumps(self.__config))
        return True
