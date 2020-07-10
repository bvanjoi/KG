import json
import os

class clearBaikeData:
    '''清洗爬虫数据中的无效数据
    '''
    def __init__(self):
        self.fileJson = open( os.getcwd() + '/clear/dataBaike.json', 'r')
        self.newFileJson = open( os.getcwd() + '/clear/newDataBaike.json', 'w+')
        
    def needClear( self, line):
        lineJson = json.loads( line)
        if( 'desc' not in lineJson or lineJson['desc'] == ''): 
            return True
        return False

    def clearJson( self):
        for line in self.fileJson:
            if( not self.needClear( line)):
                self.newFileJson.write( line)
                
if __name__ == "__main__":
    handle = clearBaikeData()
    handle.clearJson()