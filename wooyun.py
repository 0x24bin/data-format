import json
from collections import defaultdict
path = '/home/fang/out.json'
records = [json.loads(line) for line in open(path).readlines()]
changshang_dic = [rec['changhsang'] for rec in records]
# 找出给的平均rank最高的厂商
########################################################################
class changshang:
    """"""

    #----------------------------------------------------------------------
    def __init__(self,name):
        """Constructor"""
        
        self.name = name
        self.rank = 0
        self.count = 0 # 漏洞计数
    
    #----------------------------------------------------------------------
    def __hash__(self):
        """"""
        return hash(self.name)
#----------------------------------------------------------------------
def get_rank_top(records):
    """"""
    changshang_set = {} # 
    for i in records:
        if hash(i['changhsang']) in changshang_set:
            changshang_set[hash(i['changhsang'])].rank+=i['changshang_rank']
            changshang_set[hash(i['changhsang'])].count+=1
        else:
            
            changshang_set[changshang(i['changhsang'])] = i['changshang_rank']
            changshang_set[hash(i['changhsang'])].count = 1
#----------------------------------------------------------------------
def get_counts(sequence):
    counts = {}
    for i in sequence:
        if i in counts:
            counts[i] += 1
        else:
            counts[i] = 1
    return counts
#----------------------------------------------------------------------
def top_counts(count_dict, n=10):
    """"""
    value_key_pairs = [(count,name) for name,count in count_dict.items()]
    value_key_pairs.sort()
    return value_key_pairs[-n:]
changshang_count = get_counts(changshang_dic)
get_rank_top(records)
print('over!')