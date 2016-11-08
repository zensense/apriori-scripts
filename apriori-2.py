# apriori-algo.py

'''
Algo tool for parsing assignment data and writing assignment out
Apriori Algo: p.250-253 Chapter 6 Mining Frequent Patterns, Associations, and Correlations

minsup = 0.01
absup > 771
file-in: ./categories.txt

see https://pypi.python.org/pypi/apyori/1.1.1
see http://www.borgelt.net/docs/apriori.pdf (pseudocode)

'''


import os
import sys
import apyori


class FreqItemMiner(object):

    def __init__(self, incoming, sup):
        self.file_data = incoming
        self.min_sup = sup
        self.transaction_count = 0
        self.transaction_list = []

    def data_from_file(self):
        file_iter = open(self.file_data, 'rU')
        for line in file_iter:
            self.transaction_list.append([x.strip() for x in line.split(';')])
            self.transaction_count = self.transaction_count + 1
        file_iter.close()

    def print_results(self, path_out, results_in):
        try:
            f = open(path_out, 'wb')
            for item in results_in:
                item_set = item.items
                sup = int(item.support * self.transaction_count)
                item_set = ';'.join(str(d.strip()) for d in item_set)
                print>> f, "{}:{}".format(sup, item_set)
            f.close()
        except IOError as e:
            print("Miner can't write to {} because {}".format(path_out, e))

        print("The results were printed out to: {}".format(path_out))

    def run_tools(self):
        results = list(apyori.apriori(self.transaction_list,
                                      min_support=self.min_sup))
        return results

if __name__ == "__main__":

    file_incoming = raw_input("Enter the full path to the transaction file: ")
    min_sup = 0.01
    default_path = os.path.dirname(os.path.realpath(__file__))
    db_name = 'patterns.txt'
    db_file = os.path.join(default_path, db_name)

    if os.access(file_incoming, os.R_OK):
        print("Incoming file verified: " + str(file_incoming))
    else:
        print("Check to make sure transaction file exists and is accessible.")
        sys.exit("Program exiting.")

    beginMiner = FreqItemMiner(file_incoming, min_sup)
    beginMiner.data_from_file()
    results = beginMiner.run_tools()
    beginMiner.print_results(db_file, results)
