########################################################################
class poc(object):
    #----------------------------------------------------------------------
    def __init__(self,name,key_word,expect_word=''):
        """Constructor"""
        self.name = name
        self.key_word = key_word.split(' ')
        self.expect_word = expect_word.split(' ')
    
    #----------------------------------------------------------------------
    def check(self,url):
        """检查一个list里面是否存在关键词"""
        for key_word in self.key_word:
            if key_word in url:
                for i in self.expect_word:
                    if i in url:
                        return None
                return self.name
        return None
    #----------------------------------------------------------------------
    def __hash__(self):
        """return hash of name"""
        return hash(self.name)
    #----------------------------------------------------------------------
    def __str__(self):
        """return the name of poc"""
        return self.name
    #----------------------------------------------------------------------
    def list_format(self,url_list):
        """默认的去重url的方法"""
        # 具体:像s2命令执行的这种漏洞,一个网站只取一个url即可,但是对于sql注入的漏洞,应该要采取更加复杂的去重方法 一个url中如果只要参数不同,那么就应该分别检验
        from urllib.parse import urlparse
        url_set = set()
        return_list = []
        for i in url_list:
            parseResult = urlparse(i)
            netloc = parseResult[1]
            if netloc not in url_set:
                return_list.append(i)
                url_set.add(netloc)
        return return_list
########################################################################
class Sql_injection(poc):
    """主要重写了url去重的规则"""
    #----------------------------------------------------------------------
    def list_format(self,url_list):
        """规则应该是->每个路径下都取一个,比如www.baidu.com/aaa/text?a=1"""
        from urllib.parse import urlparse
        url_set = set()
        return_list = []
        for i in url_list:
            parseResult = urlparse(i)
            netloc = parseResult[1]
            path = parseResult[2]
            if netloc+path not in url_set:
                return_list.append(i)
                url_set.add(netloc+path)
        return return_list
sql_injection = Sql_injection(name='sql_injection',key_word='=',expect_word='http') # 这里加expect_word 有一个想法是 只检测本域的url
st2_ = poc(name='struts2',key_word='.do .action',expect_word='.doc www.do')
file_get = poc(name='任意文件下载',key_word='filename= file=')
login_url = poc(name='敏感链接',key_word='login admin',)
# 现在只添加了三个特征库,需要的话可以添加更多
# 每个类负责检测去重属于自己的类型
test_list = ['/portal/?user_type=zxxs', '/portal/?user_type=jzyg', '/portal/?user_type=sdxy', '/portal/?user_type=hzhb', '/portal/?user_type=zsdr', '/portal/?user_type=shfk']
if __name__=='__main__':
    print(test_list)