# 做黑帽SEO询盘网站的的关键在于域名和关键词，域名权重比较好的（暂时）：be,it,nl,in,而关键词怎么扩展，扩展的精度是一个问题
## 最近在学python爬虫，想着能不能写一个python脚本爬别人网站的关键词，所以需求很简单，就是找到别人网站的sitemap,将他的关键词爬下来
### *1.先写了一个爬取慢的python脚本*
```
# Author:Vanyo
import requests
from bs4 import BeautifulSoup
import os
import urllib3

# 服务器反爬虫机制会判断客户端请求头中的User-Agent是否来源于真实浏览器，所以，我们使用Requests经常会指定UA伪装成浏览器发起请求
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'}


# 用于抓取标签列表，例如想爬取某个url下的所有p标签，则get_html(url,p):
# 会生成一个列表[<p>safg asjfgaj jafhajk</p>,<p>safg asjfgaj jafhajk</p>,...]
def get_html(url,label):
  urllib3.disable_warnings()
  # 爬取到的一个对象，它有很多属性，比如text就是文本信息
  proxy = {'http':'http://127.0.0.1:1081','https':'https://127.0.0.1:1081'}
  res = requests.get(url,headers=headers,verify=False,proxies=proxy)
  # 编码
  res.encoding = "GB2312"
  # 转成源代码
  soup = BeautifulSoup(res.text,"html.parser")
  # 找标签
  list = soup.find_all(label)
  # 返回生成的列表
  return(list)

# 2.抓取这个网址的sitemap.xml页,获取sitemap的条数
def geturl_num(url):
  url = "https://"+url+"/sitemap.xml"
  result = get_html(url,"sitemap")
  # 计算列表长度
  num_list = len(result)
  return(num_list)

# 3.循环sitemap_.xml,
def getsitemap_whole(num,res):
  for i in range(1,num+1,1):
    getsitemap_single(i,res)

# 4.去爬每页里的东西
def getsitemap_single(i,res):
  url = "https://"+res+"/sitemap" + str(i) + ".xml"
  # return url
  result = get_html(url, "loc")
  for r in result:
    single_url = str(r.string)
    result = get_html(single_url, "title")
    title = str(result[0].string)
    # 写入文件
    with open(res+"-keywords.txt","a+",encoding="utf-8") as f:
      f.write(title+"\n")
    print("One keyword has been written")

# 让用户输入要抓取的网址
res = input("input the url address:")
num = geturl_num(res)
print(res+"一共有"+str(num)+"页sitemap,接下来开始爬取关键词：")
getsitemap_whole(num,res)

```
***这个脚本旨在进入每个sitemap网页，找代码中的<title></title>***

**优点**：能直接把keyword从网页中爬出来，不需要进一步筛选

**缺点**：速度慢，需要爬几万次，每个网页都要去获取一次标题

### *2.后又写了一个投机取巧的python脚本*
```
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
```

***这个脚本旨在进入总的sitemap网页，找代码中的每个sitemap的url,从url里筛选出***

**优点**：速度快，只需要爬几个sitemap页面

**缺点**：由于url链接不定，需要对筛选条件进行设置，比如有的url是.html结尾，有的则是以/结尾

