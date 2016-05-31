########################################################################
class rule:
    """定义检测一个url的规则"""
    # 例如对于一个sql注入,就应该有 一个=号.而且要是里面有 filename 这样子,这样的链接我们就不能取,然后我们来试一下~~
    # 然后这个爬虫就有了可扩展性
    #----------------------------------------------------------------------
    def __init__(self,in_url,should_all_in=0,cannot_inUrl=[],expType):
        """对于一个漏洞应该满足的条件"""
        self.in_url = in_url
        self.should_all_in = should_all_in
        self.cannot_inUrl = cannot_inUrl
        self.expType = expType
    
    #----------------------------------------------------------------------
    def check(self,url):
        """给我一个url,我给你检查是不是符合我的规则"""
        for key_word in self.cannot_inUrl:
            if key_word in url:
                return None # 如果存在不想要的关键词,那么直接丢弃
        if self.should_all_in:
            for key_word in self.in_url: # 必须存在于url中的
                if key_word not in url:
                    return None # 如果关键词没有存在 那么return False
        else:
            for key_word in self.in_url:
                if key_word in url:
                    return self.expType