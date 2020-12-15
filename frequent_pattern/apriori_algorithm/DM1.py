"""
2018253015  YoonBee Kim  Assignment 1
"""

from math import ceil
from itertools import combinations

MIN_SUPPORT_PERCENT = 0.035


# This function reads a file under filename and extracts all transactions and a set of distinct items
# param filename: The name of the input file (should provide path if necessary)
# return: A dictionary of transactions and a set of distinct items
def get_input_data(filename):
    input_file = open(filename, 'r')
    transactions = dict()
    itemset = set()
    for line in input_file:
        """
        FILL UP HERE!
        Parse a transaction from each line by using split with certain delimiters and store the items as a value of the key transaction id
        Also generate a list of all distinct items from the transactions
        """
        # add to dictionary from each line
        # dictionary keys: transaction ID(first column)
        # dictionary values: genes
        sp = line.strip().split('\t')
        transactions[sp[0]] = set(sp[1:])

        # append genes to itemset
        itemset.update(sp[1:])

    return transactions, itemset


# This function calculates support of the itemset from transactions
# param transactions: All transactions in a dictionary
# param itemset: The itemset to calculate support
# return: The support count of the itemset
def support(transactions, itemset):
    support_count = 0
    """
    FILL UP HERE!
    Calculate support of an itemset by iterating over the frequent itemsets
    """
    # find support_count
    # if itemset is subset of transactions.value() then plus 1
    for dic_v in transactions.values():
        if itemset.issubset(dic_v):
            support_count += 1
    return support_count


# This function generates a combination from the frequent itemsets of size (itemset_size - 1) and accepts joined itemsets if they share (itemset_size - 2) items
# param frequent_itemsets: The table of frequent itemsets discovered
# param itemset_size: The size of joined itemsets
# return: All valid joined itemsets
def generate_selectively_joined_itemsets(frequent_itemsets, itemset_size):
    # Record seen_itemsets to prevent duplicates
    seen_itemsets = set()
    joined_itemsets = set()

    """
    FILL UP HERE!
    Try all combinations of two itemsets from the table of frequent itemsets and join the pair if they share (itemset_size - 2) items
    Add each joined itemset to the list if it is not present in the list and discard it otherwise
    """
    # find all combination of two itemsets(size: itemset_size-1)
    # and add it to joined_itemsets if they share (itemset_size-2) items
    for i, item1 in enumerate(tuple(frequent_itemsets[itemset_size - 1])):
        for item2 in tuple(frequent_itemsets[itemset_size - 1])[i + 1:]:
            if len(item1 & item2) == itemset_size - 2:
                joined_itemsets.add(item1 | item2)

    return joined_itemsets


# This function checks all the subsets of selected itemsets whether they all are frequent or not and prunes the itemset if anyone of the subsets is not frequent
# param selected_itemsets: The itemsets which are needed to be checked
# param frequent_itemsets: The table of frequent itemsets discovered
# param itemset_size: The size of intended frequent itemsets
# return: The itemsets whose all subsets are frequent
def apply_apriori_pruning(selected_itemsets, frequent_itemsets, itemset_size):
    apriori_pruned_itemsets = set()
    """
    FILL UP HERE!
    Add each itemset to the list if all of its subsets are frequent and discard it otherwise
    """
    # find all subsets that size is itemset_size -1
    # and add to apriori_pruned_itemsets if all of the subset is in frequent_itemsets
    for item in selected_itemsets:
        subsets = tuple()

        for size in range(itemset_size - 1, itemset_size):
            subsets = subsets + tuple(combinations(item, size))

        subset_flag = True
        for subset_t in set(subsets):
            subset_s = frozenset(subset_t)

            if subset_s not in frequent_itemsets[len(subset_s)]:
                subset_flag = False
                break

        if subset_flag is True:
            apriori_pruned_itemsets.add(item)

    return apriori_pruned_itemsets


# This function generates candidate itemsets of size (itemset_size) by selective joining and apriori pruning
# param frequent_itemsets: The table of frequent itemsets discovered
# param itemset_size: The size of intended frequent itemsets
# return: candidate itemsets formed by selective joining and apriori pruning
def generate_candidate_itemsets(frequent_itemsets, itemset_size):
    joined_itemsets = generate_selectively_joined_itemsets(frequent_itemsets, itemset_size)
    candidate_itemsets = apply_apriori_pruning(joined_itemsets, frequent_itemsets, itemset_size)
    return candidate_itemsets


# This function generates a table of itemsets with all frequent items from transactions based on a given minimum support
# param transactions: The transactions based upon which support is calculated
# param items: The unique set of items present in the transaction
# param min_support: The minimum support to find frequent itemsets
# return: The table of all frequent itemsets of different sizes
def generate_all_frequent_itemsets(transactions, items, min_support):
    frequent_itemsets = dict()
    itemset_size = 0
    frequent_itemsets[itemset_size] = list()
    frequent_itemsets[itemset_size].append(frozenset())

    # Frequent itemsets of size 1
    itemset_size += 1
    frequent_itemsets[itemset_size] = list()

    """
    FILL UP HERE!
    Find all frequent itemsets of size-1 and add them to the list
    """
    # add frequent itemsets(size: 1) if their support is greater than min_support
    size1 = set()
    for item in items:
        s = 0
        for dic_v in transactions.values():
            if item in dic_v:
                s += 1
        if s >= min_support:
            size1.add(frozenset([item]))
    frequent_itemsets[itemset_size] = size1

    # frequent itemsets of greater size
    itemset_size += 1

    while frequent_itemsets[itemset_size - 1]:
        frequent_itemsets[itemset_size] = list()
        candidate_itemsets = generate_candidate_itemsets(frequent_itemsets, itemset_size)
        pruned_itemset = set()
        """
        FILL UP HERE!
        Prune the candidate itemset if its support is less than minimum support
        """
        # if support is greater than min_support then add each item to pruned_itemset
        for item in candidate_itemsets:
            if (support(transactions, item)) >= min_support:
                pruned_itemset.add(item)

        frequent_itemsets[itemset_size] = pruned_itemset
        itemset_size += 1
    return frequent_itemsets


# This function writes all frequent itemsets along with their support to the output file with the given filename
# param filename: The name for the output file
# param frequent_itemsets_table: The dictionary which contains all frequent itemsets
# param transactions: The transactions from which the frequent itemsets are found
# return: void
def output_to_file(filename, frequent_itemsets_table, transactions):
    file = open(filename, 'w')
    """
    FILL UP HERE!
    Iterate over the list of frequent itemsets of different size and write them to the file with the given filename along their support
    Follow this format:
    {YIL035c, YOR039w} 3.70% support 
    {YDL134c, YDL188c} 3.70% support 
    {YIL035c, YOR061w, YGL019w} 3.70% support   
    """
    # write file if size(transactions.keys()) >= 2
    for dic_k, dic_v in frequent_itemsets_table.items():
        if dic_k < 2:
            continue
        for item in dic_v:
            s = str(item)[10:-1] + " " + str(
                round(support(transactions, item) / len(transactions) * 100, 2)) + "% support\n"
            file.write(s)

    file.close()


# The main function
def main():
    input_filename = 'assignment1_input.txt'
    output_filename = 'result1.txt'
    cellular_functions, genes_set = get_input_data(input_filename)
    min_support = ceil(MIN_SUPPORT_PERCENT * len(cellular_functions))
    frequent_itemsets_table = generate_all_frequent_itemsets(cellular_functions, genes_set, min_support)
    output_to_file(output_filename, frequent_itemsets_table, cellular_functions)
    print(frequent_itemsets_table)

if __name__ == '__main__':
    main()
