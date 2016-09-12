
#Shubham Rastogi
#Rastogis@purdue.edu
#ECE 404 hw 4

import sys
from BitVector import *
from random import randint
import collections
def genTable():
	subBytesTable = [] 
	AES_modulus = BitVector(bitstring='100011011')
	c = BitVector(bitstring='01100011')
	d = BitVector(bitstring='00000101')
	for i in range(0, 256):
        # For the encryption SBox
		a = BitVector(intVal = i, size=8).gf_MI(AES_modulus, 8) if i != 0 else BitVector(intVal=0)
        # For bit scrambling for the encryption SBox entries:
		a1,a2,a3,a4 = [a.deep_copy() for x in range(4)]
		a ^= (a1 >> 4) ^ (a2 >> 5) ^ (a3 >> 6) ^ (a4 >> 7) ^ c
		subBytesTable.append(int(a))
	return subBytesTable

def genInvTable():
	invSubBytesTable = []
	AES_modulus = BitVector(bitstring='100011011')
	c = BitVector(bitstring='01100011')
	d = BitVector(bitstring='00000101')
	for i in range(0, 256):
        # For the decryption Sbox:
		b = BitVector(intVal = i, size=8)
        # For bit scrambling for the decryption SBox entries:
		b1,b2,b3 = [b.deep_copy() for x in range(3)]
		b = (b1 >> 2) ^ (b2 >> 5) ^ (b3 >> 7) ^ d
		check = b.gf_MI(AES_modulus, 8)
		b = check if isinstance(check, BitVector) else 0
		invSubBytesTable.append(int(b))
	return invSubBytesTable

def g(word, Table_Bytes, round_num):
	# Calculate the g function value
	AES_modulus = BitVector(bitstring='100011011')
	#rotate word to the left by 1
	d = collections.deque(word)
	d.rotate(-1)
	##call subbytes function on each byte of the word
	for I in range(4):
		word[I] = SubBytes(word[I], Table_Bytes)
	#calculate Rcon value
	RC = []
	temp = BitVector(intVal = 0x01, size = 8)
	bitvec_2 = BitVector(intVal = 0x02, size = 8)
	RC.append(temp) 
	for I in range(1, 10):
		RC.append(RC[I - 1].gf_multiply_modular(bitvec_2, AES_modulus, 8))
	word[0] = word[0] ^ RC[round_num]
	return word


def SubBytes(inputByte, Table_Bytes):
	#divide input byte into two halves
	[left,right] = inputByte.divide_into_two() 
	row = left.intValue()
	col = right.intValue()
	#subsitute input byte with Subbyte from table
	SubByte = Table_Bytes[((row * 16) + col)]
	SubByte_bv = BitVector(intVal = SubByte, size = 8)
	return SubByte_bv

def ShiftRow(statearray):
	#rotate second row to the left once
	d = collections.deque(statearray[1])
	d.rotate(-1)
	#rotate third row to the left twice
	statearray[1] = d
	d = collections.deque(statearray[2])
	d.rotate(-2)
	statearray[2] = d
	#rotate third row to the left thrice
	d = collections.deque(statearray[3])
	d.rotate(-3)
	statearray[3] = d
	return statearray

def ColumnMix(statearray):
	AES_modulus = BitVector(bitstring='100011011')
	#generate matrix for column mixing
	matrix = [[0 for x in range(4)]  for x in range(4)]
	matrix[0][0] = BitVector(intVal = 0x02, size = 8)
	matrix[0][1] = BitVector(intVal = 0x03, size = 8) 
	matrix[0][2] = BitVector(intVal = 0x01, size = 8)
	matrix[0][3] = BitVector(intVal = 0x01, size = 8)
	matrix[1][0] = BitVector(intVal = 0x01, size = 8)
	matrix[1][1] = BitVector(intVal = 0x02, size = 8)
	matrix[1][2] = BitVector(intVal = 0x03, size = 8)
	matrix[1][3] = BitVector(intVal = 0x01, size = 8)
	matrix[2][0] = BitVector(intVal = 0x01, size = 8)
	matrix[2][1] = BitVector(intVal = 0x01, size = 8)
	matrix[2][2] = BitVector(intVal = 0x02, size = 8)
	matrix[2][3] = BitVector(intVal = 0x03, size = 8)
	matrix[3][0] = BitVector(intVal = 0x03, size = 8)
	matrix[3][1] = BitVector(intVal = 0x01, size = 8)
	matrix[3][2] = BitVector(intVal = 0x02, size = 8)
	matrix[3][3] = BitVector(intVal = 0x01, size = 8)
	#Calculate new matric to be returned by muliplying hex matrix with input
	ret_statearray = [[0 for x in range(4)]  for x in range(4)]
	for i in range(4):
		for j in range(4):
			ret_statearray[i][j] = matrix[i][j].gf_multiply_modular(statearray[i][j], AES_modulus, 8)
	return ret_statearray
	
def AES():
	#define some varibles
	Table_Bytes = genTable()
	num = 4
	text = ""
	Store_word = []
	key = "howtogettosesame"
	#make key bitvector and key array
	key_bv = BitVector(textstring = key)
	keyarray = [[0 for x in range(4)]  for x in range(4)]
	for i in range(4):
		for j in range(4):
			keyarray[j][i] = key_bv[32 * i + 8 * j:32 * i + 8 *(j + 1)]
	#make first 4 words from key
	word = [[0 for x in range(4)]  for x in range(4)]
	word[0] = keyarray[:][0]
	word[1] = keyarray[:][1]
	word[2] = keyarray[:][2]
	word[3] = keyarray[:][3] 
	#store words from key in a list
	for I in range(4):
		Store_word.append(word[I])
	#generate w4 to w43
	for x in range(10):
		for I in range(4):
			temp = g(word[3], Table_Bytes, x)
			for J in range(4):
				word[0][J] = word[0][J] ^ temp[J]
		for I in range(4):
			word[1][I] = word[0][I] ^ word[1][I]
			word[2][I] = word[1][I] ^ word[2][I]
			word[3][I] = word[2][I] ^ word[3][I]
		#store w4 to w43 in a list
		for I in range(4):
			Store_word.append(word[I])
	#open and read 12 bits from file
	bv = BitVector(filename = 'plaintext.txt')
	while bv.more_to_read:
		bitvec = bv.read_bits_from_file(128)
		mod = bitvec.length() % 128
		if not mod == 0:
			bitvec.pad_from_right(128 - mod)
		#generate statearray from the input
		statearray = [[0 for x in range(4)]  for x in range(4)]
		for i in range(4):
			for j in range(4):
				statearray[j][i] = bitvec[32 * i + 8 * j:32 * i + 8 *(j + 1)]
		#XOR statearray from the input with w0 to w3
		for I in range(4):
			for J in range(4):
				statearray[I][J] = statearray[I][J] ^ Store_word[I][J]
		#run AES form 10 rounds
		for x in range(10):
			#do subbytes on each byte of statearray
			for k in range(4):
				for l in range(4):
					statearray[k][l] = SubBytes(statearray[k][l], Table_Bytes)
			#do shift rows on statearray
			statearray = ShiftRow(statearray)
			#do column mixing on statearray except for last round
			if x < 9:
				statearray = ColumnMix(statearray)
			#The statearray is XORed with wi to w(i+3)
			for I in range(4):
				for J in range(4):
					statearray[I][J] = statearray[I][J] ^ Store_word[I + num][J]
			num = num + 4
		num = 4
		#store text to be written to file
		for I in range(4):
			for J in range(4):
				text += statearray[I][J].get_bitvector_in_hex()
	#open and write to file 
	fp = open( 'encryptedtext.txt', 'wb' )
	fp.write(text)
	fp.close()
	#return generated words
	return Store_word

def InvSubBytes(inputByte, Table_Bytes):
	#Divide input byte into 2
	[left,right] = inputByte.divide_into_two() 
	row = left.intValue()
	col = right.intValue()
	#subsite input byte from the byte in the inverse subsitution table
	SubByte = Table_Bytes[((row * 16) + col)]
	SubByte_bv = BitVector(intVal = SubByte, size = 8)
	return SubByte_bv

def InvShiftRow(statearray):
	#rotate second row to the right by one
	d = collections.deque(statearray[1])
	d.rotate(1)
	statearray[1] = d
	#rotate third row to the right by two
	d = collections.deque(statearray[2])
	d.rotate(2)
	statearray[2] = d
	#rotate fourth row to the right by three
	d = collections.deque(statearray[3])
	d.rotate(3)
	statearray[3] = d
	return statearray

def InvColumnMix(statearray):
	#generate matrix for multiplication
	AES_modulus = BitVector(bitstring='100011011')
	matrix = [[0 for x in range(4)]  for x in range(4)]
	matrix[0][0] = BitVector(intVal = 0x0E, size = 8)
	matrix[0][1] = BitVector(intVal = 0x0B, size = 8) 
	matrix[0][2] = BitVector(intVal = 0x0D, size = 8)
	matrix[0][3] = BitVector(intVal = 0x09, size = 8)
	matrix[1][0] = BitVector(intVal = 0x09, size = 8)
	matrix[1][1] = BitVector(intVal = 0x0E, size = 8)
	matrix[1][2] = BitVector(intVal = 0x0B, size = 8)
	matrix[1][3] = BitVector(intVal = 0x0D, size = 8)
	matrix[2][0] = BitVector(intVal = 0x0D, size = 8)
	matrix[2][1] = BitVector(intVal = 0x09, size = 8)
	matrix[2][2] = BitVector(intVal = 0x0E, size = 8)
	matrix[2][3] = BitVector(intVal = 0x0B, size = 8)
	matrix[3][0] = BitVector(intVal = 0x0B, size = 8)
	matrix[3][1] = BitVector(intVal = 0x0D, size = 8)
	matrix[3][2] = BitVector(intVal = 0x09, size = 8)
	matrix[3][3] = BitVector(intVal = 0x0E, size = 8)
	#generate return state array and multiply the matrices together
	ret_statearray = [[0 for x in range(4)]  for x in range(4)]
	for i in range(4):
		for j in range(4):
			ret_statearray[i][j] = matrix[i][j].gf_multiply_modular(statearray[i][j], AES_modulus, 8)
	return ret_statearray

def AES_Decrypt(Store_word):
	#initialize variables
	bv = BitVector(filename = 'encryptedtext.txt')
	Inv_Table = genInvTable()
	num = 4
	text = ""
	#rea 12 bits at a time from file
	while bv.more_to_read:
		bitvec = bv.read_bits_from_file(128)
		mod = bitvec.length() % 128
		if not mod == 0:
			bitvec.pad_from_right(128 - mod)
		#create statearray of encrypted ciphertext
		statearray = [[0 for x in range(4)]  for x in range(4)]
		for i in range(4):
			for j in range(4):
				statearray[j][i] = bitvec[32 * i + 8 * j:32 * i + 8 *(j + 1)] 
		#XOR statearray with w40 to w43
		for I in range(4):
			for J in range(4):
				statearray[I][J] = statearray[I][J] ^ Store_word[I + 40][J]
		#Run decryption 10 times
		for x in range(10):
			#Do inverse shift row
			statearray = InvShiftRow(statearray)
			#do inverse sub bytes on each byte of statearray
			for k in range(4):
				for l in range(4):
					statearray[k][l] = InvSubBytes(statearray[k][l], Inv_Table)
			#XOR words with statearray
			for I in range(4):
				for J in range(4):
					statearray[I][J] = statearray[I][J] ^ Store_word[I + num][J]
			num = num + 4
			#do inverse column mix for the first 9 rounds of the decryption
			if x < 9:
				statearray = InvColumnMix(statearray)
		#store text of statearray in hex 
		for I in range(4):
			for J in range(4):
				text += statearray[I][J].get_bitvector_in_hex()
		num = 4
	#write decrypted text to a file
	fp = open( 'decryptedtext.txt', 'wb' )
	fp.write(text)
	fp.close()
if __name__ == "__main__":
	Store_word = AES()
	AES_Decrypt(Store_word)



#Output

#bash-4.1$ python ./ece404_hw04_rastogi.py
#bash-4.1$ cat plaintext.txt
#This is an unusual paragraph. I'm curious how quickly you can find out what is so unusual about it? It looks so plain you would think nothing was wrong with it! In fact, nothing is wrong with it! It is unusual though. Study it, and think about it, but you still may not find anything odd. But if you work at it a bit, you might find out! Try to do so without any coaching! You most probably won't, at first, find anything particularly odd or unusual or in any way dissimilar to any ordinary composition. That is not at all surprising, for it is no strain to accomplish in so short a paragraph a stunt similar to that which an author did throughout all of his book, without spoiling a good writing job, and it was no small book at that.
#bash-4.1$ 
#bash-4.1$ 
#bash-4.1$ cat encryptedtext.txt
#676d4b53e9ff3c27129fbe5fb6dc83ea0da3543eb976cf9373d85f4d7dfce4ffb067a96816760f274a84b56b77dcc6f7f6ea2a531676b1425445db9a09ebb3df3cc48239b959c5d073743374d6880c512ec4f61c16ff0f1c5a78c990147adf94f6875b00155998d0517478920e7ae5779bb02aae162ccf422845a6f8777aa4df340fb91037763c4212e3f72d48bedfdf23726000bd630fe53d9b33907db56ceae7ff2b8016a5dc43a85962cf777fe5bafe6d0a39564b0f4c120cbe49ed7a83dff687a9ae165998d09574686048bee5eb55727dae16250f800b9bcd3a237a6775f6a3b975377698e580b3f7e6484be5ea2ebda837990bccd00be93360d67ae5ea239c358016769842126f629a77ebb3943cb0461ce925c54573d1abf8d69e3d75e76d3568150bf0275aba68d8d60e63eae7bdaf594876d7d00b74f73a235de594b5fcfb00bd0b0fc6f6d162601dfaa4ea86eaaff62f0b0f4220d1a074d6246cdff6c40a1c46b798d0a174bec252a90c94f66daf807376bdf69c84a04c0ef37bf72e9c5b59e97699452874c3e623fa4151e71afb00bdb765d012e962fb1d4e6cea34fc54ae092c3c421214f7e652f3df9455b754ae1659ffa87374686048be0cdf556d4b68e9b70f27e2e3d33ad67a6ceaf4bd4b1c5276d381927ebee6237f837756b7541c46720f27e2e3be4c525d6c9423724c003763d3e50b7ac95f237aa4ea3ca3f6ae607473d00b74be4c0ef3e594f6fc5b8052767e751274becf7a88df07e71a461ce976bdd0e20cbee62342e594399caff6bd0b7327f69f6274d688e475c66d4b0852b77343a674c94ce7a9633be718af39db2cd78073e3f7e6f3f383bae718af4cd7a598c6e2d8b5747abee5ba3c18af002f4b0fc62884f7491df3c6692e724b1c60aacc809cd1cf74d6a967eaf672af24d70b7ec273e7f76023fa41bce7bde610160b7e32017ec992d6030c9be718af59b6765627a6e3a0e6147fa4fff46daff6e9720f4c12d8a0e6d6dd63b25572b97616
#bash-4.1$ 
#bash-4.1$ cat decryptedtext.txt 
#84bd258ecf944f37facf2152267c4d6646828f7e4a36230a2dcf48312de2a5dcca488f63cf9692e7c42e8f0702db385b4248c71e9b76f6d376d421452db61c20fa69293a4a96be1efa668f52027c8714ae82c76347bcb006ea6648452d7c7cb0bff8292a4a9ff4bfe3cf8f3d0204db6602d6dd2acf364c37add0898832b69f9d4c0d8f63cfc9c1f6f02e648853987cba42a3033a4a94f62c94c0c0783f387cdacc07293a4a966ef0f03c21c7264f7c05028929ba6996b01e94d08f075e711c8fbf482948eccdf437ea0264885398878f021edd1e8ac91d0894d08f735e7c7cfb2bf829634a9612bfa2f2bf3d2d04065bcc69c78447768cf0ad7b8f885eb69f144c82718e47944c1e1a3c8f3d0204a58f460769ba0d96237ce38e558834b63820cc438f3a9b96f6f89402c331d4de118f4ca3c7be9b94922c2dd0553151e2b28fc8f829ba4a944f37eb84fb3d51dba58f2843c71e47c98cf693308ff826e28adcbf7ae63a4a966ebffa2eaa3d324f4dba4682257e9b36230a1ad48f885eb6d1babf6929484acdf41eeaf264885398875b2b43691e0dc913089466553134fb7c8f021e293a4a9613c994f2bfe25198115bca8980bedfde12c92d2e8f735edeb29dbf82714847cdf41ec4c08f3102de381e1d07691e0dc9be7ca258aa3132e238f9cc69c863cf946e08a22e4d8832984d54caa3031e4ac9122ce3668f315ee28a8fcca329484acdf6062d848f3d0204d18f4643c72a473623f6fad089073271a59d4cbd2563cfc9c1f0a23cbf3d51de06054269038e4adff637767bcc7334defa14c8a3294decd24f06fa664d52327c4d14024303be4a36b008a28c4d3134e2db14c86969ba0dde4fd3a2cf8f8802984dbaca07801edfc9127c942e640765717c9dfa078f3a9b961337eb024d70323fd18fbf4329849b76f4f6766621315ee2fa8f1d69803a8496f4d3e37b4d3d3204dbf9cc6903be4a94bef876c0bf88abb6fadabf7a69484acdf4bff03c5588b7987c052882e63a89941d0a9430fb0753717cfbbf69c72adfdff4d3fa848f45023f4d8f2b69dd678aa7c1f8ead42145d47c7c05cc482548cf816e372dcf8f3d02ded1bacc898066df9f8c2c945821785e387cf9c8078fbe9bc94f37e8025588b798db8f464329be9b9423f6e37baa3134e28ab04c48dd8ecf944ce7ebf2bf3d2d04d15b4607e6ba8996237ce8582107d4717cf90248294d4a9613e7a2f2642f5336875b4243693a0d94f6089466558834b67c8f02bd253acf961337fa665552b77c4d14c8d603be4a94232ce32e8f315ee2389dbfbde6ba89364c37a23c8fe202384d052b82807edf36230a94588f73267c80f90248693a4a96f4e7a23c8f52f17c8705c882e6be8994230ae3d4640765713805ccbd71ba4736f6039402c331d4de118fca898084df76121e94cf8f315ee2dbdc4c07ce67d536c1f0c4f28f88ab98385bca82dd1e8ac9120a94d42107d4717c05bf48e667893df437eb848f7302ded18f4682c7baa596230a9430c0483f7c7cdcc8bd252acfdf4ff0e83c8f880298db05c882801edfc9230a1a58aa07f171d1f94c698f679b3648d32d7b4d52327cd1f9bf43031e4a76f4f62dc0c0733fdea5da30bde6678936f437fa02553db7db4d14288925be4736f41e94d4fb1a53fb7c05c86903ba27de4fd3e82ebfe22d981cba4207177edf36f67ce35821f8d4e238f9c869034847cd4fd3e8d4fb70513f1c05c882c71ea5c9230676c055f834e21cda4c69803a8496c1d3e802aa70323f1c8fcc0729639bbc8c7cead42114d4ab7cbaccbdce63d5946e37943cfbe25e9811052b8903be4adec1d376c0fb3153e2fadabf690367473df4d3948e4d70320411da42078066df9ff67ce36621f85e4f878fc83929674a3d4ff0a23c4d1a32044d8fca89033a4a941d1e94d04d07d4fb80fbc8698f6f4abc4fd3e8cf8f52027c1cba286929846976f4f8e3588f4526b638f9bf69253acf964cd3fa7b8f3df14f4df9466903be4a3623f8765848f865041cf9bash-4.1$ 
