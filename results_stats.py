#!/usr/bin/env python3

# Authors:
# Michael Bergeron - mikeb.code@gmail.com - Copyright 2016

# Released under the MIT license. See the LICENSE file in this directory for
# more information.

# This script provides simple analytics about the JSON file. Namely, how often
# each answer appears. :)

import argparse
import json
import os.path
import re
import string
import textwrap

# Helper functions
def fill_dict(dest, key, sub_list, src):
    if key not in dest:
        dest[key] = {}
    for this in sub_list:
        if this not in dest[key]:
            dest[key][this] = 0
        dest[key][this] += src[this]
    pass

def print_res(results, colors_off=False):
    OK = '\033[92m'
    WARN = '\033[93m'
    FAIL = '\033[91m'
    CLR = '\033[0m'
    for this in sorted(results):
        tc = results[this]['times_correct']
        ta = results[this]['times_asked']
        if ta:
            pct = float(tc) / float(ta) * 100
        else:
            pct = 0
        color = OK
        if pct < 80:
            color = WARN
        if pct < 74.3:
            color = FAIL

        if colors_off:
            CLR = ''
            color = ''

        print((CLR + "Test: %s :: %d/%d = " + color + "%3.2f%%" + CLR) % \
                (this, tc, ta, pct))

# Argument Parsing
parser = argparse.ArgumentParser(
        description='Generate analytics based on your results JSON')
parser.add_argument('-c', '--colors-off', action='store_true',
        help="Disable color coding")
parser.add_argument('filename', metavar='input', type=str, nargs=1,
        help='Name of text file containing previous test')
args = parser.parse_args()

# Open the input file
if not os.path.isfile(args.filename[0]):
    raise ValueError('Invalid filename provided')

with open(args.filename[0], 'r') as f:
    data = json.load(f)

num_sorted = sorted(data, key=lambda k: k['number'])

res_test = {}
res_sect = {}
res_sub = {}

for this in num_sorted:
    m = re.search('([EGT])([0-9])([A-Z])([0-9]+)', this['number'])
    test = m.group(1)
    sect = m.group(2)
    sub = m.group(3)
    num = m.group(4)

    key_list = ['times_asked', 'times_correct', 'times_wrong',
            'correct_in_a_row']

    #TODO: There must be a better way to do this, but not sure how
    fill_dict(res_test, test, key_list, this)
    fill_dict(res_sect, test + sect, key_list, this)
    fill_dict(res_sub, test + sect + sub, key_list, this)

print("========== SORTED BY TEST ==========")
print_res(res_test, args.colors_off)
print("")

print("========== SORTED BY SECTION ==========")
print_res(res_sect, args.colors_off)
print("")

print("========== SORTED BY SUBSECTION ==========")
print_res(res_sub, args.colors_off)
print("")

print("========== QUESTION LAST ANSWERED INCORRECT ==========")
inc_list = []
for this in num_sorted:
    if this['times_asked'] > 0 and this['correct_in_a_row'] == 0:
        inc_list.append(this['number'])

for line in textwrap.wrap(" ".join(inc_list), 80):
    print(line)
