# honey_glazed
Scripts to help with studying for the amateur / ham radio tests in the US.

## tech, general, and extra.json
JSON copies of the HAM / amateur radio test administered by the NCVEC for the US. These were converted via an automated
script detailed below.

### IMPORTANT NOTE
While I have done my best to get the JSON files to match the NCVEC questions exactly, I can't guarantee they are 100%
correct. Please use at your own risk!

## convert_questions.py
This script takes a text file in a format similar to below, and convert it to JSON:

QuestionNumber (ANSWER) [REGULATION PART]
A. Answer A
B. Answer B
C. Answer C
D. Answer D
~~

## check_json.py
Check some basic info about the JSON; the question has text, four possible answers, and answer between A-D, etc.
