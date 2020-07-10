import requests
import re
import json
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/51.0.2704.63 Safari/537.36'}
baseURL = 'https://baike.baidu.com/item/'

def process(value):
    '''
    Args:
        value: 输入要爬取的名词
    
    Return:
        返回value对应页面的标题、描述、三元组
    '''
    url = baseURL + value

    r = requests.get(url, headers=headers)
    
    if( r.status_code != 200):
        print('sorry, It\'s faild. now url is:' + url)
        return 
    
    soup = BeautifulSoup(r.text, 'lxml')
    if not soup.find('dd'):
        return 'failed'

    resDict = {}
    # h1
    entity = soup.find('dd', class_='lemmaWgt-lemmaTitle-title')\
                .find('h1').text.replace('/', '')
    
    # h2 副标题
    tempH2 = soup.find('dd', class_='lemmaWgt-lemmaTitle-title')\
                .find('h2')
    if( tempH2):
        entity += tempH2.text.replace('/', '')
                
    resDict['name'] = entity 
    # 描述
    desc = re.sub( u'\\[.*?\\]|\n', '', 
                    soup.find('div', class_='lemma-summary').text
                )
    resDict['desc'] = desc
    # 三元组
    attrs  = soup.find_all('dt', class_='basicInfo-item name')
    values = soup.find_all('dd', class_='basicInfo-item value')
    if( len(attrs) != len(values)):
        print( value + ' 属性与值的数量不同')
        return 
    for attr, value in zip( attrs, values):
        attr =  attr.text.replace('\xa0','')
        value = [ i 
                  for i in re.split('[,，、\xa0/]', re.sub( u'\\(.*?\\)|（.*?\\）|《|》|<.*?>|\[.*?\]|等|收起|展开|\n', '', value.text))
                  if len(i) != 0
                ]
        if entity in value:
            continue
        resDict[attr] = value
    
    resJson = json.dumps( resDict, ensure_ascii=False)
    return resJson

if __name__ == "__main__":
    print(process('北京大学'))
    pass