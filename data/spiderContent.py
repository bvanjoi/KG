import requests
from bs4 import BeautifulSoup
import pprint
import json

# 去除首页中诸如 [1] 之类的索引
def dealHeadWords( text):
    res = ''
    isIn = 0
    for i in text:
        if i == '[':
            isIn = 1
        elif i == ']' and isIn == 1:
            isIn = 0
        elif isIn == 0:
            res += i
    return res

class financialSpider:
    def __init__(self):
        self.wikiURL = 'https://wiki.mbalib.com/wiki/'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/51.0.2704.63 Safari/537.36'}
        self.hadGone = []       # 用来保存已经爬取过的网页

    def dealEscapeCharacter(self, s):
        return s.replace('&amp;','&').replace("&lt;",'>').replace("&gt;",'>').replace("&quot;", '"').replace("&apos;", "'")

    # 用来爬取 分类索引 首页所有的索引
    # def get_home_html(self):   
    #     url =  "https://wiki.mbalib.com/wiki/MBA%E6%99%BA%E5%BA%93%E7%99%BE%E7%A7%91:%E5%88%86%E7%B1%BB%E7%B4%A2%E5%BC%95"
    #     r = requests.get(url, headers = self.headers)
    #     if( r.status_code != 200):
    #         raise Exception('sorry, It\'s faild. now url is:', url)
    #     soup = BeautifulSoup(r.text, 'lxml')                # 第二个参数是解析器，不知道为什么，此处不能使用'html.parser'
    #     # 为直观一点，多写了点 find
    #     indexs = soup.find("div", id = "globalWrapper")\
    #                 .find("div", id = "column-content")\
    #                 .find("div", id = "content")\
    #                 .find("div", id = "bodyContent")\
    #                 .find("div", style = "margin:10px 5px;border:1px solid #B2DE90;background-color:#E3F0D8;padding:5px")\
    #                 .find("div", style = "padding:0 5px;")\
    #                 .find_all('a')
    #     # 爬下所需的链接
    #     #res = []
    #     for index in indexs:
    #         if len(str(index.get('title'))) > 0:
    #             self.get_classify_html(self.wikiURL + self.dealEscapeCharacter(index.get('href')))

    #     return

    # 用于获取某个 分类页面 下的索引
    # def get_classify_html(self, url):
    #     if url in self.hadGone:
    #         print('Had Gone : ', url)
    #         return
    #     print('now :', url)
    #     self.hadGone.append(url)
    #     r = requests.get(url, headers=self.headers)
    #     if( r.status_code != 200):
    #         raise Exception('sorry, It\'s faild. now url is:', url)
    #     soup = BeautifulSoup(r.text, 'lxml')
    #     # 依旧为了直观
    #     indexs = soup.find("div", id = "globalWrapper")\
    #                 .find("div", id = "column-content")\
    #                 .find("div", id = "content")\
    #                 .find("div", id = "bodyContent")\
    #                 .find_all("a")

    #     for index in indexs:
    #         if index.get('href') and 'until' not in index.get('href'):
    #             href = self.wikiURL + self.deal_EscapeCharacter(index.get('href'))
    #             if 'Category' in (str(index.get('title'))):
    #                 self.get_classify_html(href)
    #             elif index.get('title') and index.get('href') != '#':
    #                 print('testOnlytestOnlytestOnlytestOnly')
    #     return
    

    def parseHtml(self, url):
        if url in self.hadGone:
            print('Had Gone : ', url)
            return
        print('now :', url)
        self.hadGone.append(url)

        r = requests.get(url, headers=self.headers)
        
        if( r.status_code != 200):
            raise Exception('sorry, It\'s faild. now url is:', url)
        soup = BeautifulSoup(r.text, 'lxml')

        # 依旧为了直观
        indexs = soup.find("div", id="globalWrapper") \
                    .find("div", id="column-content") \
                    .find("div", id="content")
        
        name = indexs.find('h1', class_ = 'firstHeading').string
        print('name:',name)                    # 大标题，即专业名词

        indexs = indexs.find("div", id = 'bodyContent')

        AllContent = []
        SubContent = []

        for child in indexs.children:
            if child.name == 'table':             # 省略索引部分
                continue
            elif child.name == 'div':             # 此处找的是小标题
                childChild = child.find('h2')
                if childChild:
                    if len(SubContent) > 0:
                        AllContent.append(SubContent)
                    SubContent = []

                    SubContent.append(dealHeadWords( childChild.text).strip())
                else:
                    childChild = child.find('h3')
                    if childChild:
                        SubContent.append(childChild.text.strip())
            elif child.name == 'p':             # 小标题下的内容(文本部分）
                if len(SubContent) > 1:
                    SubContent[-1] += child.text
                else:
                    SubContent.append(child.text.strip())
                # 向 SubContent 中添加小标题下的图片
                childChild = child.find('img')
                if childChild:  
                    SubContent[-1] += '<img src="' + self.wikiURL + str(childChild['src']) + '">'   # 图片解析成 html 支持的格式
            elif child.name == 'dl':        # 'dl' 为小标题内部再分级
                childChild = child.find('dt')
                if childChild:
                    SubContent.append(childChild.text)
            elif child.name == 'ul':        # 'ul' 为'相关条目' 下内容的存储方式
                childChild = child.find_all('li')
                for index in childChild:
                    SubContent.append(index.text.strip())

        if len(SubContent) > 0:
            AllContent.append(SubContent)
            
        return AllContent
        # for i in AllContent:
        #     for j in range(0, len(i)):
        #         if j == 0:
        #             print('当前条目对应的list长度为:', len(i))
        #         print(i[j])
        #     print()

if __name__ == '__main__':
    handler = financialSpider()
    #href = handler.get_home_html()
    #handler.get_classify_html('https://wiki.mbalib.com/wiki/Category:%E9%87%91%E8%9E%8D%E7%90%86%E8%AE%BA')
    url = 'https://wiki.mbalib.com/wiki/买点'
    handler.parseHtml(url)