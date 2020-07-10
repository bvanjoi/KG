import os
import json
from py2neo import Graph, Node, Relationship
import re

class toNeo4j():
    '''将数据导入到 neo4j 中
    '''
    def __init__(self, path):
        # neo4j的配置文件中 dbms.security.auth_enabled 从true 修改为false.
        self.g = Graph(
            host="127.0.0.1",
            http_port=7474,
            username="kg", 
            password="123"
        )
        # self.f = open( os.getcwd() + path, 'r')
    
    def isExistNode(self, node_name):
        '''用 name 作为 key 值，防止重复
        '''
        try:
            res = self.g.run('MATCH (n) where n.name = \'%s\' return n'%(node_name)).data()
            return len(res) != 0
        except:
            print( 'error: check node | ', 'node_name:', node_name)
            

    def createNode(self, label, node_name, node_desc):
        '''创建节点并导入到 neo4j 中
        '''
        if( self.isExistNode( node_name)):  # 当前 name 为 node_name 的节点已经存在时，则更新
            if label == 'main':
                try:
                    self.g.run("MATCH (n{name:\'%s\'}) set n.label ='%s', n.desc='%s'  RETURN n"%(node_name,label,node_desc))
                    print( 'success: update main node | node_name:', node_name)
                except:
                    print( 'error: update node | ', 'node_name:', node_name)
            else:
                try:
                    self.g.run("MATCH (n{name:\'%s\'}) set n.name ='%s' RETURN n"%( node_name, node_name))
                    print( 'success: update other node | node_name:', node_name)
                except:
                    print( 'error: update node | ', 'node_name:', node_name)
        else:
            if label == 'main':
                node = Node(
                    label=label,
                    name=node_name,
                    desc=node_desc
                    )
            else:
                node = Node(
                    label=label,
                    name=node_name
                    )
            self.g.create(node)
            print( 'success: create %s node | node_name:' % label, node_name)


    def isExistRelation( self, begin_name, relation, end_name):
        '''检查是否存在该关系
        '''
        try:
            res = self.g.run("match p = (n)-[%s]->(m) where n.name ='%s' and m.name='%s' return p"%( relation,begin_name, end_name)).data()
            return len(res) != 0
        except:
            print( 'error: check realation | ', 'begin_name:', begin_name, 'relation:', relation, 'end_name:', end_name)

    def createRealation( self, begin_name, relation, end_name):
        if( self.isExistRelation( begin_name, relation, end_name)):
            pass
        else:
            try:
                query = "match (p),(q) where p.name='%s' and q.name='%s' create (p)-[r:%s]->(q)" % ( begin_name, end_name, relation)
                print( 'success_relation:', 'begin_name:', begin_name, 'relation:', relation, 'end_name:', end_name)
                self.g.run(query)
            except:
                print( 'error: create realation | ', 'begin_name:', begin_name, 'relation:', relation, 'end_name:', end_name)

    def process(self):
        # count = 0
        for line in self.f:
            line = json.loads(line)
            for attribute in line:
                if attribute == 'name':
                    self.createNode( 'main', line['name'], line['desc'])
                elif attribute == 'desc':
                    pass
                else:
                    for otherNode in line[attribute]:
                        self.createNode( 'other', otherNode, '')
                        self.createRealation( line['name'], re.sub( u'/|\*|\?|\.', '',attribute), otherNode)
            print( 'success:', line['name'], ' count: ',count)
            # count+=1
        
if __name__ == "__main__":
    path = '/neo4j/data/newDataBaike.json'
    to = toNeo4j(path)
    to.process()