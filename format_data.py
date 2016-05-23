from bs4 import BeautifulSoup
from urllib.parse import urlparse
#----------------------------------------------------------------------
def is_this_url(netloc, url):
    """你给我一个链接,我检查是不是本域的,如果是本域的,加上http://域名返回给你"""
    if 'http' not in url and 'javascript' not in url: # 差不多就是一个本地的链接了
        return "%s/%s"%(netloc,url)
    if 'http' in url: #如果网站站长很奇葩,把本地的链接都给补成http类型的
        from urllib.parse import urlparse
        if netloc in url:
            return url # 直接return
    else:
        return None # 如果不是本域的,那么返回None

    
#----------------------------------------------------------------------
def shit(text,url):
    """从一堆text里面提取出自己想要的东西"""
    # 1.想要本域的带有=的链接,只取一个
    # 2.如果链接里面有带login admin这种字样的,即为敏感链接
    # 3.对于外部域名,分为两种,一种是单纯的链接(无参数,我们称为友情链接),还有一种是带有参数的链接(我们称为相关链接)
    # 4.如果深度为2,你还得继续爬取的页面
    soup = BeautifulSoup(text,'lxml')
    paramSet = set()
    local_link_list = []
    about_link_set = set()
    friend_url = set()
    keyword = '.action' # 关键词 可以是 = 也可以是action 或者是admin这种(这种适配比较困难...)
    for i in soup.findAll('a'):
        if(i.has_attr('href')):
            href = i['href']
            # print(i['href'])
            if keyword in href: # 检查payload_url
                href_format = is_this_url(url,href) # 对于同域的域名,应该只是除参数的值不相同之外我们才认为不同
                if href_format:
                    local_link_list.append(href_format) #把本域的这个链接加进去,待去重
                # 如果不是本域的怎么搞,不是本域的就只留下 网站首页的链接.后面的路径和参数都不要
                elif 'javascript' not in href: # 如果不是本域的,又是一个长得比较正常的外部链接,那么我们留下网站首页的链接
                    netloc = urlparse(href)[1]
                    if netloc:
                        about_link_set.add(netloc)
            elif 'http://' in href: # 如果存在'http://关键词,那么算为友情链接'
                netloc = urlparse(href)
                if netloc:
                    friend_url.add('%s://%s'%(netloc[0],netloc[1]))
    if local_link_list:
        print(local_link_list[0])
    #print('本地带有keyword的链接:')
    # for i in local_link_list:
        # print(i)
    # print('和本网页有关的链接')
    # for i in about_link_set:
        # print(i)
    # print('本网页的友情链接')
    # for i in friend_url:
        # print(i)
#----------------------------------------------------------------------
def get_http(target):
    """如果里面没有加http 那么加上http"""
    if 'http' not in target:
        return 'http://www.%s'%target
#----------------------------------------------------------------------
def shit_test():
    """shit test"""
    import requests
    for i in open('/tmp/mm').readlines():
        try:
            shit(requests.get(get_http(i.strip('\n'))).text,'http://www.sdu.edu.cn')
        except Exception as e:
            print(e)
if __name__=='__main__':
    shit_test()