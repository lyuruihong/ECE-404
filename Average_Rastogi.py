#!/usr/bin/env/python

#shubham rastogi
#ECE404 HW2
#0026340022, rastogis@purdue.edu

key_permutation_1 = [56,48,40,32,24,16,8,0,57,49,41,33,25,17,9,1,58,
50,42,34,26,18,10,2,59,51,43,35,62,54,46,38,30,22,14,6,61,53,45,37,
29,21,13,5,60,52,44,36,28,20,12,4,27,19,11,3]

import sys
from BitVector import *
from random import randint
import DES_Rastogi
def main(): 
	key = "ecepurdu" #key for DES
	user_key_bv = BitVector(textstring = key) # make bitvector of key
	key_bv = user_key_bv.permute(key_permutation_1) #permute key
	encrypt_og = DES_Rastogi.des("e", "message.txt",  "output.txt", key_bv, False) #get encryption without changing message
	# get encryption after changing a bit 4 different times
	encrypt_1 = DES_Rastogi.des("e", "message.txt",  "output.txt", key_bv, True) 
	encrypt_2 = DES_Rastogi.des("e", "message.txt",  "output.txt", key_bv, True)
	encrypt_3 = DES_Rastogi.des("e", "message.txt",  "output.txt", key_bv, True)
	encrypt_4 = DES_Rastogi.des("e", "message.txt", "output.txt", key_bv, True)
	#make Bitvectors of encryption text returned
	bv_og = BitVector(textstring = encrypt_og)
	bv_enc_1 = BitVector(textstring = encrypt_1)
	bv_enc_2 = BitVector(textstring = encrypt_2)
	bv_enc_3 = BitVector(textstring = encrypt_3)
	bv_enc_4 = BitVector(textstring = encrypt_4)
	#XOR the original with the changed BV to find the number of changed bits
	bv_enc_1 = bv_enc_1 ^ bv_og
	bv_enc_2 = bv_enc_2 ^ bv_og
	bv_enc_3 = bv_enc_3 ^ bv_og
	bv_enc_4 = bv_enc_4 ^ bv_og
	#Calculate number of changed bits
	num1 = bv_enc_1.count_bits()
	num2 = bv_enc_2.count_bits()
	num3 = bv_enc_3.count_bits()
	num4 = bv_enc_4.count_bits()
	#calculate average
	avg = (num1 + num2 + num3 + num4) / 4
	print "The average diffusion is: ", avg
	rand_num = randint(0, 63) # random number generation for changing key bit
	encrypt_ogk = DES_Rastogi.des("e", "message.txt",  "output.txt", key_bv, False) #get encryption without changing key
	key_tmp = key_bv
	key_tmp[rand_num] = key_tmp[rand_num] ^ 1 #change one random bit in key
	# get encryption after changing a bit in key 4 different times
	encrypt_1k = DES_Rastogi.des("e", "message.txt",  "output.txt", key_tmp, True) 
	key_tmp = key_bv
	rand_num = randint(0, 63) # random number generation for changing key bit
	key_tmp[rand_num] = key_tmp[rand_num] ^ 1 #change one random bit in key
	encrypt_2k = DES_Rastogi.des("e", "message.txt",  "output.txt", key_tmp, True)
	key_tmp = key_bv
	rand_num = randint(0, 63) # random number generation for changing key bit
	key_tmp[rand_num] = key_tmp[rand_num] ^ 1 #change one random bit in key
	encrypt_3k = DES_Rastogi.des("e", "message.txt",  "output.txt", key_tmp, True)
	key_tmp = key_bv
	rand_num = randint(0, 63) # random number generation for changing key bit
	key_tmp[rand_num] = key_tmp[rand_num] ^ 1 #change one random bit in key
	encrypt_4k = DES_Rastogi.des("e", "message.txt", "output.txt", key_tmp, True)
	#make Bitvectors of encryption text returned
	bv_ogk = BitVector(textstring = encrypt_ogk)
	bv_enc_1k = BitVector(textstring = encrypt_1k)
	bv_enc_2k = BitVector(textstring = encrypt_2k)
	bv_enc_3k = BitVector(textstring = encrypt_3k)
	bv_enc_4k = BitVector(textstring = encrypt_4k)
	#XOR the original with the changed BV to find the number of changed bits
	bv_enc_1k = bv_enc_1k ^ bv_ogk
	bv_enc_2k = bv_enc_2k ^ bv_ogk
	bv_enc_3k = bv_enc_3k ^ bv_ogk
	bv_enc_4k = bv_enc_4k ^ bv_ogk
	#Calculate number of changed bits
	num1k = bv_enc_1k.count_bits()
	num2k = bv_enc_2k.count_bits()
	num3k = bv_enc_3k.count_bits()
	num4k = bv_enc_4k.count_bits()
	#calculate average
	avgk = (num1k + num2k + num3k + num4k) / 4
	print "The average confusion is: ", avgk
if __name__ == "__main__":
	main()
"""

bash-4.1$ python ./Average_Rastogi.py
The average diffusion is:  30
The average confusion is:  4804
"""
