'''
fileName: updateJson.py
author: zbh
function: 1. read data.json;
          2. update data.json
update policy: insert new entites and realtion words.
'''

import json
import os

class updateJson:
    def __init__(self):
        self.dictPath = os.getcwd() + '/data/dict.txt'
        file = open(self.dictPath, 'r')
        self.words = set([])
        for lineData in file:
            self.words.add(str(lineData).replace('\n',''))
        #print(self.words)
        return 
        
    def checkJson(self, path, name):
        if( name in self.words):
            print('Had Gone')
            return False
        open(self.dictPath, 'a').write(str(name) + '\n')
        return True
        #以上代码是通过创建 set  文件检查是否重复
        #以下代码是通过读取 json 文件检查是否重复
        # file = open(path, 'r')
        # for lineData in file:
        #     # 存在巨大的性能问题
        #     lineDataJson = json.loads(lineData)
        #     if( lineDataJson['name'] == name):
        #         print('Had Gone')
        #         return False
        # return True         # It means need insert
    
    def insertJson(self, path, name, about):
        if(self.checkJson(path,name) == True):
            storeData = {"name":name, "about":about}
            file = open(path,'a')
            file.write(str(storeData).replace('\'','\"')+'\n')
            file.close()
            print(str(storeData).replace('\'','\"'))
        return 
    
        
if __name__ == '__main__':
    # handler = updateJson()
    pass