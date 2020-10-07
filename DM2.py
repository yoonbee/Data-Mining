"""
2018253015  YoonBee Kim   Assignment 2
"""
from math import ceil

MIN_SUPPORT_PERCENT = 0.035


# This function reads a file under filenames and extracts all transactions and a set of distinct items
# param filename: The name of the input file
# return: A dictionary of transactions and set of distinct items
def get_input_data(filename):
    input_file = open(filename, 'r')
    transaction = dict()
    genes_set = set()

    for line in input_file:
        # add to dictionary from each line
        # dictionary keys: transaction ID(first column)
        # dictionary values: genes
        sp = line.strip().split('\t')
        transaction[sp[0]] = set(sp[1:])

        # add genes to genes_set
        genes_set.update(sp[1:])

    return transaction, genes_set


# This function computes the frequency of union set and pruning non-closed branched for each itemset pair
# param frequent_itemsets: The table of frequent closed itemsets discovered
# param itemset_size: The size of intended frequent itemsets
# return: merged itemsets which non-closed branches are removed
def apply_charm_algorithm(frequent_closed_itemsets, itemset_size):
    copied = frequent_closed_itemsets[itemset_size - 1].copy()
    merged_itemsets = list()
    seen_itemsets = set()
    same_tid = list()

    for i, item1 in enumerate(copied):
        # skip to the next items if item1 is removed at frequent_closed_itemsets
        if item1 not in frequent_closed_itemsets[itemset_size - 1]:
            continue

        for item2 in copied[i + 1:]:
            # skip to the next items if item1 or item2 is removed at frequent_closed_itemsets
            if item1 not in frequent_closed_itemsets[itemset_size - 1]:
                break
            elif item2 not in frequent_closed_itemsets[itemset_size - 1]:
                continue

            # skip to the next items if size of interaction of item1 and item2 is not itemset_size - 2
            elif len(item1[0] & item2[0]) != itemset_size - 2:
                continue

            # skip to the next items if union of item1 and item2 is already merged
            elif item1[0] | item2[0] in seen_itemsets:
                continue

            # add union of item1 and item2 to seen_itemsets to prevent duplication
            seen_itemsets.add(item1[0] | item2[0])
            merged_itemsets.append([item1[0] | item2[0], item1[1] & item2[1]])

            # pruning non-closed branches
            # case 1: tid of item1 == tid of item2
            if item1[1] == item2[1]:
                frequent_closed_itemsets[itemset_size - 1].remove(item1)
                same_tid.append(item2[0])

            # case 2: tid of item1 is subset of tid of item2
            elif item1[1].issubset(item2[1]):
                frequent_closed_itemsets[itemset_size - 1].remove(item1)

            # case 3: tid of item2 is subset of tid of item1
            elif item2[1].issubset(item1[1]):
                frequent_closed_itemsets[itemset_size - 1].remove(item2)

            # case 4: tid of item1 and tid of item2 are different
            # nothing changed

    for item in frequent_closed_itemsets[itemset_size-1]:
        if item[0] in same_tid:
            frequent_closed_itemsets[itemset_size - 1].remove(item)

    return merged_itemsets


# This function pruned merged_itemset if support is smaller than min_support
# param merged_itemsets: The list of merged itemset
# param min_support: The minimum support to find frequent itemsets
# return: frequent itemsets
def pruning_infrequenct_itemsets(merged_itemsets, min_support):
    pruned_itemsets = list()

    for item in merged_itemsets:
        if len(item[1]) >= min_support:
            pruned_itemsets.append(item)

    return pruned_itemsets


# This function generates a table of closed itemsets with all frequent items from transactions
# param transactions: The transactions based upon which support is calculated
# param items: The unique set of items present in the transaction
# param min_support: The minimum support to find frequent itemsets
# return: The table of all frequent closed itemsets of different sizes
def generate_all_frequent_closed_itemsets(transactions, items, min_support):
    frequent_closed_itemsets = dict()

    itemset_size = 0
    frequent_closed_itemsets[itemset_size] = list()
    frequent_closed_itemsets[itemset_size].append(frozenset())

    # Frequent itemsets of size 1
    itemset_size += 1
    frequent_closed_itemsets[itemset_size] = list()
    for item in items:
        cnt = 0
        for dic_v in transactions.values():
            if item in dic_v:
                cnt += 1

        # get tid_set if support is greater than mini_support and add item and tid_set to frequent_closed_itemsets
        if cnt >= min_support:
            tid_set = set()
            for tran_k, tran_v in transactions.items():
                if item in tran_v:
                    tid_set.add(tran_k)
            frequent_closed_itemsets[itemset_size].append([frozenset([item]), tid_set])

    # Frequent itemsets of greater size
    itemset_size += 1

    while frequent_closed_itemsets[itemset_size - 1]:
        frequent_closed_itemsets[itemset_size] = list()

        # get merged_itemsets by using charm algorithm
        merged_itemsets = apply_charm_algorithm(frequent_closed_itemsets, itemset_size)

        # if support is greater than min_support then add to pruned_itemsets
        pruned_itemsets = pruning_infrequenct_itemsets(merged_itemsets, min_support)

        # add pruned_itemsets to frequent_closed_itemsets
        frequent_closed_itemsets[itemset_size] = pruned_itemsets
        itemset_size += 1

    return frequent_closed_itemsets


# This function writes all frequent closed itemsets along with their support to the output file with the given filename
# param filename: The name for the output file
# param frequent_closed_itemsets_table: The dictionary which contains all frequent closed itemsets
# param transactions: The transactions from which the frequent itemsets are found
# return: void
def output_to_file(filename, frequent_closed_itemsets_table, transactions):
    file = open(filename, 'w')

    for dic_k, dic_v in frequent_closed_itemsets_table.items():
        # skip if the size of sets is smaller than 2
        if dic_k < 2:
            continue
        for item in dic_v:
            s = str(item[0])[10:-1] + " " + str(round(len(item[1]) / len(transactions) * 100, 2)) + " % support\n"
            file.write(s)
    file.close()


# The main function
def main():
    input_filename = 'assignment2_input.txt'
    output_filename = 'result2.txt'
    cellular_functions, genes_set = get_input_data(input_filename)
    min_support = ceil(MIN_SUPPORT_PERCENT * len(cellular_functions))
    frequent_closed_itemsets_table = generate_all_frequent_closed_itemsets(cellular_functions, genes_set, min_support)
    output_to_file(output_filename, frequent_closed_itemsets_table, cellular_functions)


if __name__ == '__main__':
    main()
