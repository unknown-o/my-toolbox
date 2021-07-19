#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author:Mr. Wu (i@mr-wu.top)
# 2021/7/19
import requests
import re
from bs4 import BeautifulSoup
import sys
import datetime
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import ElementTree
from urllib.parse import urlparse
from xml.dom import minidom
import xml.dom.minidom

def getAllLink(urlArr, url, currentLevel, maxLevel):
    if(not (urlparse(url).path.split(".")[-1] == urlparse(url).path or urlparse(url).path.split(".")[-1].lower() in ["html","php","jsp","htm","asp"])):
        print("不处理链接 " + url)
        return urlArr
    print("正在处理链接 " + url)
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.70',
        }
        response = requests.get(url, headers, timeout=(60,60))
        htmlBody = response.text
        if(response.status_code == 200):
            urlArr.append(url)
            if(currentLevel <= maxLevel):
                soup = BeautifulSoup(htmlBody, "html.parser")
                for link in soup.find_all('a'):
                    if(not link.get('href') == None):
                        domain = urlparse(url).netloc
                        linkTemp = link.get('href').split("?")[0].split("#")[0]
                        if(not "http" in link.get('href')):
                            if(linkTemp[0] == "/"):
                                linkTemp = urlparse(url).scheme + "://" + domain + linkTemp
                            else:
                                if(url[-1] == "/"):
                                    linkTemp = url + linkTemp
                                else:
                                    linkTemp = url + "/" + linkTemp
                        if(not linkTemp in urlArr):
                            if(domain in linkTemp):
                                urlArr = getAllLink(urlArr, linkTemp, currentLevel+1, maxLevel)
    except:
        pass
    return urlArr

urlArr = getAllLink([], sys.argv[1], 1, int(sys.argv[2]))
print("===遍历完成，正在生成sitemap===")
root = Element('urlset',xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
for url in urlArr:
    print("正在写入文件 " + url)
    urlBody = SubElement(root, 'url')
    SubElement(urlBody, 'loc').text = url
    SubElement(urlBody, 'lastmod').text = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S+00:00")
    SubElement(urlBody, 'changefreq').text = "weekly"
    SubElement(urlBody, 'priority').text = "0.8"
print("正在格式化XML文档中...")
ElementTree(root).write('/www/server/panel/plugin/my_toolbox/static/sitemap.xml', encoding = 'utf-8')
result = xml.dom.minidom.parse("/www/server/panel/plugin/my_toolbox/static/sitemap.xml")
with open('/www/server/panel/plugin/my_toolbox/static/sitemap.xml', 'w') as f:
    f.write(result.toprettyxml())
print("处理成功！")