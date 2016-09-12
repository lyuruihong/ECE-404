from BitVector import *

class RC4:
	enc_key = ''
	def __init__(self, key):
		enc_key = key
	def encrypt(self, imagePointer):
		self.enc_key = BitVector(textstring = self.enc_key)
		list_image = imagePointer.readlines()
		S = []
		T = []
		encryption_byte = []
		header = []
		for I in range(3):
			header.append(list_image[0])
			del list_image[0]
		for I in range(0xFF):
			S.append(I)
		S.append(0xFF)
		for I in range(256):
			T.append(self.enc_key[I % 16])
		j  =  0
		temp = S[0]
		for i in range(256):
			j  =  ( j + S[i] + T[i] )  %  256
			temp = S[i]
			S[i] = S[j]
			S[j] = temp
		i, j  =  0
		for x in range(len(list_image)):
			i  =  ( i + 1 )  % 256
			j  =  ( j + S[i] )  %  256
			temp = S[i]
			S[i] = S[j]
			S[j] = temp
			k  =  ( S[i]  +  S[j] )  % 256
			list_image[x] = list_image[x] ^ S[k]
		with open('encryted.ppm') as fp:
			for x in range(3):
				fp.write(header[x])
			for x in range(len(list_image)):
				fp.write(list_image[x])
if __name__ == "__main__":
	rc4 = RC4('1234512345123456')
	fp = open('winterTown.ppm', 'r')
	rc4.encrypt(fp)
	fp.close()
		
