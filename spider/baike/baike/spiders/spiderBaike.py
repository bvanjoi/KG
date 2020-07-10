'''
通过索引链的方式爬取百度百科，主要是为了获得结构化数据
'''

import scrapy               # scrapy 爬虫框架
import urllib               # 操作 URL
import os                   # 系统命令
import re                   # 字符串，正则表达式
import json
import time

from bs4 import BeautifulSoup
from scrapy.selector import Selector
from scrapy.cmdline import execute # python代码模拟执行命令行

# json 数据文件,这里就不使用mongoDB了
fJson    = open('dataBaike.json', 'a+')
# 字典
fDict    = open('dictBaike.txt', 'a+')
# 用网址记录爬过的网页
fhadGone = open('hadGone.txt','a+')

class spiderBaike(scrapy.Spider):
    name = 'baike'
    allowed_doamins = ['baike.baidu.com']
    start_urls = ['https://baike.baidu.com/item/金融']

    def __init__(self, keyValue, *args, **kwargs):
        super(spiderBaike, self).__init__(*args, **kwargs)    
        self.start_urls = ['https://baike.baidu.com/item/' + keyValue]


    # 检查是否爬取过
    def hadGone( self, response):
        for lineData in open('hadGone.txt','r'):
            if response.url == lineData.replace('\n',''):
                return False #已经爬取过
        return True #未爬取

    # 处理三元组，并将其 json 格式化
    def dealTriplet(self, response):
        # dict
        resDict = {}
        
        # 实体名称
        #   h1
        entity = ''.join(response.xpath('//h1/text()').getall()).replace('/', '')
        #   h2 如果存在的话
        tempH2 = BeautifulSoup( str(                                        
                            response.xpath('//dd[contains(@class,"lemmaWgt-lemmaTitle-title")]').getall()[0]
                        ), 'lxml').find('h2')
        if tempH2:
            entity += tempH2.text

        resDict['name'] = entity

        # 实体描述
        try:
            desc = re.sub(u'\\[.*?\\]|\n', '', BeautifulSoup(                 
                            str(                                        
                                response.xpath('//div[contains(@class,"lemma-summary")]').getall()[0]
                            ), 'lxml').text)        
            resDict['desc'] = desc
        except:
            pass

        # 实体之间的联系, attrs 为关系，values为其他实体
        attrs  = response.xpath(
            '//dt[contains(@class,"basicInfo-item name")]').getall()
        values = response.xpath(
            '//dd[contains(@class,"basicInfo-item value")]').getall()
        if len(attrs) != len(values):
            print('属性与值的数量不对等')
            return 

        for attr, value in zip( attrs, values):
            attr  = ''.join( Selector( text =  attr).xpath( '//dt//text()').getall()).replace('\xa0','')
            value = [ i
                      for i in re.split('[,，、\n\xa0/]', re.sub( u'\\(.*?\\)|（.*?\\）|《|》|个|等|人|收起|展开|', '', ''.join( Selector( text = value).xpath( '//dd/text()|//dd/a//text()').getall())))
                      if len(i) != 0
                    ]
            if entity in value:
                continue
            resDict[attr] = value
        
        resJson = json.dumps(resDict, ensure_ascii=False)
        fJson.write( resJson + '\n')
        fDict.write( entity  + '\n')
        
        # return resJson

    # 用来获取其他的索引进行爬虫
    def nextHTML(self, response):
        itemName = re.sub('/', '', re.sub('https://baike.baidu.com/item/','', urllib.parse.unquote( response.url)))
        # 下一个 爬虫链接 索引
        items = set(response.xpath(
            '//a[contains(@href, "/item/")]/@href').re(r'/item/[A-Za-z0-9%\u4E00-\u9FA5]+'))
        print( items)
        # print( items)
        
        for item in items:
            new_url = 'https://baike.baidu.com'+urllib.parse.unquote(item)
            new_item_name = re.sub(
                '/', '', re.sub('https://baike.baidu.com/item/', '', new_url))
            yield response.follow( new_url, callback=self.parse)

    def parse( self, response):
        print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        if self.hadGone( response) == False:
            print( '已经爬过：', response.url)
            return 
        print('当前的爬虫页面为:',response.url)
        fhadGone.write(response.url + '\n')
        self.dealTriplet(response)

        # ------------
        # # 把 nextHTML 搬过来了，因为我也不知道为什么调用函数不能运行
        # itemName = re.sub('/', '', re.sub('https://baike.baidu.com/item/','', urllib.parse.unquote( response.url)))
        # # 下一个 爬虫链接 索引
        # items = set(response.xpath(
        #     '//a[contains(@href, "/item/")]/@href').re(r'/item/[A-Za-z0-9%\u4E00-\u9FA5]+'))
        
        # for item in items:
        #     new_url = 'https://baike.baidu.com'+urllib.parse.unquote(item)
        #     new_item_name = re.sub(
        #         '/', '', re.sub('https://baike.baidu.com/item/', '', new_url))
        #     yield response.follow( new_url, callback=self.parse)
        #-------------------------------

if __name__ == "__main__":
    keyValue = '北京大学'
    execute(['scrapy', 'crawl', 'baike',"-a","keyValue=%s"%(keyValue)])