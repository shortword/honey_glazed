#!/usr/bin/env python3

# Authors:
# Brad Geltz - brgeltz@gmail.com - Copyright 2016

# Released under the MIT license. See the LICENSE file in this directory for
# more information.

import argparse
import json
import os.path
import re
import random
from datetime import datetime

now = int((datetime.now() - datetime(1970, 1, 1)).total_seconds())

# Argument Parsing
parser = argparse.ArgumentParser(
        description='Use the JSON file to start the quiz.')
parser.add_argument('filename', metavar='input', type=str, nargs=1,
        help='Name of JSON file containing questions')
parser.add_argument('-s', '--seed', metavar='<INTEGER>', type=int, dest='s', default=now,
    help='Seed value for question set; Default is random')
parser.add_argument('-q', '--questions', metavar='<INTEGER>', type=int, dest='q', default=35,
    help='Number of questions in quiz; default = 35 (technician and general; extra has 50)')
args = parser.parse_args()

# Open the input file
if not os.path.isfile(args.filename[0]):
    raise ValueError('Invalid filename provided')

with open(args.filename[0], 'r') as f:
    data = json.load(f)

random.seed(args.s)
question_set = random.sample(range(len(data)), args.q)

print('-' * 58)
print('Amateur Radio / Ham Radio Quiz #%d - %d questions' % (args.s, args.q))
print('-' * 58)

letters = ['A', 'B', 'C', 'D']

right = 0

for i in range(0, args.q):
    print()
    print('Question (%d / %d) : %s - %s' % \
        ((i+1), args.q, data[question_set[i]]['number'], data[question_set[i]]['text']))
    if data[question_set[i]]['part'] != '((NOT SPECIFIED))':
        print('Part - %s' % data[question_set[i]]['part'])

    for j, k in enumerate(data[question_set[i]]['answers']):
        print('\t%s. %s' % (letters[j], k))
    print()

    while True:
        ans = input("? ")
        ans = ans.upper()
        if ans in letters:
            break
        print('Enter only A, B, C, or D.')

    msg = ''
    if ans == data[question_set[i]]['answer']:
        right += 1
        msg += 'CORRECT'
    else:
        msg += 'WRONG (correct answer: %s)' % data[question_set[i]]['answer']

    print('%s - (%d / %d) = %d%%' % (msg, right, (i+1), (right/float(i+1)*100)))

print("Test completed")

