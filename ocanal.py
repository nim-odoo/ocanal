#!/usr/bin/env python3

import argparse
import operator
from subprocess import check_output

def parse_line(line):
    line_split = line.lower().split(':')
    if len(line_split) <= 1:
        return []
    line_split = line_split[0].split(']')
    if len(line_split) <= 1:
        return []
    modules = line_split[-1].replace(' ', '').split(',')
    return modules

# Parse arguments
parser = argparse.ArgumentParser(description='Odoo commit analysis')
parser.add_argument('-d', '--date', required=True, help='start date of analysis')
parser.add_argument('-b', '--branch', required=True, help='branch to analyze')
args = parser.parse_args()

# Checkout appropriate branch and retrieve log output 
check_output(['git', 'checkout', '-q' , args.branch])
out = check_output([
    'git', 'log', '--oneline', '--after="{}"'.format(args.date), '--grep=\[F'
])

# Parse git log
data = {}
for line in out.decode('utf-8').split('\n'):
    modules_list = parse_line(line)
    for module in modules_list:
        data.setdefault(module, 0)
        data[module] += 1

# Sort and display results
data_sorted = sorted(data.items(), key=operator.itemgetter(1))
data_sorted.reverse()

print('Total: {}, from {}, on branch {}\n'.format(sum(data.values()), args.date, args.branch))
print('|{:40s}|{}|'.format('Module', 'Count'))
print('|{}|{}|'.format(40 * '-', 5 * '-'))
for module, count in data_sorted:
    print('|{:40s}|{:5d}|'.format(module, count))
