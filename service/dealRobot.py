import jieba
import os
import json
import re
import random

import synonyms

from spider import process

import sys
sys.path.append( os.getcwd() + "/neo4j/")

from toneo4j import toNeo4j

class dealRobot:
    def __init__(self):
        self.stopword_list = [k.strip() for k in open( os.getcwd() + '/service/stopwords.txt', encoding='utf-8') if k.strip() != '']
        self.res = {}
        self.to = toNeo4j('')
        
    def cut_sentence( self, sentence):
        self.res['origin'] = sentence

        self.res['cut'] = jieba.lcut( sentence)
        # self.res['cut_for_search'] = " ".join(jieba.cut_for_search( sentence))
        
        self.res['stopwords_cut'] = sorted([ i for i in jieba.cut( sentence) if i not in self.stopword_list], key = lambda i:len(i),reverse=True)
        # self.res['stopwords_cut_for_search'] = [ i for i in jieba.cut_for_search( sentence) if i not in self.stopword_list]
        
        self.get_information( self.res['stopwords_cut'])
        print( self.res)
        return self.res 

    def get_information( self, lists):
        count = 0
        info = []
        for noun in lists:
            if count >= 2:
                break 
            temp = process(noun)
            if temp == 'failed':
                continue
            count += 1
            temp = json.loads(temp)
            info.append( temp)
            # 将名词的关系导入到 neo4j 中
            for attribute in temp:
                if attribute == 'name':
                    self.to.createNode( 'main', temp['name'], temp['desc'])
                elif attribute == 'desc':
                    pass
                else:
                    for otherNode in temp[attribute]:
                        self.to.createNode( 'other', otherNode, '')
                        self.to.createRealation( temp['name'], re.sub( u'/|\*|\?|\.', '',attribute), otherNode)
        
        self.res['graph'] = info
        self.get_graph(info)
        if len(self.res['graph']) > 1:
            self.get_relation()

    def get_graph( self, info):
        if len(info) == 0:
            return 
        f = info[0]
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

        self.res['describe'] = self.res['graph'][0]['desc']
        self.res['show_cut'] = list(self.res['stopwords_cut'][0])
        self.res['nodes'] = nodes
        self.res['links'] = links

    def get_relation(self):
        name0 = self.res['graph'][0]['name']
        name1 = self.res['graph'][1]['name']
        print( 'name0:', name0)
        print( "name1:", name1)
        nodes = []
        links = []
        desc = ""

        next_flag = True
        # 如果两个一个为节点，一个为关系
        
        m0 = self.to.g.run( "match (n) where n.name = '%s' return n"%(name0)).data()
        m1 = self.to.g.run( "match (n) where n.name = '%s' return n"%(name1)).data()
        if len(m0):# 如果 name0 是节点名，name1 为关系名
            nodes, links, relation_score = self.get_relation_single_node( name0, name1)
            if relation_score > 0.9:
                next_flag = False
        if next_flag and len( m1) > 0: # 如果 name1 是节点名，name0 为关系名 
            nodes, links, relation_score = self.get_relation_single_node( name1, name0)
            if relation_score > 0.9:
                next_flag = False            
        if next_flag: # 如果两个均为节点
            # r1 与 r2 分别为 name0 -> name1, name1 -> name0 两个方向的寻找，查找二者是否有关系
            r1 = self.to.g.run( "match p=(n{name:'%s'})-[*]->(m{name:'%s'}) return p"%(name0, name1)).data()
            r2 = self.to.g.run( "match p=(n{name:'%s'})-[*]->(m{name:'%s'}) return p"%(name1, name0)).data()

            if len(r1) != 0:
                nodes, links = self.get_relation_between_nodes(r1,r2)
            elif len(r2) != 0:
                nodes, links = self.get_relation_between_nodes(r2,r1)
            else: # 如果二者无关， 则使用 get_relation 的结果
                return 
        
        for i in range(len(links)):
            desc += links[i]['source'] + links[i]['name']
            if i == len(links) - 1:
                desc += links[i]['target']
            
        self.res['describe'] = desc
        self.res['show_cut'] = self.res['stopwords_cut']
        self.res['nodes'] = nodes
        self.res['links'] = links
    
    def get_relation_between_nodes(self, r1, r2):
        ''' 如果 m0, m1 都是节点，并且 m0 和 m1 有关系
        ''' 
        nodes = []
        links = []
        for i in range( len(r1[0]['p'].relationships)):
            start_node_name = r1[0]['p'].relationships[i].start_node['name'].encode('unicode_escape').decode('unicode_escape')
            end_node_name = r1[0]['p'].relationships[i].end_node['name'].encode('unicode_escape').decode('unicode_escape')
            if start_node_name in [ i['name'] for i in nodes]:
                continue 
            nodes.append( {
                'name': start_node_name,
                'category': random.randint(0,49),
                'symbolSize': random.randint(15,50)
            })
            if i == len(r1[0]['p'].relationships) - 1 and end_node_name not in [ i['name'] for i in nodes]:
                nodes.append( {
                'name': end_node_name,
                'category': random.randint(0,49),
                'symbolSize': random.randint(15,50)
            })
        for relationship in r1[0]['p'].relationships:
            start_node_name = relationship.start_node['name'].encode('unicode_escape').decode('unicode_escape')
            end_node_name = relationship.end_node['name'].encode('unicode_escape').decode('unicode_escape')
            r = str(type( relationship)).split('\'')[1].split('.')[-1]
            links.append( {
                'source': start_node_name,
                'name': r,
                'target': end_node_name
            })

        return nodes, links

    def get_relation_single_node(self, node_name, relation_name):
        node = self.to.g.run( "match p=(n{name:'%s'})-[]->(m{}) return p"%(node_name)).data()
        nodes = []
        links = []
        max_relation_score = 0
        relation_name = re.sub( u'\\(.*?\\)|（.*?\\）|《|》|<.*?>|\[.*?\]|\n', '', relation_name)   # 正则去除括号等
        for relationship in node:
            relationship = relationship['p'].relationships[0]
            r = str(type( relationship)).split('\'')[1].split('.')[-1]
            now_score = synonyms.compare(relation_name, r, seg=False)
            print( relation_name, r, 'relation_score:', now_score)
            start_node_name = relationship.start_node['name'].encode('unicode_escape').decode('unicode_escape')
            end_node_name   = relationship.end_node['name'].encode('unicode_escape').decode('unicode_escape')
            if now_score > max_relation_score:
                max_relation_score = now_score
                nodes = [{
                        'name': start_node_name,
                        'category': random.randint(0,49),
                        'symbolSize': random.randint(15,50)
                    },
                    {
                        'name': end_node_name,
                        'category': random.randint(0,49),
                        'symbolSize': random.randint(15,50)
                    }]
                links = [{
                   'source': start_node_name,
                    'name': r,
                    'target': end_node_name 
                }]


        return nodes, links, max_relation_score

if __name__ == "__main__":
    d = dealRobot()
    d.cut_sentence('李彦宏是哪里人')

    # d.cut_sentence('李克强与北京大学有什么关系')
    # test = d.to.g.run( "match (n) where n.name = '%s' return n"%('李克强')).data()
    # for i in test:
    #     print( i.decode('utf-8'))
    # print(d.to.g.run( "match (n) where n.name = '%s' return n"%('北京大学')).data())
    # print(d.to.g.run( "match p= (n{name:'%s'})-[*]->(m{name:'%s'}) return p"%('', '北京大学')).data())