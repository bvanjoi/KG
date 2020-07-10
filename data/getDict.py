import json
import os
import re

file_json = open( os.getcwd() + '/data/data.json', 'r')
dict_text = open( os.getcwd() + '/data/dict.txt', 'w+')

def getDict():
    count = 0
    hadIn = []
    for line in file_json:
        try:
            line = json.loads( line)
            noun = re.sub( u'\(.*?\)|（.*?）|《|》', '', line['name'])
            if noun not in hadIn:
                count += 1 
                hadIn.append( noun)
                dict_text.write( noun + '\n')

            for name in line['about']:
                noun = re.sub( u'\(.*?\)|（.*?）|《|》', '', name)
                if noun not in hadIn:
                    count += 1
                    hadIn.append( noun)
                    dict_text.write( noun + '\n')
        except :
            print(line)
    print( 'all count = ', count)            
    
    return 
                
if __name__ == "__main__":
    getDict()