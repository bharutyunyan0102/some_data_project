import os
import re
import bisect
import math
import sys

#defining textbook rounding function as opposed to banker's rounding
def tround(val):
    if (float(val) % 1) >= 0.5:
        x = math.ceil(val)
    else:
        x = round(val)
    return x

#function to calculate textbook median of the sorted list
def tmedian(l):
    n = len(l)
    if n % 2 == 1:
        return l[n // 2]
    else:
        return sum(l[n//2-1 : n//2+1])/2.0

#checking whether the inputted string is a correct date and return YYYYMMDD
def check_date(s):
    if re.match('[0-1][0-9][0-3][0-9]\d{4}$' ,s) != None and re.match('00.*' ,s) == None and re.match('\d{2}00.*' ,s) == None:
        return s[-4:] + s[:2] + s[2:4]
    else:
        return None

#return date to the standard format
def date_return(s):
    return s[4:6] + s[-2:] + s[:4]
        
    
    
    

#defining the dictionary for various running calculations
dict = {}

#data file directory
d_path = sys.argv[1]
#output file directory
o_path = sys.argv[2]
d_stream = open(d_path, 'r')

#erasing everything in the output file written before and then reopening for appending lines
o_stream = open(o_path, 'w')
o_stream.close()
o_stream = open(o_path, 'a')

#load the string of headers from csv file
head_path = os.path.join(os.curdir,'src', 'indiv_header_file.csv')
head_stream = open(head_path, 'r')
headstr = head_stream.readlines()[0]
headstr = headstr.strip()
headstr = headstr.split(',') #notice this is no longer a string but a list of header names
head_stream.close()

#finding the column indices of the variables of interest
CMTE_ID = headstr.index('CMTE_ID')
ZIP_CODE = headstr.index('ZIP_CODE')
TRANSACTION_DT = headstr.index('TRANSACTION_DT')
TRANSACTION_AMT = headstr.index('TRANSACTION_AMT')
OTHER_ID = headstr.index('OTHER_ID')

#reading lines, analyzing, checking conditions and writing to a new file
for i in d_stream:
    line = i.strip('\n')
    line = line.split('|')
    
    if line[CMTE_ID] !='' and line[TRANSACTION_AMT] != '':
        
        if line[OTHER_ID] == '':            
            zip = line[ZIP_CODE]
            zip = zip[0:5]
            
            
            if re.match('\d{5}', zip) != None:
                
                #key for the dictionary
                key = line[CMTE_ID] + zip
                #amount received, converted to integer and textbook rounding
                amt = int(tround(float(line[TRANSACTION_AMT])))
                
                if not (key in dict):
                    dict[key]=[]                    
                    dict[key].append([amt])
                    dict[key].append(1)
                    dict[key].append(amt)
                else:
                    bisect.insort(dict[key][0], amt)
                    dict[key][1] = dict[key][1] + 1
                    dict[key][2] = dict[key][2] + amt
                    
                #composing the string wline to write to the file
                med = int(tround(tmedian(dict[key][0])))
                wline = line[CMTE_ID] + '|' + zip + '|' + str(med) + '|' + str(dict[key][1]) + '|' + str(dict[key][2]) + '\n'
                #writing
                o_stream.write(wline)    
                
#closing the output for zip 
o_stream.close()        
d_stream.close()  

##############################################################################################
#starting the date file
d_stream = open(d_path, 'r')

o_path = sys.argv[3]
o_stream = open(o_path, 'w')
o_stream.close()
o_stream = open(o_path, 'a')

#setting the dictionary again
dict = {}

#reading lines, analyzing, checking conditions and writing to a new file
for i in d_stream:
    line = i.strip('\n')
    line = line.split('|')
    
    if line[CMTE_ID] !='' and line[TRANSACTION_AMT] != '':
        
        if line[OTHER_ID] == '':            
            date = line[TRANSACTION_DT]
            date = check_date(date)           
            if date != None:
                
                #key for the dictionary
                key = line[CMTE_ID] + date
                #amount received, converted to integer and textbook rounding
                amt = int(tround(float(line[TRANSACTION_AMT])))
                
                if not (key in dict):
                    dict[key]=[]                    
                    dict[key].append([amt])
                    dict[key].append(1)
                    dict[key].append(amt)
                else:
                    bisect.insort(dict[key][0], amt)
                    dict[key][1] = dict[key][1] + 1
                    dict[key][2] = dict[key][2] + amt

                    
#sorting the keys in the dictionary and iterating over
for key in sorted(dict.keys()):

    #composing the string wline to write to the file
    med = int(tround(tmedian(dict[key][0])))
    date = key[-8:]    
    wline = key[:-8] + '|' + date_return(date) + '|' + str(med) + '|' + str(dict[key][1]) + '|' + str(dict[key][2]) + '\n'
    #writing
    o_stream.write(wline) 




d_stream.close()
o_stream.close()
    



