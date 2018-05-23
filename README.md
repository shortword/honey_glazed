# honey_glazed
The goal of this project is to provide two main things:

1. JSON formatted versions of the NCVEC US amateur (HAM) radio test questions
2. Scripts to test yourself, analyze the frequency of answers in test sets, and to check the validity of the JSON files.

## Question JSON files

The JSON files are generated through a series of automated and manual steps.
Because the question pools are so infrequently updated the manual steps are easier to perform than scripting it.
That said, you can find, in ```pool_files/``` the original files from the NCVEC, and the rough steps used to convert them to the JSON in this (root) directory.

### IMPORTANT NOTE
While I have done my best to get the JSON files to match the NCVEC questions exactly, I can't guarantee they are 100%
correct. Please use at your own risk!

Please double check the NCVEC's website for when question pools roll over. _Typically_ this is June 30th/July 1st, but I cannot guarantee that.

## Scripts

The scripts provided at the root of this repo handle a few various tasks. Those are described below:

### analysis

This script analyzes the frequency of each answer in a JSON file.
That is, it tells you the most and least likely answers in a test set.
So, if you have to guess, at least let statistics be on your side. :)

```
$ ./analysis.py 2014-2018_tech.json 
A: 112 of 426 (26.29 %)
B: 102 of 426 (23.94 %)
C: 115 of 426 (27.00 %)
D: 97 of 426 (22.77 %)
```

### check_json

This script will analyze a JSON file and ensure that each entry has a valid question, correct answer, and valid number of answers.
It is typically run right after you run ```convert_questions```.

```
$ ./check_json.py 2014-2018_tech.json 
Test completed
```

If invalid answers would have been detected it might have looked like this:
```
ERROR: T1A11 has invalid number of answers
Test completed
```

### convert_questions

This script takes an ASCII input text file, in the format below, and converts it to a JSON file.

*NOTE:* It does not verify the validity of that file. See ```check_json.py``` above.

#### Expected Format
```
QuestionNumber (ANSWER) [REGULATION PART]
A. Answer A
B. Answer B
C. Answer C
D. Answer D
~~
```

### do_i_know_it

This script allows you to test your knowledge by parsing the JSON file and asking you random questions until it thinks you're ready.
The program flow is roughly as follows:

1. Randomize the order of the questions
1. Ask you any questions you haven't been asked in this "round"
1. Keep track of whether you've gotten the question correct or not
1. Once you've answered all questions in this round
    1. Remove any questions you've gotten right three times in a row
    1. Reset the counter on any questions you haven't 
1. Repeat until you've gotten everything right three times in a row

*NOTE:* This script makes modifications to the JSON in-place. So if you want a pristine copy you'll have to revert/re-checkout or make a copy.

#### Example:

```
$ ./do_i_know_it.py 2014-2018_tech.json 


Question 1 of 426 :: T8A11
 What is the approximate maximum bandwidth required to transmit a CW signal?

A: 2.4 kHz
B: 150 Hz
C: 1000 Hz
D: 15 kHz
Answer (QQQ to quit): b
CORRECT



Question 2 of 426 :: T5A10
 Which term describes the rate at which electrical energy is used?

A: Resistance
B: Current
C: Power
D: Voltage
Answer (QQQ to quit):
```

### quiz

This is a simpler version of ```do_i_know_it.py```.
If you're looking for a quick test, this script randomly selects a number of questions from a JSON file and presents them to you.
```
$ ./quiz.py -h
usage: quiz.py [-h] [-s <INTEGER>] [-q <INTEGER>] input

Use the JSON file to start the quiz.

positional arguments:
  input                 Name of JSON file containing questions

optional arguments:
  -h, --help            show this help message and exit
  -s <INTEGER>, --seed <INTEGER>
                        Seed value for question set; Default is random
  -q <INTEGER>, --questions <INTEGER>
                        Number of questions in quiz; default = 35 (technician
                        and general; extra has 50)
```

*NOTE:* It does NOT make sure that the number of questions for each section would be valid for a real test; AKA x questions from section A, y questions from B, etc.
It is completly random.

### results_stats

This script provides you with the results of your tests so you know what sections you need work in.
The output is long, but the usage is as follows:
```
./results_stats.py 2014-2018_tech.json
```