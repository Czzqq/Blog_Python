# 2021/6/10 17:31
#导入相关库
from bs4 import BeautifulSoup   #网页解析 获取数据
import re          #正则表达式
import requests   #制定URL，获取网页数据
import xlwt       #进行excel操作
import os
import sqlite3

#正则表达式，根据规则     ####     点表示任意字符 *表示一次到多次


# 第一步请求归档网页，并得到回应
# 第二步使用正则表达式，对文章发布时间、文章标题、文章url进行爬取、类别由于在归档网页没有，因此进入第三步
# 第三步使用bs4库，在主页进行类别的爬取，由于学习bs4晚于re，因此在爬取第二步内容以后开始穿插着使用bs4库中内容
           #重复以上内容，将整个blog进行遍历其中url是在末尾的/page/x进行迭代
# 第四步保存数据，构想使用文本保存和excel保存两种方式；

#使用三个方法，包括：
#                定义url和请求url获取html字符；
#                BeautifulSoup实例化 ；
#                get_sava_Data获取数据（包括文章标题、时间、url、分类、正文,使用excel文本文档保存或者数据库保存）；


def main():
    my_file = 'blog_data.xls'  # 文件路径
    if os.path.exists(my_file):  # 如果文件存在
        # 删除文件，可使用以下两种方法。
        os.remove(my_file)  # 则删除
        # os.unlink(my_file)
    else:
        print('no such file:%s' % my_file)
    baseurl = "https://www.kingname.info/"        #需要爬取网页的地址，
    get_sava_Data(baseurl)



def askUrl(url):
    header = {
        #模拟浏览器头部信息，向豆瓣服务器发送信息，不然会被禁止访问
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122 Safari / 537.36"
    }
    # 用户代理，表示告诉服务器，我们是什么类型的机器、浏览器（本质上是告诉浏览器，我们可以接收什么水平的文件内容）
    # #print(url)
    # 发出请求，获得回应
    response = requests.get(url,headers=header)
    # 解码
    content = response.content.decode('utf8')
    return content

def get_sava_Data(baseurl):
    # ----------------------------------------------以下为获取数据部分------------------------------------------------
    #因为爬取标题、时间、链接可以在归档的页面完成因此这里分两部分写

    datalists1 = []          #存放标题、发布时间、链接、分类这四个数据；
    datalists2 = []          #存放正文文本、照片链接、代码部分

    for i in range(1,3):                #总共15页因此进行15次遍历
        if i == 1:
            # 爬取文章标题
            content1 = askUrl(baseurl + "archives/")
            Titles = re.findall('<span itemprop="name">(.*?)</span>', content1, re.DOTALL)
            #print(Titles)

            # 爬取文章时间
            Times = re.findall('<time.*?content="(.*?)">.*?</time>', content1, re.DOTALL)
            #print(Times)

            # 爬取文章链接
            Links = re.findall('<a class="post-title-link" href="(.*?)".*?</a>', content1, re.DOTALL)
            #print(Links)

            # 爬取文章分类
            content2 = askUrl(baseurl)
            Kinds = re.findall('<a href.*?<span itemprop="name">(.*?)</span></a>', content2, re.DOTALL)
            #print(Kinds)

            for Title,Time,Link,Kind in zip(Titles,Times,Links,Kinds):
                datalist1 = {
                            "Title":Title,
                            "Time":Time,
                            "Link":baseurl + Link,
                            "Kind":Kind
                }
                datalists1.append(datalist1)
        else:
            content1 = askUrl(baseurl + "archives/page/" + str(i))
            content2 = askUrl(baseurl+"page/" + str(i))
            Titles = re.findall('<span itemprop="name">(.*?)</span>', content1, re.DOTALL) #输出的是一个列表
            #print(Titles)

            # 爬取文章时间
            Times = re.findall('<time.*?content="(.*?)">.*?</time>', content1, re.DOTALL) #输出的是一个列表
            #print(Times)

            # 爬取文章链接
            Links = re.findall('<a class="post-title-link" href="(.*?)".*?</a>', content1, re.DOTALL)#输出的是一个列表
            #print(Links)

            # 爬取文章分类
            Kinds = re.findall('<a href.*?<span itemprop="name">(.*?)</span></a>', content2, re.DOTALL)#输出的是一个列表
            #print(Kinds)
            for Title,Time,Link,Kind in zip(Titles,Times,Links,Kinds):
                datalist1 = {
                            "Title" : Title,         #文章标题
                            "Time" : Time,          #发布时间
                            "Link" : baseurl + Link, #文章url
                            "Kind" : Kind            #文章类别
                }
                datalists1.append(datalist1)
    #爬取文章正文（一页有十个文章）
    for item in datalists1:                  #此方法可以获取列表中字典的某一key的值
        read_Link = item["Link"]
        print("正在爬取url:" + read_Link)
        content3 = askUrl(read_Link)
        soup = BeautifulSoup(content3, 'html.parser')  # 实例化
        bodys = soup.find_all('div', class_="post-body")  # 爬取文章正文的html字符，这里输出为一个对象\
        Codes = soup.find_all('td', class_="code")
        # # 在正文中爬取文本信息
        # # 在正文中爬取图片url
        # # 在正文中爬取code
        # # 创建列表最后存取
        # ###数据还都在对象中，因此这里将其转化为列表
        for body in bodys:
            ps = list(body.find_all('p'))  # 提取所有文本信息为一个对象；
            codes = list(body.find_all('code'))  # 提取所有codes为一个对象；
            imgs = list(body.find_all('img', {"src": True}))  # 提取所有图片为一个对象
        read_ps = []
        read_imgs = []
        read_codes = []
        read_Codes = []
        # 由于以上信息还都
        for p in ps:
            # 因为string只能读取单对便签的纯文本 因此这里选择使用get_text()
            read_ps.append(p.get_text())
        for img in imgs:
            read_imgs.append(img['src'])  # 提取特定属性的文本信息
        for code in codes:
            read_codes.append(code.string)
        for Code in Codes:
            read_Codes.append(Code.get_text())

        datalist2 = {
            "Text": "".join(read_ps),        #文本信息
            "code": "".join(read_codes),         #文本内代码
            "img_Link": " ".join(read_imgs),      #正文图片链接
            "Code": "\n".join(read_Codes)      #代码块信息
        }
        datalists2.append(datalist2)
    #print(datalists1)
    #print(datalists2
#-----------------------------------------------------以下为保存数据部分------------------------------------------------
# 将文章标题、发布时间、url、分类、文章正文、行内代码、图片url、代码块保存到xls文档中
    #创建工作簿
    print("数据爬取并保存完毕")
    sava_data =xlwt.Workbook(encoding="utf-8",style_compression=0) #创建xlwt对象
    #创建工作表
    sheet = sava_data.add_sheet("Data_1",cell_overwrite_ok=True)
    #------------------填充数据--------------------
    #创建行名
    col = ("文章标题","文章发布时间","文章链接","文章分类","文章正文","行内代码信息","图片url","代码块",)
    for i in range(0, 8):
        sheet.write(i, 0, col[i])  #填充列名
        for l in range(0, 20):
            data1 = datalists1[l]
            data2 = datalists2[l]
            for j in range(0, 8):
                if j == 0:
                    sheet.write(j , l + 1, data1.get("Title"))
                elif j == 1:
                    sheet.write(j , l + 1, data1.get("Time"))
                elif j == 2:
                    sheet.write(j , l + 1, data1.get("Link"))
                elif j == 3:
                    sheet.write(j , l + 1, data1.get("Kind"))
                elif j == 4:
                    sheet.write(j , l + 1, data2.get("Text"))
                elif j == 5:
                    sheet.write(j , l + 1, data2.get("code"))
                elif j == 6:
                    sheet.write(j , l + 1, data2.get("img_Link"))
                elif j == 7:
                    sheet.write(j , l + 1, data2.get("Code"))
        sava_data.save("blog_data.xls")
#---------------------------------------使用数据库保存-----------------------------------------
    dbpath = "identifier.sqlite" #设置数据库路径
    sql = '''
            create table blog_data
            (
                id       integer
                    constraint blog_data_pk
                        primary key,
                Title    text default null,
                Time     varchar default null,
                Link     varchar default null,
                Kind     varchar default null,
                Text     text default null,
                code     text default null,
                img_Link text default null,
                Codes    text default null
            )
    '''  # 数据库的sql语言
    conn = sqlite3.connect(dbpath)  # 链接数据库
    cursor = conn.cursor()  # 对数据的操作需要通过cursor来实现，即游标
    cursor.execute(sql)  # 执行sql语句
    conn.commit()  # 提交事务，不然不能做到真正插入数据
    conn.close()  # 用于关闭连接,以防止下面紧接着有另外的 查询会产生冲突。

    conn = sqlite3.connect(dbpath)  # 链接数据库
    cur = conn.cursor()  # 对数据的操作需要通过cursor来实现，即游标
    for i in range(0,20):
        data1 = datalists1[i]
        data2 = datalists2[i]
        sql = "insert into blog_data(id, Title, Time, Link, Kind, Text, code, img_Link, Codes)values(%d, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
                                                                        (i + 1,
                                                                       data1.get("Title"),data1.get("Time"),
                                                                       data1.get("Link"),data1.get("Kind"),
                                                                       data2.get("Text").replace("'"," "),data2.get("code").replace("'"," "),
                                                                       data2.get("img_Link"),data2.get("Code").replace("'"," "))
        #print(sql) #测试语句
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__": #当程序执行时
    main()