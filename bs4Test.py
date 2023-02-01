# 2021/6/11 13:38

import re
import requests
from bs4 import BeautifulSoup


baseurl = "https://www.kingname.info/2020/10/02/copy-from-ssh/"

#设置请求头
headers = {
        "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
}
#发出请求，获得回应
response = requests.get(baseurl,headers=headers)
#解码
content = response.content.decode('utf8')

bodys = []
Codes = []
soup = BeautifulSoup(content,'html.parser')       #实例化
bodys = soup.find_all('div',class_="post-body")   #爬取文章正文的html字符，这里输出为一个对象\
# print(bodys)
Codes = soup.find_all('td',class_="code")
#在正文中爬取文本信息
#在正文中爬取图片url
#在正文中爬取code
#创建列表最后存取
###数据还都在对象中，因此这里将其转化为列表
for body in bodys:
    ps = list(body.find_all('p'))  # 提取所有文本信息为一个对象；
    codes = list(body.find_all('code'))  # 提取所有codes为一个对象；
    imgs = list(body.find_all('img', {"src": True}))  # 提取所有图片为一个对象
read_ps = []
read_imgs = []
read_codes = []
read_Codes = []
#由于以上信息还都
for p in ps:
    # 因为string只能读取单对便签的纯文本 因此这里选择使用get_text()
    read_ps.append(p.get_text())
print(read_ps)
print("-------------------以上是正文文本信息-------------------")
for img in imgs:
    read_imgs.append(img['src'] ) #提取特定属性的文本信息
print(read_imgs)
print("-------------------以上是图片链接信息-------------------")
for code in codes:
    read_codes.append(code.string)
print(read_codes)
print("-------------------以上是行内代码数据-------------------")
for Code in Codes:
    read_Codes.append(Code.get_text())
print(read_Codes)
print("-------------------以上是代码块数据-------------------")

print("".join(read_ps))
print(" ".join(read_imgs))
print("  ".join(read_codes))
print("\n".join(read_Codes))