from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests
from poc_class import *
#----------------------------------------------------------------------
def format_text(text,url):
    """两个参数"""
    """你想找出什么东西来?
    1. 用来向外面抓的链接
    2. 本地用来检测sql注入的链接
    3. 用来检测s2命令执行的链接,只要是能够检测
    4. 敏感链接 比如说带有admin 的链接
    """
    #　那么找出所有的链接，　不管怎样把没有带http的加上http 然后得到一个list
    # 然后只检测上面的几种漏洞
#----------------------------------------------------------------------
def get_things(url_list,netloc):
    """get something you want"""
    poc_classList = [sql_injection,st2_,file_get]
    dic_ = {}
    for i in url_list:
        for j in poc_classList:
            name = j.check(i)
            if name:
                if name in dic_:
                    dic_[name].append(i)
                else:
                    dic_[name] = []
                    dic_[name].append(i)
                #print('待检测->',name,'-->%s'%i)
    #print(dic_)
    return_list = []
    for key in dic_: # 在这个里面的--->那么
        for i in poc_classList:
            if key==i.name:
                return_list.append({key:list(i.list_format(dic_[key]))})
                
    return return_list
            
#----------------------------------------------------------------------
def main(text,netloc):
    """开始"""
    soup = BeautifulSoup(text,'lxml')
    url_list = []
    for i in soup.findAll(href=True):
        url_list.append(i['href'])
    return get_things(url_list,netloc)
    
#----------------------------------------------------------------------
def get_friend_url(text):
    """很单纯的找出friend url"""
    from urllib.parse import urlparse
    url_set = set()
    soup = BeautifulSoup(text,'lxml')
    try:
        for i in soup.findAll(href=True):
            url_set.add(urlparse(i['href'])[1])
    except Exception as e:
        print(e)
    return url_set
        
#----------------------------------------------------------------------
def test_mongo():
    """找友情链接的方法"""
    import pymongo
    client = pymongo.MongoClient('127.0.0.1')
    db = client.edu_cn
    for i in db.text.find().limit(50):
        #main(i['text'],i['url'])
        url_set = get_friend_url(i['text'])
        db.text.update_one({
            'url':i['url'],
            },{
                '$set':
                {
                    'friend_url':list(url_set)
                }
            }
        )
#----------------------------------------------------------------------
def test_mongodb_1():
    """找poc的方法"""
    import pymongo
    client = pymongo.MongoClient('localhost')
    db = client.edu_cn
    for i in db.text.find().limit(100):
        poc_list = main(i['text'],i['url'])
        db.text.update_one({
                    'url':i['url'],
                    },{
                        '$set':
                        {
                            'poc_':list(poc_list)
                        }
                    }  
                           )    
if __name__=='__main__':
    #url = 'http://www.hnfnu.edu.cn/'
    test_mongodb_1()
    #main(requests.get(i.strip('\n')).text,'www.sdu.edu.cn')
    #get_friend_url(requests.get(url).text)
    #test_mongo()
    