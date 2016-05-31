import requests
from poc_class import *
from bs4 import BeautifulSoup
def main(text,netloc):
    """开始"""
    soup = BeautifulSoup(text,'lxml')
    url_list = []
    for i in soup.findAll(href=True):
        url_list.append(i['href'])
    get_things(url_list,netloc)
    
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
    for key in dic_: # 在这个里面的--->那么
        for i in poc_classList:
            if key==i.name:
                print(key,list(i.list_format(dic_[key])))
                break

# if '__name__'=='__main__':
for i in open('/tmp/mm').readlines():
    try:
        main(requests.get(i.strip('\n')).text,'ss')
    except Exception as e:
        print(e)
    