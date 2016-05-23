import pymongo
from format_data import *
conn = pymongo.MongoClient('202.194.14.166')
#conn = pymongo.MongoClient('127.0.0.1')
db = conn.edu_cn
for things in db.text.find():
    try:
        shit(things['text'], things['url'])
    except Exception as e:
        print(e)