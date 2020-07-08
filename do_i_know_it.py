#!/usr/bin/env python3

# Authors:
# Brad Geltz - brgeltz@gmail.com - Copyright 2016
# Michael Bergeron - mikeb.code@gmail.com - Copyright 2016

# Released under the MIT license. See the LICENSE file in this directory for
# more information.

# IMPORTANT NOTE: In the effort of simplicity, this script modifies your JSON
#                 file in place. So, if you want an unmodified version of your
#                 JSON make sure to make a copy!

# This script is designed to have a running test for you. It will:
#   1. Randomize the order of all the questions
#   2. Ask you all of the questions
#   3. Keep track of whether you got it correct or not.
#   4. Once you've answer a question correctly 3 times it drops it from the pool
#   5. You can pick-up from where you left off.

import argparse
import json
import os.path
import random
import string
import sys
from datetime import datetime

now = int((datetime.now() - datetime(1970, 1, 1)).total_seconds())

# Argument Parsing
parser = argparse.ArgumentParser(
        description='A running test which asks a lot of questions')
parser.add_argument('filename', metavar='input', type=str, nargs=1,
        help='Name of JSON file containing questions')
args = parser.parse_args()

# Open the input file
if not os.path.isfile(args.filename[0]):
    raise ValueError('Invalid filename provided')

# Open up the JSON file
with open(args.filename[0], 'r')as f:
    data = json.load(f)

# Setup the answer tracking if it hasn't been setup already
for this in data:
    if 'times_asked' not in this:
        this['times_asked'] = 0
        this['times_correct'] = 0
        this['times_wrong'] = 0
        this['correct_in_a_row'] = 0

# Generate from a changing but constant seed. This isn't crypto. :)
random.seed(now)

continue_loop = True
while continue_loop:

    # Determine whether some questions have been asked fewer times than others.
    # Ask those for the first set.
    min = sys.maxsize
    questions = []
    for this in data:
        if this['times_asked'] <= min:
            if this['times_asked'] < min:
                min = this['times_asked']
                questions = []
            if this['correct_in_a_row'] < 3:
                questions.append(this)

    # Randomize the question order
    random.shuffle(questions)

    correct_list = []
    incorrect_list = []
    num = 1;

    # Ask the questions
    for this in questions:

        # Print the question and potential answers
        print("")
        print("")
        print("Question %d of %d :: %s" % (num, len(questions), this['number']))
        num += 1
        print(this['text'])
        print("")
        ans_list = [ 'A', 'B', 'C', 'D' ]
        idx = 0
        for ta in this['answers']:
            print("%s: %s" % (ans_list[idx], ta))
            idx += 1

        # Get an answer
        resp = input("Answer (QQQ to quit): ")
        resp = resp.upper()
        if resp == "QQQ":
            continue_loop = False
            break;

        # Check the answer
        if resp == this['answer']:
            this['times_correct'] += 1
            correct_list.append(this['number'])
            this['correct_in_a_row'] += 1
            print("CORRECT")
        else:
            this['times_wrong'] += 1
            incorrect_list.append(this['number'])
            this['correct_in_a_row'] = 0
            print("INCORRECT (%s)" %(this['answer']))
        this['times_asked'] += 1
        with open(args.filename[0], 'w')as f:
            json.dump(data, f)

    print("Round complete")
    cor = len(correct_list)
    wro = len(incorrect_list)
    tot = cor + wro
    print("Correct:   %3d (%3.2f)" % (cor, (float(cor)/float(tot)) * 100))
    print("Incorrect: %3d (%3.2f)" % (wro, (float(wro)/float(tot)) * 100))
    print()
    print("Correct List:")
    print(correct_list)
    print()
    print("Incorrect List:")
    print(incorrect_list)

with open(args.filename[0], 'w')as f:
    json.dump(data, f)

# TODO - Handle no answers given better

times_right = {}
times_right['0'] = []
times_right['1'] = []
times_right['2'] = []
times_right['3'] = []

# TODO - Fix this stuff below

#for this in data:
#    times_right['%d' % this['correct_in_a_row']].append(this['number'])
#
#for key, value in times_right:
#    print
#    print "Times correct - %d:" % (key)
#    for this in value:
#        print "this"
#    print
