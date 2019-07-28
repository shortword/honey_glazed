# pool_files

These files are copies of the exact files as downloaded from the NCVEV.
See the ARRL's website for the latest links to NCVEC question pools and
diagrams.

http://www.arrl.org/question-pools

## Conversion Step

The general flow for conversion looks like this:
1. Pull the doc or PDF question pool
1. Convert to a .txt file (though it will likely be Unicode, not ASCII): `docx2txt [docfile.docx]`
1. Verify that listed Errata have been addressed
1. Check the file type is ASCII (not unicode): `file [docfile.txt]`
1. (If necessary) Convert the unicode to ASCII
1. Fix any formatting issues
1. Run `convert_questions.sh`