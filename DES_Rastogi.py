#!/usr/bin/env/python

### hw2_starter.py

#shubham rastogi
#ECE404 HW2
#0026340022, rastogis@purdue.edu

import sys
from BitVector import *
from random import randint
################################   Initial setup  ################################

# Expansion permutation (See Section 3.3.1):
expansion_permutation = [31, 0, 1, 2, 3, 4, 3, 4, 5, 6, 7, 8, 7, 8, 
9, 10, 11, 12, 11, 12, 13, 14, 15, 16, 15, 16, 17, 18, 19, 20, 19, 
20, 21, 22, 23, 24, 23, 24, 25, 26, 27, 28, 27, 28, 29, 30, 31, 0]

# P-Box permutation (the last step of the Feistel function in Figure 4):
p_box_permutation = [15,6,19,20,28,11,27,16,0,14,22,25,4,17,30,9,
1,7,23,13,31,26,2,8,18,12,29,5,21,10,3,24]

# Initial permutation of the key (See Section 3.3.6):
key_permutation_1 = [56,48,40,32,24,16,8,0,57,49,41,33,25,17,9,1,58,
50,42,34,26,18,10,2,59,51,43,35,62,54,46,38,30,22,14,6,61,53,45,37,
29,21,13,5,60,52,44,36,28,20,12,4,27,19,11,3]

# Contraction permutation of the key (See Section 3.3.7):
key_permutation_2 = [13,16,10,23,0,4,2,27,14,5,20,9,22,18,11,3,25,
7,15,6,26,19,12,1,40,51,30,36,46,54,29,39,50,44,32,47,43,48,38,55,
33,52,45,41,49,35,28,31]

# Each integer here is the how much left-circular shift is applied
# to each half of the 56-bit key in each round (See Section 3.3.5):
shifts_key_halvs = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1] 




###################################   S-boxes  ##################################

# Now create your s-boxes as an array of arrays by reading the contents
# of the file s-box-tables.txt:
with open('s-box-tables.txt') as f:
	arrays = []
	for line in f: #read a line in file at a time
		if len(line) > 4: #make s box with lines with more than characters
			arrays.append(line.split())
s_box = []
for i in range(0,32, 4):
   	s_box.append([arrays[k] for k in range(i, i+4)]) # S_BOX



#######################  Get encryption key from user  ###########################

def get_encryption_key(): # key                                                              
    ## ask user for input
    key = raw_input("Enter key:\n")
    ## make sure it satisfies any constraints on the key
    while not len(key) == 8: # keep asking user for a key of excatly 8 bytes in length
		print ("Enter a key that is 8 characters long\n")
		key = raw_input("Enter key:\n")
    ## next, construct a BitVector from the key    
    user_key_bv = BitVector(textstring = key)   
    key_bv = user_key_bv.permute( key_permutation_1 )        ## permute() is a BitVector function
    return key_bv


################################# Generatubg round keys  ########################
def extract_round_key( nkey ): # round key
    round_key = []                                                   
    for i in range(16):
		[left,right] = nkey.divide_into_two()   ## divide_into_two() is a BitVector function
		left << shifts_key_halvs[i] # shift the left by key halves
		right << shifts_key_halvs[i] # shift the right by key halves
		rejoined_key_bv = left + right;	 #rejoin the key
		round_key.append(rejoined_key_bv.permute( key_permutation_2 )) #key permutation
    return round_key


########################## encryption and decryption #############################

def des(encrypt_or_decrypt, input_file, output_file, key, flag): 
    bv = BitVector( filename = input_file ) #make a bitvector of the file
    encryption = "" # string to return encrypted text
    rand_pos = randint(0, 63) # generate random number
    FILEOUT = open( output_file, 'wb' ) #open file
    while bv.more_to_read:
        bitvec = bv.read_bits_from_file( 64 )   ## assumes that your file has an integral    
        modulo = bitvec.length() % 64 
        if flag == True:
			rand_pos = randint(0, 63)
			bitvec[rand_pos] = bitvec[rand_pos] ^ 1
			flag = False 
        if not modulo == 0:
            bitvec.pad_from_right(64 - modulo)  # pad if not in multiple of 8 bytes
        [LE, RE] = bitvec.divide_into_two() 
        round_key = extract_round_key(key)
        for i in range(16):        #16 rounds of DES
            temp = RE #make temp of right side
            RE = RE.permute(expansion_permutation) #do expansion permutation
            if encrypt_or_decrypt == "d": #depending on decrytpion on encryption change RE
				RE = RE ^ round_key[15 - i]
            elif encrypt_or_decrypt == "e":
				RE = RE ^ round_key[i]
            first = 0
            middle = 1
            last = 5
            bv2 = BitVector(size = 0)
            for I in range(8):
                J = 2 * RE[first] + RE[last] #calculate row for s box
                K = 2 * RE[middle + 2] + 4 * RE[middle + 1] + RE[middle + 3] + 8 * RE[middle] #calculate column for s box
                bv2 += BitVector(intVal = int(s_box[I][J][K]), size = 4) #append sbox value to new bitvector
                first += 6
                middle += 6
                last += 6
            bv2 = bv2.permute(p_box_permutation)   #do p box permutation
            LE = LE ^ bv2   # xor with original LE and switch right and left
            RE = LE
            LE = temp 
        bitvec = RE + LE
		#print out the bitvec to output file and reutrn the encryption
        FILEOUT.write(bitvec.get_text_from_bitvector())
        encryption += bitvec.get_text_from_bitvector()
    FILEOUT.close()
    return encryption		
#################################### main #######################################

def main():
    ## write code that prompts the user for the key
    ## and then invokes the functionality of your implementation
	des_key = get_encryption_key()
	stat = raw_input("Do you want to encrypt or decrypt? (e/d)")
	if stat == "e":
		inputf = "message.txt"
		outputf = "encrypted.txt"
	elif stat == "d":
		inputf = "encrypted.txt"
		outputf = "decrypted.txt"
	enc1 = des(stat, inputf, outputf, des_key, False)
	sys.exit()
if __name__ == "__main__":
	main()
