#!/usr/bin/env python

import sys
import csv
import re

from table import SIMPLE_NAMES, CATEGORIES
from collections import defaultdict


def main(path):
    #print 'loading data from: %s...' % path
    result = defaultdict(int)
    with open(path) as csv_file:
        for date, _, name, amount, diff in csv.reader(csv_file, delimiter=';'):
            clear_name = clear(name)
            expense_type = categorize(clear_name) or 'Other'
            result[expense_type] += float(diff.replace(',', ''))
    longest = max(map(len, result.keys()))
    for expense, total in result.items():
        print '{1:{0}} {2:,}'.format(longest, expense, total)


def clear(name):
    for simple_name in SIMPLE_NAMES:
        if simple_name in name:
            return simple_name
    clear = re.sub(r'^Card \*\*\*\d+ ', '', name)
    clear = re.sub(r'(?:\d+ )?(MOSCOW|MOSKVA|MOSCOVSKAYA)', '', clear)
    return clear.strip()


def categorize(name):
    for category, names in CATEGORIES.items():
        if name in names:
            return category


if __name__ == '__main__':
    if len(sys.argv) > 1:
        path = sys.argv[1]
        main(path)
    else:
        print 'no input provided'
