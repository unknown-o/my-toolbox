#!/bin/bash
PATH=/www/server/panel/pyenv/bin:/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

#配置插件安装目录
install_path=/www/server/panel/plugin/my_toolbox

#安装
Install()
{
	
	echo '正在安装...'
	#==================================================================
	#依赖安装开始
	if [ -f "/usr/bin/yum" ] && [ -d "/etc/yum.repos.d" ]; then
		#判断是否存在Python3
		if [ ! -f "/www/server/panel/pyenv/bin/python" ];then
			if ! [ -x "$(command -v python3)" ]; then
				yum install python3 -y
				pip3 install bs4
				pip3 install requests
				echo '安装Python3！成功'
			fi
		else
			/www/server/panel/pyenv/bin/pip install bs4
			/www/server/panel/pyenv/bin/pip install requests
			echo '使用宝塔Python3版本，无需安装Python3！'
		fi
		
		#安装nmap
		if ! [ -x "$(command -v nmap)" ]; then
			yum install nmap -y
		fi
		
		echo '如果安装失败，请尝试yum update或手动安装下试试？'
	elif [ -f "/usr/bin/apt-get" ] && [ -f "/usr/bin/dpkg" ]; then
		if [ ! -f "/www/server/panel/pyenv/bin/python" ];then
			if ! [ -x "$(command -v python3)" ]; then
				apt-get install python3 -y
				pip3 install bs4
				pip3 install requests
				echo '安装Python3！成功'
			fi
		else
			/www/server/panel/pyenv/bin/pip install bs4
			/www/server/panel/pyenv/bin/pip install requests
			echo '使用宝塔Python3版本，无需安装Python3！'
		fi
		apt-get update
		
		#安装nmap
		if ! [ -x "$(command -v nmap)" ]; then
			apt-get install nmap -y
		fi
		echo '如果安装失败，请手动安装下试试？'
	fi

	#依赖安装结束
	#==================================================================

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
