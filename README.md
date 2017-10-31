# Approach

## For zip output file

The code reads the input file line by line. For each read line, it is split on the pipe separator and analyzed by re package. I check all the conditions for validity of entries of interest of the line and then add the appropriately parsed entries to a dictionary with the key of contributor id and zip code joined as string. At the last step a new string line is composed, written to the output file, and the program proceeds to the next line.
To calculate the running median, each transaction amount is inserted into the list under the specific key in an appropriate place so as to keep list sorted. This is accomplished by bisect package. Calculating median on a sorted list then is trivial (function tmedian defined manually).


## For date output file

The process is similiar to the above descibed but the writing happens only when the whole dictionary is ready and all lines are processed. 
The keys of the dictionary are composed of conributor id + date string, but date is re-parsed to YYYYMMDD format. This allows sorting of the keys. At the last writting step, keys of the dictionary are extracted into a list, sorted, and threaded over each element with one by one writing of lines into the output file. During the writing process the date is re-converted back into the original format (dunction date_return).

# Package Dependencies

re
bisect
math
os
sys

Note: The instructions didn't specify whether one should consider transactions with 0 amount, so I didn't omit them. 
