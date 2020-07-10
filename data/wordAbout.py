'''
fileName: wordAbout.py
author: zbh
function: 1. get a encyclopedia web random by '随便看看'.
          2. and then get all relation entities about this.
          3. finally update data json.
'''

import requests
from bs4 import BeautifulSoup

from updateJson import updateJson
import time
import random
import os

class wordAbout:
    def __init__(self):
        self.wikiURL = 'https://wiki.mbalib.com/wiki/'
        self.randomURL = 'https://wiki.mbalib.com/wiki/Special:Random'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/51.0.2704.63 Safari/537.36'}
        self.dataPath = os.getcwd() + '/data/data.json'
        self.updateJson = updateJson()

    def getRandomHtml(self):  # return a random html
        r = requests.get( self.randomURL, headers=self.headers)
        r.encoding = 'UTF-8'
        if( r.status_code != 200):
            raise Exception('sorry, It\'s faild. now url is:', self.randomURL)
            
        return r.text

    def getSpecifiedHtml(self, keyValue):
        specifiedURL = self.wikiURL + keyValue
        print(specifiedURL)
        r = requests.get( specifiedURL, headers=self.headers)
        r.encoding = 'UTF-8'
        if( r.status_code != 200):
            raise Exception('sorry, It\'s faild. now url is:', specifiedURL)
            
        return r.text

    def updateJsonData(self, path, name, about):
        self.updateJson.insertJson(path, name, about)
        return 

    def praseHtml(self, html): # return list which has all realtion entities
        soup = BeautifulSoup( html, 'lxml')

        # get entity name in this page.
        indexs = soup.find("div",id="content")
        name = indexs.find('h1', class_='firstHeading').string
        
        print( '名词：',name)

        indexs = indexs.find('div',id="bodyContent")
    
        about = []
            
        for index in indexs.find_all('a'):
            if index.get('href') and index.get('href')[0:5] == '/wiki': # It means the entites only in mbalib website
                temp = str(index.get('title'))
                if temp == name or len(temp) == 0 or temp.startswith('MBA智库百科:') or temp.startswith('Category:'):   #解决重复、空、非有效索引等内容
                    continue
                elif index.get('class'):    #解决诸如 image, internal 等内容
                    continue
                else:
                    about.append(temp)
        
        about = list(set(about))

        return name, about


if __name__ == '__main__':
    handler = wordAbout()
    while(1):
       time.sleep( random.randint(5,15))
       print('this is a random html: ')
       name, about = handler.praseHtml(handler.getRandomHtml())
       handler.updateJsonData(handler.dataPath, name, about)