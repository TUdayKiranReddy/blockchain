import secrets 
import math
from helpfunctions import *
from main import *
from unittest import TestCase
import time
import threading
import matplotlib.pyplot as plt
import random

def create_list(size):
	res = []
	for x in range(size):
		x = secrets.randbelow(pow(2,256))
		res.append(x)
	return res


n, A0, S = setup()

x = create_list(100)
#print(x)

tik = time.time()
A,nipoe = batch_add(A0,S,x,n)
W = create_all_membership_witnesses(A0, S, n)
tok = time.time()
print(tok-tik)
proofs = dict()
i = 0
for x in S.keys():
	proofs[x] = W[i]
	i += 1
	
print(len(proofs))
	
n_blocks = 1000
Acc = dict()
Acc[0] = A
for i in range(1,50):
	size_of_utxo = len(S)
	print(size_of_utxo)
	n_tx_per_block = random.randint(int(size_of_utxo/5),int(size_of_utxo/4))
	n_inputs = random.randint(1,3)
	n_outputs = random.randint(1,3)
	S_d = dict()
	print(n_tx_per_block,n_inputs,n_outputs)
	
	
	tik = time.time()
	
	for utxo in S.keys():
		S_d[utxo] = S[utxo]
		#del S[utxo]
		#print(S_d[utxo])
		if len(S_d) == n_tx_per_block*n_inputs:
			break
	#print(S_d)
	#print(len(S_d))
	
	
	proofs_list = []
	#members = []
	for x in S_d.keys():
		proofs_list.append(proofs[x])
		#members.append(hash_to_prime(x, ACCUMULATED_PRIME_SIZE, S[x])[0])
		#del S[x]
		#print(x_list[x])
	print(len(S))
	print(len(S_d))
	#A_pre_delete = A[i-1]
	A_post, product, nipoe = batch_delete_using_membership_proofs(Acc[i-1], S, S_d, proofs_list, n)
	tok = time.time()
	print(tok-tik)
	# for x in S_d.keys():
		 # del S[x]
		# del proofs[x]
	
	# Update witnesses	
	# for x in S.keys():
		# proof = shamir_trick(A_post,proofs[x],product,x,n)
		# proofs[x] = proof
	# for x in S.keys():
		# for y in S_d.keys():
			# proof1 = shamir_trick(proofs[x], proofs[y],x,y,n)
			# proofs[x] = proof1
	
	tik = time.time()
	y = create_list(n_tx_per_block*n_outputs)
	A_final,nipoe_add = batch_add(A_post, S, y, n)
	Acc[i] = A_final
	W = create_all_membership_witnesses(A0,S,n)
	j = 0
	for x in S.keys():
		proofs[x] = W[j]
		j += 1
	tok = time.time()
	print(tok-tik)
	# tik = time.time()
	# members = []
	# proofs_list = []
	# for utxo in S.keys():
		# members.append(hash_to_prime(utxo, ACCUMULATED_PRIME_SIZE, S[utxo])[0])
		# proofs_list.append(proofs[utxo])
		# if len(members) == n_tx_per_block*n_inputs:
			# break
	# A_post_delete = proofs_list[0]
	# product = members[0]
	
	# for j in range(1,len(members)):
		# A_post_delete = shamir_trick(A_post_delete, proofs_list[j], product, members[j], n)
		# product *= members[j]
	# nipoe_delete = prove_exponentiation(A_post_delete, product, Acc[i-1], n)
	# tok = time.time()
	# print(tok-tik)	
	# print(A_post_delete == A_post)
	# print(len(S))
	# print(len(proofs))
	# witness_update_after_batch_delete(A_post_delete, S, proofs,n)
	 
		
		

#print(S)
#print(A)
#print(nipoe)

# time_to_batch_add = []
# num = []
# for i in range(10):
	# x = create_list(i*100)
	# tik = time.time()
	# A,nipoe = batch_add(A0,S,x,n)
	# W = create_all_membership_witnesses(A0, S, n)
	# tok = time.time()
	# num.append(i*100)
	# time_to_batch_add.append(tok-tik)
	
# plt.plot(num,time_to_batch_add)
# #plt.grid()
# plt.xlabel('num of utxos added to Accumulator+inclusion proofs of all utxo')
# plt.ylabel('time in sec')
# plt.grid()
# plt.savefig('./figs/batch_add_proofs.pdf')
# plt.savefig('./figs/batch_add_proofs.eps')
# plt.show()

# x_list = x
# tik = time.time()
# nonce_list = list(map(lambda e: hash_to_prime(e)[1], x_list))
# primes_list = [hash_to_prime(x, nonce=nonce_list[i])[0] for i, x in enumerate(x_list)]
# p = calculate_product(primes_list)
# A_post_add = pow(A0, p, n)
# nipoe = prove_exponentiation(A0, p, A_post_add, n)
# tok = time.time()
# print(tok-tik)

# x_list = x
# S = dict()
# tik = time.time()
# hashes = []
# for x in x_list:
	# if x not in S.keys():
		# hash_prime, nonce = hash_to_prime(x)
		# S[x] = nonce
		# hashes.append(hash_prime)
			
# product = calculate_product(hashes)
# A_post_add = pow(A0, product, n)
# nipoe = prove_exponentiation(A0, product, A_post_add, n)
# W = root_factor(A0, hashes, n)
# tok = time.time()
# print(tok-tik)
#print(S)
#print(A_post_add)
#print(nipoe)	


