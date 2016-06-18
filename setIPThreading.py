import pymongo
import socket
from format_data import add_one
from urllib.parse import urlparse
from queue import Queue
client = pymongo.MongoClient('nofiht.ml')
db = client.wooyun_
import threading
#----------------------------------------------------------------------
def insertIPByHost(host):
    """"""
    try:
        #add_one(db,i['_id'],'ip_',socket.gethostbyname(host))
        return socket.gethostbyname(host)
    except Exception as e:
        print(e)
que = Queue()
#----------------------------------------------------------------------
def runThread():
    """runThread"""
    global que
    while(not que.empty()):
        i = que.get()
        add_one(db,i['_id'],'_ip',insertIPByHost(urlparse(i['url'])[1]))
        #print(insertIPByHost(urlparse(i['url'])[1]))
 
for i in db.text.find({'_ip':{'$exists':False}},{'text':0,'poc_':0,'friend_url':0,'title':0,'has_form':0}).skip(10):
    que.put(i)
threads = [threading.Thread(target=runThread) for i in range(1,50)]
for i in threads:
    i.start()
    i.join()
