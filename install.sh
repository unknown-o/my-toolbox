#!/bin/bash
PATH=/www/server/panel/pyenv/bin:/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

#配置插件安装目录
install_path=/www/server/panel/plugin/my_toolbox

#安装
Install()
{
	
	echo '正在安装...'
    mkdir -p /www/server/panel/plugin/my_toolbox/tmp
	if [ -f "/usr/bin/yum" ] && [ -d "/etc/yum.repos.d" ]; then
		yum install nmap -y
		yum install httpd-tools -y
		echo '如果安装失败，请尝试yum update或手动安装下试试？'
	elif [ -f "/usr/bin/apt" ] && [ -f "/usr/bin/dpkg" ]; then
		apt update
		apt install apache2-utils -y
		apt install nmap -y
		apt install smbclient -y
		echo '如果安装失败，请手动安装下试试？'
	fi
	/www/server/panel/pyenv/bin/pip install bs4
	/www/server/panel/pyenv/bin/pip install requests
	echo '================================================'
	echo '安装完成'
}

#卸载
Uninstall()
{
	rm -rf $install_path
}

#操作判断
if [ "${1}" == 'install' ];then
	Install
elif [ "${1}" == 'uninstall' ];then
	Uninstall
else
	echo 'Error!';
fi
