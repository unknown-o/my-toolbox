#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup
import sys
import datetime
import re

def creat_xml(filename, url):
    header = '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    file = open(filename, 'w', encoding='utf-8')
    file.writelines(header)
    file.close()

    html=requests.get(url).text
    soup = BeautifulSoup(html,"html.parser")
     
     
    href_ = soup.find_all(name='a')
    for each in href_:
        if str(each.get('href'))[:4]=='http':
            times = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S+00:00")
            urls = re.sub(r"&", "&amp;", each.get('href'))
            ment = "  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>\n" % (urls, times)

            file = open(filename, 'a', encoding='utf-8')
            file.writelines(ment)
            file.close()


    last = "</urlset>"
    file = open(filename, 'a', encoding='utf-8')
    file.writelines(last)
    file.close()


if __name__ == '__main__':
    creat_xml("/www/server/panel/plugin/my_toolbox/static/sitemap.xml", sys.argv[1])
