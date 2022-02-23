'''
Created on 17-Feb-2022

@author: Nachiket Deo
'''


# class items:
#     itemset = []
#     no_items = int()


class horizontalDataset:
    t_id = int()
    item = []
    
    def __init__(self, t_id, item):
        self.t_id = t_id
        self.item = item 

class transactionTree:
    
    item_id = int()
    item_count = int()
    interval_start = int()
    interval_end = int()
    children = []
    
    def __init__(self, item_id, item_count,interval_start,interval_end,children):
        self.item_id = item_id
        self.item_count = item_count
        self.interval_start = interval_start
        self.interval_end = interval_end
        self.children = children

    def add_child(self, obj):
        self.children.append(obj)


class transactionMapping:

    def createTransactionTree(gp,length):

        freqent_itemset = {}
        ordered_frequent_itemset = {}

        root = transactionTree(0,0,0,0,[])
        
        ##
        ## Scan 1 
        ## Collecting the set of 1-frequent items F and their supports.
        ##
    
        for i in range(0,length - 1):
            data = gp[i].item
            for j in range(0,len(data)):
                if data[j] in freqent_itemset:
                    freqent_itemset[data[j]] +=1
                else:
                    freqent_itemset[data[j]] = 1
        
        ##
        ## Sorting based on the values and delete the ones with frequency as  1
        ##
    
        freqent_itemset_sorted = sorted(freqent_itemset.items(), key = lambda kv:(kv[1], kv[0]))
    
        for keys in freqent_itemset_sorted:
            if freqent_itemset_sorted[keys] == 1:
                freqent_itemset_sorted.pop(keys)
            else:
                break
        
        ##
        ## Generation of ordered_frequent_itemset for each transaction
        ##
    
        for i in range(0,length - 1):
            data = gp[i].item
            ordered_frequent_itemset[gp[i].t_id] = []
        
            for keys in freqent_itemset_sorted:
                if keys in data:
                    ordered_frequent_itemset[gp[i].t_id].append(keys)
                    
                
