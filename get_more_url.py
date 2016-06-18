#!/usr/bin/env python
#coding:utf-8
"""
  Author:  fang --<fiht@qq.com>
  Purpose: 用来找出相关的url以进行下一步的抓取
  Created: 2016年06月05日
"""
import pymongo
#----------------------------------------------------------------------
def run():
    """找出没有抓取过的友情链接"""
    client = pymongo.MongoClient('nofiht.ml')
    collectionList = ['edu_cn','edu_added']
#    db = client.edu_added
    self_url = set()
    new_url = set()
    for collection in [client.edu_cn,client.edu_added]:
        db = collection
        for i in db.text.find({},{'text':0,"_id":0,'friend_url':0}):
            try:
                self_url.add(i['url'].strip('http://').strip('https://'))
            except Exception as e:
                print(e)
    db = client.edu_added
    for urls in db.text.find({},{'text':0,"_id":0,'url':0}):
        if 'friend_url' in urls.keys():
            for i in urls['friend_url']:
                if i not in self_url:
                    if i not in new_url:
                        print(i)
                        new_url.add(i)

if __name__ == '__main__':
    run()
