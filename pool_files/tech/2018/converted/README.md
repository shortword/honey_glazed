# converted

Converted files generally adhere to the following generation flow:
    1. The doc/docx file is converted to straight text
    1. The straight text from the step above has its headers and errata removed
    1. The 'cleaned' version from the step above is run through convert_questions.py.
    1. The JSON version is run through check_json.py
    1. The straight text version above is manually corrected
    1. Repeat convert_questions.py and check_json.py until the check is successful.

The script files mentioned above are found at the root of this repo.
