import secrets 
import math
from helpfunctions import *
from main import *
from unittest import TestCase
import time
import threading
import matplotlib.pyplot as plt
import random
import numpy as np

from matplotlib import rc

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
#print(tok-tik)
proofs = dict()
i = 0
for x in S.keys():
	proofs[x] = W[i]
	i += 1
	
#print(len(proofs))
	
n_blocks = 1000
Acc = dict()
Acc[0] = A
n_tx_per_block = 10
n_inputs = 1
n_outputs = 1
t1 = np.zeros(10)
t2 = np.zeros(10)
t = np.zeros(10,dtype = int)
t[0] = 10
for i in range(1,10):
	size_of_utxo = len(S)
	print(size_of_utxo)
	#n_tx_per_block = random.randint(int(size_of_utxo/5),int(size_of_utxo/4))
	#n_inputs = random.randint(1,3)
	#n_outputs = random.randint(1,5)
	
	S_d = dict()
	print(n_tx_per_block,n_inputs,n_outputs)
	
	for utxo in S.keys():
		S_d[utxo] = S[utxo]
		if len(S_d) == n_tx_per_block*n_inputs:
			break
	
	
	proofs_list = []
	for x in S_d.keys():
		proofs_list.append(proofs[x])
		
	print(len(S))
	print(len(S_d))
	
	A_post, product, nipoe = batch_delete_using_membership_proofs(Acc[i-1], S, S_d, proofs_list, n)
	
	# product1 = 1
	# for x in S_d.keys():
		# product1 *= hash_to_prime(x,128,0)[0]
	# print(product == product1)
	# nonce = hash_to_prime(product,128,nonce=0)[1]
	# print(nonce)
	# nonce1 = hash_to_prime(product1,128,nonce=0)[1]
	# print(nonce)
	# print(nonce == nonce1)
	
	# print(pow(A_post,product1,n) == Acc[i-1])
	
	tik = time.time()
	nonces_list = list(map(lambda e: hash_to_prime(e)[1],S_d))
	is_valid = batch_verify_membership_with_NIPoE(nipoe[0], nipoe[1], A_post,S_d, nonces_list, Acc[i-1], n)
	tok = time.time()
	t1[i] = tok-tik 
	print(tok-tik)
	print(is_valid)
		
	#Acc[i] = A_post
	#isvalid_pi_d = verify_exponentiation(nipoe[0],nipoe[1],A_post,product1,nonce1,Acc[i-1],n)
	
	#print(isvalid_pi_d)
	#print(tok-tik)
	#for x in S_d.keys():
	#	del S[x]
		#del proofs[x]
	
	# Update witnesses	
	# for x in S.keys():
		# proof = shamir_trick(A_post,proofs[x],product,x,n)
		# proofs[x] = proof
	# for x in S.keys():
		# for y in S_d.keys():
			# proof1 = shamir_trick(proofs[x], proofs[y],x,y,n)
			# proofs[x] = proof1
	
	# tik = time.time()
	S_a = create_list(n_tx_per_block*n_outputs)
	
	A_final,nipoe_add = batch_add(A_post, S, S_a, n)
	
	tik = time.time()
	nonces_list = list(map(lambda e: hash_to_prime(e)[1],S_a))
	is_valid = batch_verify_membership_with_NIPoE(nipoe_add[0], nipoe_add[1], A_post,S_a, nonces_list, A_final, n)
	tok = time.time()
	t2[i] = tok-tik
	print(tok-tik)
	print(is_valid)
	Acc[i] = A_final
	W = create_all_membership_witnesses(A0,S,n)
	j = 0
	proofs = dict()
	for x in S.keys():
		proofs[x] = W[j]
		j += 1
		
	n_tx_per_block += 10
	t[i] += t[i-1] + 10

	#tok = time.time()
	# print(tok-tik)
	
f = open("t1.txt","w+")
for i in range(len(t1)):
	f.write(str(t1[i]))
	#f.write(str(miners[i].miner_links()))
f.close()

f = open("t2.txt","w+")
for i in range(len(t2)):
	f.write(str(t2[i]))
	#f.write(str(miners[i].miner_links()))
f.close()

f = open("t3.txt","w+")
for i in range(len(t1)):
	f.write(str(t1[i]+t2[i]))
	#f.write(str(miners[i].miner_links()))
f.close()

f =  open('t1.txt', 'r')
for x in f:
	print(x)

plt.rcParams['ps.useafm'] = True
rc('font',**{'family':'sans-serif','sans-serif':['FreeSans']})
plt.rcParams['pdf.fonttype'] = 42
#plt.rcParams['eps.fonttype'] = 42

plt.figure()
# plot figure...


#csfont = {'fontname':'Times New Roman'}
plt.rc('font',family='serif')
plt.rcParams['mathtext.fontset'] = 'cm'
plt.plot(t,t1,label = '$\pi_d$ (inputs)')
plt.plot(t,t2,label = '$\pi_a$ (outputs)')
plt.plot(t,t1+t2,label = '$\pi_d$ + $\pi_a$')
plt.xlabel('number of inputs/outputs',fontsize=10)
plt.ylabel('time for NI-PoE.verify (in sec)',fontsize=10)
#plt.legend(['$\pi_d$ (inputs)','$\pi_a$ (outputs)','$\pi_d$ + $\pi_a$'],loc = 'best',fontsize=10)
plt.legend(loc = 'best',fontsize=10)
plt.grid()
plt.savefig('./figs/proofs_1.eps')
plt.savefig('./figs/proofs_1.pdf')
plt.show()

# plt.plot(t2)
# plt.xlabel('n_tx')
# plt.ylabel('time for NI-PoE.verify')
# plt.grid()
# plt.show()


