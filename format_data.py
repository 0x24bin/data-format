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
def get_poc(url_list,netloc):
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
def main(url_list,netloc):
    """开始"""
    url_list = []
    for i in url_list:
        url_list.append(i['href'])
    return get_things(url_list,netloc)
    
#----------------------------------------------------------------------
def get_friend_url(url_list):
    """很单纯的找出friend url"""
    from urllib.parse import urlparse
    url_set = set()
    try:
        for i in url_list:
            url_set.add(urlparse(i)[1])
    except Exception as e:
        print(e)
    return url_set
   
   
def get_form():
    import pymongo
    client = pymongo.MongoClient('127.0.0.1')
    db = client.edu_cn    
    for i in db.text.find().limit(50):
        sou
        if('method="post"' in i['text']):
            db.text.update_one({
                        'url':i['url'],
                        },{
                            '$set':
                            {
                                'has_form':1
                            }
                        })

#----------------------------------------------------------------------
def add_one(db,_id,name,data):
    """向mongo里面加入一个列"""
    db.text.update_one({'_id':_id,},{'$set':{name:data}})
#----------------------------------------------------------------------
def test_mongodb_1():
    """找poc的方法"""
    import pymongo
    from bs4 import BeautifulSoup
    client = pymongo.MongoClient('nofiht.ml')
    db = client.top_chinaz_100w
    count = 0
    #while db.text.find_one({'HasFormat':{'$exists':False}}):
    for i in db.text.find({'HasFormat':{'$exists':False}}):
        url_list = []
        soup = BeautifulSoup(i['text'],'lxml')
        for link in soup.findAll(href=True):
            url_list.append(link['href'])
        poc_list = get_poc(url_list,i['url'])
        friend_url = get_friend_url(url_list)
        if 'phpMyAdmin' in i['text']:
            add_one(db,i['_id'],'phpMyAdmin',1)
        if 'Index of' in i['text']:
            add_one(db, i['url'],'HasIndex',1)
        add_one(db,i['_id'],'poc_',list(poc_list))
        add_one(db,i['_id'],'HasFormat',1)
        add_one(db,i['_id'],'friend_url',list(friend_url))
        count+=1
        if not count%100:
            print('处理了%d条数据'%count)
if __name__=='__main__':
    #url = 'http://www.hnfnu.edu.cn/'
    test_mongodb_1()
    #import pymongo
    # client = pymongo.MongoClient('nofiht.ml')
    # db = client.IPS_BIG
    # for i in db.text.find({},{'HasFrmate':0}).limit(10):
        # print(i)
    #get_form()
    #main(requests.get(i.strip('\n')).text,'www.sdu.edu.cn')
    #get_friend_url(requests.get(url).text)
    #test_mongo()
    