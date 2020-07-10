'''
fileName: dealIntroduce.py
author: zbh
function: 1. get a random web.
          2. get words. 
          3. build wordCloud.
          4. pay attention, the data is not stored!
'''
import json
import random
import os
import sys
sys.path.append( os.getcwd())
sys.path.append( os.getcwd() + "/data")

from data.wordAbout import wordAbout

class dealIntroduce:
    def __init__(self):
        #self.file = open('/Users/vsym/Desktop/Financial_KGQA/data/data.json','r')
        self.words = [] #{ name:'', value: }
        
        self.wordAbout = wordAbout()    # 位于 data 目录下的 wordAbout.py 提供的方法
        self.name, self.about = self.wordAbout.praseHtml(self.wordAbout.getRandomHtml())
    
    def dealWords(self):
        self.words.append({"name":self.name, "value":99})
        for name in self.about:
            self.words.append({"name":name, "value":random.randint(1,100)})
        return self.words

if __name__ == '__main__':
    handler = dealIntroduce()
    #handler.dealWords()
    #print(handler.words)