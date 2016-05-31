import pymongo
from format_data import *
conn = pymongo.MongoClient('202.194.14.166')
#conn = pymongo.MongoClient('127.0.0.1')
db = conn.edu_cn
old_set = set()
friend_set = set()
from urllib.parse import urlparse
for things in db.text.find({},{'url':1,'_id':0,'friend_url':1}):
    try:
        netloc = urlparse(things['url'])[1]
        old_set.add(netloc)
        for i in things['friend_url']:
            friend_set.add(i)
    except Exception as e:
        #print(e,'==')
        pass
        
# for i in old_set:
    # print(i)
f = open('/tmp/targets','w+')
#print('友情链接-->')
for i in friend_set:
    if i not in old_set:
        print(i,file=f)