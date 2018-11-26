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
