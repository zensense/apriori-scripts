# apriori-algo.py

'''
Algo tool for parsing assignment data and writing assignment out
Apriori Algo: p.250-253 Chapter 6 Mining Frequent Patterns, Associations, and Correlations

minsup = 0.01
absup > 771
file-in: ./categories.txt

see https://pypi.python.org/pypi/apyori/1.1.1
see http://www.borgelt.net/docs/apriori.pdf (pseudocode)
see http://www.kdnuggets.com/2016/04/association-rules-apriori-algorithm-tutorial.html

# itertools
see http://jmduke.com/posts/a-gentle-introduction-to-itertools/
see https://docs.python.org/2/library/itertools.html

https://github.com/asaini/Apriori/blob/master/apriori.py

'''


import os
import sys
from itertools import chain, combinations
from collections import defaultdict


class FreqItemMiner(object):

    def __init__(self, incoming, sup, flag):
        self.file_data = incoming
        self.minSup = sup
        self.flag = flag

    def data_from_file(self):
        file_iter = open(self.file_data, 'rU')
        for line in file_iter:
            record = frozenset(line.split(';'))
            yield record

    def build_transaction_items_lists(self, iterator):
        # output transaction list and itemset
        # sets vs. lists: http://stackoverflow.com/questions/2831212/python-sets-vs-lists
        # a transaction is one line of our file
        transactions = list()
        # an item is a 1-item set
        items = set()

        for record in iterator:
            transaction = frozenset(record)
            transactions.append(transaction)
            for item in transaction:
                items.add(frozenset([item]))

        return items, transactions

    def mine_min_sup_items(self, itemset, transaction_list, freqset):
        """calculates the support for items in the itemSet and returns a subset
       of the itemSet each of whose elements satisfies the minimum support"""
        # TODO: add support number to output
        _itemset = set()
        localset = defaultdict(int)

        for item in itemset:
            for transaction in transaction_list:
                if item.issubset(transaction):
                    freqset[item] += 1
                    localset[item] += 1

        for item, count in localset.items():
            support = float(count)/len(transaction_list)

            if support >= self.minSup:
                _itemset.add(item)

        return _itemset

    def subsets(self, arr):
        """ Returns non empty subsets of arr"""
        return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])

    def join_set(self, items, length):
        return set([i.union(j) for i in items for j in items if len(i.union(j)) == length])

    def print_results(self, path_out, results_in):
        try:
            f = open(path_out, 'wb')
            for item in results_in:
                item_set, sup = item
                item_set = ';'.join(str(d.strip()) for d in item_set)
                print>> f, "{}:{}".format(sup, item_set)
            f.close()
        except IOError as e:
            print("Miner can't write to {} because {}".format(path_out, e))

        print("The results were printed out to: {}".format(path_out))

    def run_tools(self):
        """
        run the apriori algorithm. data_iter is a record iterator
         - items (tuple, support)
        """

        init_data = self.data_from_file()
        items, transactions = self.build_transaction_items_lists(init_data)

        frequent_set = defaultdict(int)
        large_set = dict()

        one_candidate_set = self.mine_min_sup_items(items, transactions, frequent_set)

        def get_support(item):
            return float(frequent_set[item]) / len(transactions)

        current_large_set = one_candidate_set
        k = 2
        while current_large_set != set([]):
            large_set[k - 1] = current_large_set
            current_large_set = self.join_set(current_large_set, k)
            current_candidate_set = self.mine_min_sup_items(current_large_set, transactions, frequent_set)
            current_large_set = current_candidate_set
            k = k + 1

        # flag for abs support
        return_items = []
        if self.flag == "rel":
            for key, value in one_candidate_set.items():
                return_items.extend([(tuple(item), get_support(item)) for item in value])

            return return_items
        elif self.flag == "abs":

            for key, value in large_set.items():
                return_items.extend([(tuple(item), frequent_set[item]) for item in value])

            return return_items
        else:
            print("Correct flag wasn't found in runTools()")

        # output items, support

if __name__ == "__main__":

    file_incoming = raw_input("Enter the full path to the transaction file: ")
    part_flag = raw_input("Enter support type ('rel' or 'abs'): ")
    min_sup = 0.01
    default_path = os.path.dirname(os.path.realpath(__file__))
    db_name = 'patterns.txt'
    db_file = os.path.join(default_path, db_name)

    if os.access(file_incoming, os.R_OK):
        print("Incoming file verified: " + str(file_incoming))
    else:
        print("Check to make sure transaction file exists and is accessible.")
        sys.exit("Program exiting.")

    if part_flag == "rel" or "abs":
        beginMiner = FreqItemMiner(file_incoming, min_sup, part_flag)
        results = beginMiner.run_tools()
        beginMiner.print_results(db_file, results)
    else:
        print "Please enter a valid assignment flag ('one' or 'two')."
        sys.exit("Program exiting.")
