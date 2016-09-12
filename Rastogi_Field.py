#Shubham Rastogi
#Rastogis@purdue.edu

#!/usr/bin/env python

import sys
from BitVector import *

num = None
isprime = 0
while type(num) != int:
	num = int(raw_input("Enter an integer number: "))
for i in range(1, num + 1):
	if num % i == 0:
		isprime += 1	
if isprime == 2:
	fp = open("output.txt", "w")
	fp.write("field")
	fp.close()
else:
	fp = open("output.txt", "w")
	fp.write("ring")
	fp.close()

#bash-4.1$ python Rastogi_Field.py
#Enter an integer number: 45
#bash-4.1$ !cat
#cat output.txt 
#ring

#bash-4.1$ python Rastogi_Field.py
#Enter an integer number: 41
#bash-4.1$ cat output.txt 
#field
