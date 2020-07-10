'''
fileName: dealKnowledge.py
author: zbh
function: 1. get a word from input;
          2. return knowledge graph and store this realation words.
'''
import json
import random

from spider import process

# class dealKnowledge:
#     def __init__(self):
#         self.wordAbout = wordAbout()    # 位于 data 目录下的 wordAbout.py 提供的方法
        
#     def parseKeyValue(self, keyValue):
#         name, abouts = self.wordAbout.praseHtml(self.wordAbout.getSpecifiedHtml(keyValue))
#         if( name == '首页'):
#             print('您查找的内容不存在')
#             return [],[]
#         # add in data.json and dict.txt
#         self.wordAbout.updateJsonData( self.wordAbout.dataPath, name, abouts)
#         # return nodes and links
#         return self.dealNodesLinks(name, abouts)

#     def dealNodesLinks(self, name, abouts):
#         nodes = []
#         links = []
#         nodes.append({'name':name, "category": 0})
#         for about in abouts:
#             nodes.append({'name':about, "category": random.randint(1,8)})
#             links.append({'source':name, 'target':about})

#         return nodes, links

class dealKnowledge():
    def __init__(self):
        pass

    def parseKeyValue( self, keyValue):
        f = process( keyValue)
        if f == 'failed':
            return [],[]
        f = json.loads(f)

        nodes = []
        links = []
        nodes.append( {
            'name': f['name'],
            'des':  f['desc'],
            'category': random.randint(0,50 - 1),
            'symbolSize': 80
            })
        for attr in f:
            if attr != 'name' and attr != 'desc':
                for line in f[attr]:
                    # print( attr, line)
                    nodes.append( {
                        'name': line,
                        'category': random.randint(0,49),
                        'symbolSize': random.randint(15,50)
                    })
                    links.append( {
                        'source': f['name'],
                        'name': attr,
                        'target': line
                    })
        return nodes, links

if __name__ == '__main__':
    pass