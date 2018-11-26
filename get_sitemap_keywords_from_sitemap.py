# Author:Vanyo
import requests
from bs4 import BeautifulSoup
import urllib3
import re


headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}
# proxy = {'http': 'http://127.0.0.1:1081', 'https': 'https://127.0.0.1:1081'}


# 获取sitemap的数量
def get_sitemap_num(url,label):
    url = "https://www." + url + "/sitemap.xml"
    list_label = get_label(url,label)
    return(len(list_label))

# 循环总数量，返回index
def round_num(num,url_input):
    for i in range(1,num+1,1):
        print("=================Now start crawling through the NO"+str(i)+" sitemap keywords=================")
        eachsitemap(i,url_input)
        print("=================NO" + str(i) + " sitemap keywords has been crawled=================")

# 写入数据
def write_in(keyword,url_input):
    with open(url_input+".txt","a+",encoding="utf-8") as f:
        f.write(keyword)

# 传入一个列表，并对其中的url进行刷选，得到keywords
def keyword(list_label,url_input):
    for i in list_label:
        url = str(i.string)
        keyword = re.sub(r'https:\/\/www\.'+url_input+'\/.*\/', '', url)
        keyword = re.sub(r'\.html', '', keyword)
        # keyword = re.sub(r'_', ' ', keyword)
        # keyword = re.sub(r'\/', '', keyword)
        keyword = re.sub(r'-', ' ', keyword)
        # keyword = re.sub(r'\d+', '', keyword)
        write_in(keyword+"\n",url_input)
        print("A keyword has been written...")

# url与index字符串拼接，生成新的url地址
def eachsitemap(num,url):
    url_sitemap = "https://www."+url+"/sitemap"+str(num)+".xml"
    list_label = get_label(url_sitemap,"loc")
    keyword(list_label,url)

# 爬取label标签
def get_label(url,label):
    urllib3.disable_warnings()
    res = requests.get(url,headers=headers,verify=False)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text,"html.parser")
    list_label = soup.find_all(label)
    return list_label

url_input = input("input domin as you want crawl, like --> baidu.com:")
sitemap_num = get_sitemap_num(url_input,"loc")
print("there has "+str(sitemap_num)+" sitemap pages")
round_num(sitemap_num,url_input)


