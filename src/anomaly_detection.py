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

    ## Binary search implementation
    ## NOTE: Left and right take in index values. 
    def binSearch(self, arr, target): 
        left = 0 
        right = len(arr) - 1

        while left <= right: 
            mid = left + (right - left) // 2

            # Base case: Checks if target value is found in the middle. 
            if arr[mid] == target: 
                return mid # Returns an index value
            
            # Disregard left half of array if target is greater... 
            elif arr[mid] < target: 
                left = mid + 1

            # Disregard right half of array if target is less than... 
            elif arr[mid] > target: 
                right = mid - 1

        return None

    def createTransactionTree(self,dataset,length):



        freqent_itemset = {}
        ordered_frequent_itemset = {}

        root = transactionTree(0,0,0,0,[])
        
        ##
        ## Scan 1 
        ## Collecting the set of 1-frequent items F and their supports.
        ##
    
        for i in range(0,length - 1):
            data = dataset[i].item
            for j in range(0,len(data)):
                if data[j] in freqent_itemset:
                    freqent_itemset[data[j]] +=1
                else:
                    freqent_itemset[data[j]] = 1
        
        ##
        ## Sorting frequent itemset and deleting values with a frequency of 1. 
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
            data = dataset[i].item
            ordered_frequent_itemset[dataset[i].t_id] = []

            ##
            ## Since the 'frequent_itemset_sorted' is sorted we can query the elements from data into
            ## 'frequent_itemset_sorted' using Binary Search
            ##
             
            # Worse case O(n) 
            # for keys in freqent_itemset_sorted:
            #     if keys in data: 
            #         ordered_frequent_itemset[dataset[i].t_id].append(keys)
            
            # Since "frequent_itemset_sorted" is sorted... We can query elements
            # from 'data' into "ordered_frequent_itemset" using binSearch.
            # Worse case O(log(n))
            for keys in freqent_itemset_sorted:
                key = binSearch(data, keys):
                    ordered_frequent_itemset[dataset[i].t_id].append(keys)


if __name__ == '__main__': 
    # Testing binSearch method
    L = [1,2,3,4,5,6,7,8,9,10] 
    tar1 = 6
    tar2 = -3
    bS = transactionMapping()
    assert bS.binSearch(L, tar1) == 5
    assert bS.binSearch(L, tar2) == None
    print("binSearch test cases passed!")

