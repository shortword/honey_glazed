#!/usr/bin/python

# Authors:
# Michael Bergeron - Copyright 2016

# Released under the MIT license. See the LICENSE file in this directory for
# more information.

import argparse
import json
import os.path
import re

# Argument Parsing
parser = argparse.ArgumentParser(
        description='Covert text question files in to JSON')
parser.add_argument('filename', metavar='input', type=str, nargs=1,
        help='Name of text file containing questions')
parser.add_argument('output', metavar='output', type=str, nargs=1,
        help='Name of the file to output JSON to')
args = parser.parse_args()

# Open the input file
if not os.path.isfile(args.filename[0]):
    raise ValueError('Invalid filename provided')
f = open(args.filename[0], 'r')

# Open the output file
if os.path.exists(args.output[0]):
    raise ValueError('Output filename already exists')
outfile = open(args.output[0], 'w')

in_question = False
in_answers = False
q_list = []
q_data = dict()
q_data['text'] = ''
q_data['answers'] = []
for line in f:
    line = line.rstrip()

    # If we have started a question, pull the question text, or answers
    if in_question:

        # Does the question end on this line?
        if line.startswith('~~'):
            q_list.append(q_data)
            in_question = False
            in_answers = False
            q_data = dict()
            q_data['text'] = ''
            q_data['answers'] = []
            continue

        # Is an answer starting on this line?
        if line.startswith('A. '):
            in_answers = True

        if in_answers:
            if re.match('^[A-D]\. ', line):
                q_data['answers'].append(line[3:])
            else:
                q_data['answers'][len(q_data['answers']) - 1] += " " + \
                        line
            continue

        # The question may be multiple lines
        q_data['text'] += ' ' + line
        q_data['text'] = q_data['text'].rstrip()
        continue

    # Check if starting a new question
    if re.match('^[EGT][0-9]+[A-Z][0-9]+', line):
        split_line = line.split()
        q_data['number'] = split_line[0]
        q_data['answer'] = split_line[1][1]
        if len(split_line) > 2:
            q_data['part'] = split_line[2]
        else:
            q_data['part'] = '((NOT SPECIFIED))'
        in_question = True
        continue

json.dump(q_list, outfile)
