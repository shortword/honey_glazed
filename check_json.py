#!/usr/bin/python

# Authors:
# Michael Bergeron - mikeb.code@gmail.com - Copyright 2016

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
args = parser.parse_args()

# Open the input file
if not os.path.isfile(args.filename[0]):
    raise ValueError('Invalid filename provided')

with open(args.filename[0], 'r') as f:
    data = json.load(f)

for this in data:
    if not this['number']:
        print "ERROR: Entry without a number"
        continue

    if not this['answer'] or not re.match('[A-D]', this['answer']):
        print "ERROR: %s has invalid answer" % (this['number'])

    if not this['text']:
        print "ERROR: %s has invalid question text" % (this['number'])

    if len(this['answers']) != 4:
        print "ERROR: %s has invalid number of answers" % (this['number'])

print "Test completed"

