#!/usr/bin/python
## OTP - Recovering the private key from a set of messages that were encrypted w/ the same private key (Many time pad attack) - crypto100-many_time_secret @ alexctf 2017
# @author intrd - http://dann.com.br/ 
# Original code by jwomers: https://github.com/Jwomers/many-time-pad-attack/blob/master/attack.py)

import string
import collections
import sets, sys

# 11 unknown ciphertexts (in hex format), all encrpyted with the same key
c1 = "36076737827353793867244539398877415934772302844661661429780202810526038562905903431382128591047475128797766365677866518707086694481226279266031268631913271705722075931730147289563964486320833615729757435300700161354410066393028868594800015642006497075255616465281433155871757336218649636181962588042565306568"
c2 = "35132575378143759269451501454463373404138237113858021523457198123415780722310393697155636055924122393096995527421788032468848569747956201261829522323294473910960652263668755170535901482689193628403189397764415823064172307932671365638592830197136985487433464291676856234441262994722754142522820930605409268511"
c3 = "20379600371500173560250544224517539350052498703017496027023092471995383477807276396902626460080559809126859704411756277972588763455323486503929107751145699946241527479395485774824803064971585583593151831829899820350903358281193449616619873552994442033184395479170225918778026684773220388274909444988988370727"
c4 = ""
c5 = "283f652c2b31661426292b653a292c372a2f20212a316b283c09"
c6 = "29232178373c270f682c216532263b2d3632353c2c3c2a293504"
c7 = "613c37373531285b3c2a72273a67212a277f373a243c20203d5d"
c8 = "243a202a633d205b3c2d3765342236653a2c7423202f3f652a18"
c9 = "2239373d6f740a1e3c651f207f2c212a247f3d2e65262430791c"
c10 = "263e203d63232f0f20653f207f332065262c3168313722367918"
c11 = "2f2f372133202f142665212637222220733e383f2426386b"
ciphers = [c1, c2, c3]
# The target ciphertext we want to crack
target_cipher = "17482644844951175640843255713372869422739097498066773957636359990466096121278949693816080016671592558403643716793132479255285512907247513385850323834210899918531077167485767118313722022095603863840851451191536627814100144146010392752308431038754246815068245448456643024387011488032896209253644172833489422733"

# XORs two string
def strxor(a, b):     # xor two strings (trims the longer input)
    return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b)])

# To store the final key
final_key = [None]*150
# To store the positions we know are broken
known_key_positions = set()

# For each ciphertext
for current_index, ciphertext in enumerate(ciphers):
	counter = collections.Counter()
	# for each other ciphertext
	for index, ciphertext2 in enumerate(ciphers):
		if current_index != index: # don't xor a ciphertext with itself
			for indexOfChar, char in enumerate(strxor(ciphertext.decode('hex'), ciphertext2.decode('hex'))): # Xor the two ciphertexts
				# If a character in the xored result is a alphanumeric character, it means there was probably a space character in one of the plaintexts (we don't know which one)
				if char in string.printable and char.isalpha(): counter[indexOfChar] += 1 # Increment the counter at this index
	knownSpaceIndexes = []

	# Loop through all positions where a space character was possible in the current_index cipher
	for ind, val in counter.items():
		# If a space was found at least 7 times at this index out of the 9 possible XORS, then the space character was likely from the current_index cipher!
		if val >= 7: knownSpaceIndexes.append(ind)
	#print knownSpaceIndexes # Shows all the positions where we now know the key!

	# Now Xor the current_index with spaces, and at the knownSpaceIndexes positions we get the key back!
	xor_with_spaces = strxor(ciphertext.decode('hex'),' '*150)
	for index in knownSpaceIndexes:
		# Store the key's value at the correct position
		final_key[index] = xor_with_spaces[index].encode('hex')
		# Record that we known the key at this position
		known_key_positions.add(index)

# Construct a hex key from the currently known key, adding in '00' hex chars where we do not know (to make a complete hex string)
final_key_hex = ''.join([val if val is not None else '00' for val in final_key])
# Xor the currently known key with the target cipher
output = strxor(target_cipher.decode('hex'),final_key_hex.decode('hex'))

print "Fix this sentence:"
print ''.join([char if index in known_key_positions else '*' for index, char in enumerate(output)])+"\n"

# WAIT.. MANUAL STEP HERE 
# This output are printing a * if that character is not known yet
# fix the missing characters like this: "Let*M**k*ow if *o{*a" = "cure, Let Me know if you a"
# if is too hard, change the target_cipher to another one and try again
# and we have our key to fix the entire text!

#sys.exit(0) #comment and continue if u got a good key

target_plaintext = "cure, Let Me know if you a"
print "Fixed:"
print target_plaintext+"\n"

key = strxor(target_cipher.decode('hex'),target_plaintext)

print "Decrypted msg:"
for cipher in ciphers:
	print strxor(cipher.decode('hex'),key)

print "\nPrivate key recovered: "+key+"\n"
