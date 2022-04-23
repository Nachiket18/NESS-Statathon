"""
Created on 17-Feb-2022

@author: Nachiket Deo
"""

# class items:
#     itemset = []
#     no_items = int()

from dataclasses import dataclass
import queue
from typing import Any, Dict, List, Optional
from lexicographic_tree import LexicoNode


class horizontalDataset:
    t_id = int()
    item = []

    def __init__(self, t_id, item):
        self.t_id = t_id
        self.item = item

@dataclass
class TreeNode:
    item_id: int
    item_count: int
    children: Dict[int, object]
    interval_start: Optional[int] = None
    interval_end: Optional[int] = None

    def add_child(self, data: int):
        # assert isinstance(node, TreeNode)
        new_node = TreeNode(item_id=data, item_count=1, children={})
        self.children[data] = new_node

    def findChild(self, data):
        return self.children[data]

    def incrementCount(self):
        self.item_count += 1

    ##
    ## To locate a node with specified item_id in the Transaction Tree
    ##

    def searchNodeBFS(self,searchItem,searchChildren):
        
        output_interval_range = []
        output_searchItemRange = []
        q = queue.Queue()
        visited = []

        #print(source.getId())
        q.put(self)

        visited.append(self.item_id)

        while( q.empty() == False):
            v = q.get()

            if v.item_id == searchItem:
                
                sub_q = queue.Queue()
                sub_q.put(v)

                sub_visited = []
                sub_visited.append(v.item_id)
                output_searchItemRange.append(v.interval_start)
                output_searchItemRange.append(v.interval_end)
                while (sub_q.empty() == False):
                    
                    b = sub_q.get()
                    for key,chd in b.children.items():
                        #if key not in sub_visited:
                        sub_q.put(chd)
                        sub_visited.append(key)
                        if key in searchChildren:
                            output_interval_range.append([chd.item_id,chd.interval_start,chd.interval_end])

                out_tree_node = v

            else:

                for key,nbr in v.children.items():
                    if key not in visited:
                        q.put(nbr)
                        visited.append(key)

        return output_interval_range,output_searchItemRange,out_tree_node


class transactionMapping:
    def __init__(self):
        pass

    def buildSubTree(self, node: TreeNode, value, i: int):
        print("Node:", node.item_id, node.item_count, node.children.keys())

        if i <= (len(value) - 1):

            if value[i] in node.children.keys():
                node.children[value[i]].incrementCount()

                child = node.findChild(value[i])
                self.buildSubTree(child, value, i + 1)

            else:
                node.add_child(value[i])
                print("Child-Added", node.item_id, node.children[value[i]].item_id)
                child = node.findChild(value[i])
                self.buildSubTree(child, value, i + 1)
        else:
            return
        return

    def constructIntervalLists(self, node: TreeNode):

        queue = []  # Create a queue
        queue.append(node)

        while len(queue) != 0:

            node_t = queue[0]
            queue.pop(0)
            i = 0

            for key, value in node_t.children.items():
                i += 1
                print(
                    value.item_id,
                    value.item_count,
                    node_t.item_count,
                    node_t.item_id,
                    node_t.interval_start,
                )
                queue.append(value)
                if i == 1:
                    s_1 = node_t.interval_start
                    e_1 = (s_1 + value.item_count) - 1
                    value.interval_start = s_1
                    value.interval_end = e_1
                    e_i_prime = e_1
                else:
                    s_i = e_i_prime + 1
                    e_i = (s_i + value.item_count) - 1
                    value.interval_start = s_i
                    value.interval_end = e_i
                    e_i_prime = e_i
                    
    
    def printSubTree(self,node:TreeNode):
        
        q = []  # Create a queue
        q.append(node)

        print("In")
        while len(q) != 0:

            n = len(q)

            # If this node has children
            while n > 0:

                # Dequeue an item from queue and print it
                p = q[0]
                q.pop(0)
                print(p.item_id, p.item_count, p.interval_start, p.interval_end)

                # Enqueue all children of the dequeued item
                for key, value in p.children.items():
                    q.append(p.children[key])
                n -= 1

            print()

    def createTransactionTree(self, dataset: list, length: int):

        freqent_itemset = {}
        ordered_frequent_itemset = {}

        ##
        ## Scan 1
        ## Collecting the set of 1-frequent items F and their supports.
        ##

        for i in range(0, length):
            data = dataset[i].item
            for j in range(0, len(data)):
                if data[j] in freqent_itemset:
                    freqent_itemset[data[j]] += 1
                else:
                    freqent_itemset[data[j]] = 1

        ##
        ## Sorting based on the values and delete the ones with frequency as  1
        ##

        # print("fq",freqent_itemset)

        freqent_itemset_sorted = sorted(
            freqent_itemset.items(), key=lambda kv: (kv[1], -kv[0]), reverse=True
        )

        # print(freqent_itemset_sorted)
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
        # print(list(freqent_itemset_keys.keys()))

        for i in range(0, length):
            data = dataset[i].item
            ordered_frequent_itemset[dataset[i].t_id] = []
            for key_frequent in freqent_itemset_keys:
                for keys in data:
                    if key_frequent == keys:
                        ordered_frequent_itemset[dataset[i].t_id].append(keys)

        print(ordered_frequent_itemset)


        root = TreeNode(None,None,{},interval_start = 1)
        
        for key,value in ordered_frequent_itemset.items():
            self.buildSubTree(root,value,0)
        

        self.printSubTree(root)

        # self.printSubTree(root)

        ##
        ## Construction on Interval Lists
        ##

        self.constructIntervalLists(root)

        return root,freqent_itemset_keys
    
    def findIntersection(self,intervals_1,interval_2):
        return max(0, min(intervals_1[1], interval_2[1]) - max(intervals_1[0], interval_2[0]) + 1)

    
    def depth_first_search_lexicographic_tree_build(self,lex_node:TreeNode,root:TreeNode):
        
        searchChildren = []
        lst = list(lex_node.data)
        print("List of the Lexicographic Node",lst)

        for j in range(0,len(lst)-1):
        
            for i in range(j+1,len(lst)):
                searchChildren.append(lst[i])   

            out_range,output_searchItemRange,tree_node_current = root.searchNodeBFS(lst[j],searchChildren=searchChildren)
            print(out_range,output_searchItemRange)

            if len(out_range) != 0:

                new_node_data = []
                for node_data in out_range:   
                    support_count = self.findIntersection( [ node_data[1],node_data[2] ], output_searchItemRange )
                    print(support_count)
                    if support_count >= 2:
                        new_node_data.append(node_data[0])
                
                if new_node_data:

                    child = LexicoNode(new_node_data, {})     
                    lex_node.add_node(lst[j],child)
                    self.depth_first_search_lexicographic_tree_build(child,tree_node_current)

        return;       

    def constructLexicographicTree(self,root:TreeNode,freqent_itemset_keys:dict):

        lex = LexicoNode(freqent_itemset_keys.keys(), {})
        self.depth_first_search_lexicographic_tree_build(lex,root)

        lex.print_out()

            
    

def main():
    t_1 = horizontalDataset(1, [2, 1, 5, 3, 19, 20])
    t_2 = horizontalDataset(2, [2, 6, 3])
    t_3 = horizontalDataset(3, [1, 7, 8])
    t_4 = horizontalDataset(4, [3, 1, 9, 10])
    t_5 = horizontalDataset(5, [2, 1, 11, 3, 17, 18])
    t_6 = horizontalDataset(6, [2, 4, 12])
    t_7 = horizontalDataset(7, [1, 13, 14])
    t_8 = horizontalDataset(8, [2, 15, 4, 16])

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
    root,freqent_itemset_keys = tm.createTransactionTree(dataset = dataset,length = 8)
    
    tm.constructLexicographicTree(root,freqent_itemset_keys)

if __name__ == '__main__': 
    main()
