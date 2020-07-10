import flask
from flask_cors import CORS
import jieba

import os
import sys
sys.path.append( os.getcwd() + "/dealRobot")

from dealIntroduce import dealIntroduce
from dealKnowledge import dealKnowledge
from dealRobot import dealRobot

app = flask.Flask(__name__)
CORS(app)

print('reading the dict...')
jieba.load_userdict(os.getcwd() + '/service/dict.txt')  # 总共有 10W 个名词
print('completed')

def getJson(path):
    file = open( path,'r')
    return file

@app.route('/introduce', methods=['GET','POST'])
def introduceData():
    if flask.request.method == 'GET':
        return 'GET'
    elif flask.request.method == 'POST':
        handler = dealIntroduce()
        words = handler.dealWords()
        return flask.jsonify(words)

@app.route('/knowledge', methods=['GET', 'POST'])
def knowledgeData():
    if flask.request.method == 'GET':
        return 'GET'
    elif flask.request.method == 'POST':
        keyValue = flask.request.get_data().decode()
        print( 'in the knowledge, keyValue: ', keyValue)
        handler = dealKnowledge()
        nodes, links = handler.parseKeyValue(keyValue)
        if len(nodes) == 0:
            return 'failed'
        return flask.jsonify({'nodes':nodes, 'links':links})

@app.route('/robot', methods=['GET', 'POST'])
def robotData():
    if flask.request.method == 'GET':
        return 'GET'
    elif flask.request.method == 'POST':
        input_sentence = flask.request.get_data().decode().replace('\n', '')
        handler = dealRobot()
        word_list = handler.cut_sentence( input_sentence)
        
        return flask.jsonify( word_list)
        
if __name__ == '__main__':
    app.run()