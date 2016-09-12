    bv = BitVector( filename = input_file )
    FILEOUT = open( output_file, 'wb' )
    while bv.more_to_read:
        bitvec = bv.read_bits_from_file( 64 )   ## assumes that your file has an integral
        modulo = bitvec.length() % 64
        if not modulo == 0:
			bitvec.pad_from_right(64 - modulo)
    	[LE, RE] = bitvec.divide_into_two()
        round_key = extract_round_key(key)      
    	for i in range(16):        
        	## write code to carry out 16 rounds of processing
			temp = RE
			RE = RE.permute(expansion_permutation)
			if encrypt_or_decrypt == "encrypt":
				RE = RE ^ round_key[i]
			else:
				RE = RE ^ round_key[15 - i]
			first = 0
			middle = 1
			last = 5
			bv2 = BitVector(size = 32)
			for I in range(8):
				J = 2 * RE[first] + RE[last]
				K = 8 * RE[middle] + 4 * RE[middle + 1] + 2 * RE[middle + 2] + RE[middle + 3]
				sbox_bv = BitVector(intVal = int(s_box[I][J][K]), size = 4)
				bv2 += sbox_bv
				first = first + 6
				middle = middle + 6
				last = last + 6
			bv2 = bv2.permute(p_box_permutation)
			LE = LE ^ bv2
			RE = LE   
			LE = temp
        bitvec = RE + LE
        FILEOUT.write(bitvec.get_text_from_bitvector())
	FILEOUT.close()
