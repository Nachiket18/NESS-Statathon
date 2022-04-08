"""
Created on 17-Feb-2022

@author: Nachiket Deo
"""

# class items:
#     itemset = []
#     no_items = int()

from collections import OrderedDict
from logging import root
import queue
from nbformat import current_nbformat
from lexicographic_tree import LexicographicTree

class horizontalDataset:
    t_id = int()
    item = []

    def __init__(self, t_id, item):
        self.t_id = t_id
        self.item = item


class TreeNode:
    def __init__(
        self,
        item_id,
        item_count,
        children,
        interval_start=None,
        interval_end=None,
        parent=None,
    ):
        self.item_id = item_id
        self.item_count = item_count
        self.interval_start = interval_start
        self.interval_end = interval_end
        self.children = children

    def add_child(self, data):
        # assert isinstance(node, TreeNode)
        new_node = TreeNode(item_id=data, item_count=1, children={})
        self.children[data] = new_node

    def incrementCount(self):
        self.item_count += 1

    def findChild(self, data):
        return self.children[data]
    
    def DFS_interval_list_intersection(node,findItem):
        

    def searchNodeBFS(self,root,searchItem,searchChildren):
        
        q = queue.Queue()
        visited = []

        #print(source.getId())
        q.put(root)

        visited.append(root.item_id)

        #print("visited",visited)

        while( q.empty() == False):
            v = q.get()
            if v.item_id == searchItem:

                

            for nbr in v.getConnections():
                if nbr.getId() not in visited:
                    q.put(nbr)
                    visited.append(nbr.getId())

        return visited


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

    def binSearch(self, arr, target):
        left = 0
        right = len(arr) - 1

        while left <= right:
            mid = left + (right - left) // 2

            # Base case: Checks if target value is found in the middle.
            if arr[mid] == target:
                return mid  # Returns an index value

            # Disregard left half of array if target is greater...
            elif arr[mid] < target:
                left = mid + 1

            # Disregard right half of array if target is less than...
            elif arr[mid] > target:
                right = mid - 1

        return None

    def printSubTree(self, node: TreeNode):

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

        root = TreeNode(None, None, {}, interval_start=1)
        # current_node = copy.copy(root)
        for key, value in ordered_frequent_itemset.items():
            self.buildSubTree(root, value, 0)

        self.printSubTree(root)

        # self.printSubTree(root)

        ##
        ## Construction on Interval Lists
        ##

        self.constructIntervalLists(root)

        return root,freqent_itemset_keys
    
    def constructLexicographicTree(root:TreeNode,freqent_itemset_keys:dict):

        lex = LexicoNode(freqent_itemset_keys.keys(), {})

        for i in range(0,len(lex.data)):
            lex.data[i]   
            




            
       

        # visited = BFS(tr)
        # print(visited)


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
    tm.createTransactionTree(dataset=dataset, length=8)


if __name__ == "__main__":
    main()
