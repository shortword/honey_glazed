#!/usr/bin/python

# Authors:
# Michael Bergeron - mikeb.code@gmail.com - Copyright 2016

# Released under the MIT license. See the LICENSE file in this directory for
# more information.

# This script provides simple analytics about the JSON file. Namely, how often
# each answer appears. :)

import argparse
import json
import os.path
import string

# Argument Parsing
parser = argparse.ArgumentParser(
        description='Generate basic analytics based on JSON')
parser.add_argument('filename', metavar='input', type=str, nargs=1,
        help='Name of text file containing questions')
args = parser.parse_args()

# Open the input file
if not os.path.isfile(args.filename[0]):
    raise ValueError('Invalid filename provided')

with open(args.filename[0], 'r') as f:
    data = json.load(f)

answers = dict()
answers['A'] = 0
answers['B'] = 0
answers['C'] = 0
answers['D'] = 0
total = 0

for this in data:
    answers[this['answer']] += 1
    total += 1

for this in string.uppercase[:4]:
    print "%s: %s of %d (%2.2f %%)" % (this, answers[this], total,
            (float(answers[this])/float(total)) * 100)

