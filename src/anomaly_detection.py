'''
Created on 17-Feb-2022

@author: Nachiket Deo
'''


# class items:
#     itemset = []
#     no_items = int()

from collections import OrderedDict

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
    
    def __init__(self):
        pass

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

    def createTransactionTree(self,dataset:list,length:int):



        freqent_itemset = {}
        ordered_frequent_itemset = {}

        root = transactionTree(0,0,0,0,[])
        
        ##
        ## Scan 1 
        ## Collecting the set of 1-frequent items F and their supports.
        ##
    
        for i in range(0,length):
            data = dataset[i].item
            for j in range(0,len(data)):
                if data[j] in freqent_itemset:
                    freqent_itemset[data[j]] +=1
                else:
                    freqent_itemset[data[j]] = 1
        
        ##
        ## Sorting based on the values and delete the ones with frequency as  1
        ##

        #print("fq",freqent_itemset)

        freqent_itemset_sorted = sorted(freqent_itemset.items(), key = lambda kv:(kv[1], - kv[0]), reverse = True)
        
        #print(freqent_itemset_sorted)
        freqent_itemset_keys = {}
        i = 0
        for keys in freqent_itemset_sorted:
            if keys[1] == 1:
                freqent_itemset_sorted.pop(i)
            else:
                freqent_itemset_keys[keys[0]] = keys[1]
            i += 1        


        # freqent_itemset_keys = sorted(freqent_itemset_keys.items(), key = lambda kv:(kv[0]), reverse = False)
        # print(freqent_itemset_keys)
        ##
        ## Generation of ordered_frequent_itemset for each transaction
        ##
        #print(list(freqent_itemset_keys.keys()))

        for i in range(0,length):
            data = dataset[i].item
            ordered_frequent_itemset[dataset[i].t_id] = []
            for key_frequent in freqent_itemset_keys:
                for keys in data:
                    if key_frequent == keys:
                        ordered_frequent_itemset[dataset[i].t_id].append(keys)

        print(ordered_frequent_itemset)
       


def main():
    t_1 = horizontalDataset(1,[2,1,5,3,19,20])
    t_2 = horizontalDataset(2,[2,6,3])
    t_3 = horizontalDataset(3,[1,7,8])
    t_4 = horizontalDataset(4,[3,1,9,10])
    t_5 = horizontalDataset(5,[2,1,11,3,17,18])
    t_6 = horizontalDataset(6,[2,4,12])
    t_7 = horizontalDataset(7,[1,13,14])
    t_8 = horizontalDataset(8,[2,15,4,16])

    dataset = []
    dataset.append(t_1)
    dataset.append(t_2)
    dataset.append(t_3)
    dataset.append(t_4)
    dataset.append(t_5)
    dataset.append(t_6)
    dataset.append(t_7)
    dataset.append(t_8)
    tm = transactionMapping()
    tm.createTransactionTree(dataset = dataset,length = 8)
    
if __name__ == '__main__': 
    main()