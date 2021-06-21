import secrets
import time
import threading
import queue
import sys
import numpy as np
import os
import matplotlib.pyplot as plt
from helpfunctions import *

global RSA_KEY_SIZE 
RSA_KEY_SIZE = 3072 # RSA key size for 128 bits of security
global RSA_PRIME_SIZE
RSA_PRIME_SIZE = int(RSA_KEY_SIZE / 2)
global ACCUMULATED_PRIME_SIZE
ACCUMULATED_PRIME_SIZE = 128 # take from: LLX, "Universal accumulators with efficient nonmembership proofs", construction 1
global THREAD_MAX
THREAD_MAX = int(os.cpu_count())


def create_list(size):
	res = []
	for x in range(size):
		x = secrets.randbelow(pow(2,256))
		res.append(x)
	return res

def setup():
	p, q = generate_two_distinct_primes(RSA_PRIME_SIZE)
	n = p*q
	# draw random number within range of [0, n-1]
	A0 = secrets.randbelow(n)
	return n, A0, dict()

def add(A, S, x, n):
	if x in S.keys():
		#print("x is in S")
		return A
	else:
		hash_prime, nonce = hash_to_prime(x, ACCUMULATED_PRIME_SIZE)
		A = pow(A, hash_prime, n)
		S[x] = nonce
		#print(S[x])
		return A

def multi_thread_add(A_pre_add, S, x_list, n):
	product = 1

	for x in x_list:
		if x not in S.keys():
			hash_prime, nonce = hash_to_prime(x)
			S[x] = nonce
			product *= hash_prime
	return product

# def batch_add(A_pre_add, S, x_list, n):
# 	product = 1
# 	for x in x_list:
# 		if x not in S.keys():
# 			hash_prime, nonce = hash_to_prime(x)
# 			S[x] = nonce
# 			product *= hash_prime
# 	A_post_add = pow(A_pre_add, product, n)
# 	return A_post_add, prove_exponentiation(A_pre_add, product, A_post_add, n)
		

def batch_add(A_pre_add, S, x_list, n):
	x_list_len = len(x_list)
	thread_max = min(x_list_len, THREAD_MAX)

	product = 1
	que = queue.Queue()
	threads = list()
	for i in range(thread_max):
		start = int(i*x_list_len/thread_max)
		end = int((i+1)*x_list_len/thread_max)

		#threads.append(threading.Thread(target=multi_thread_add, args=(A_pre_add, S, x_list[start:end], n)))
		threads.append(threading.Thread(target=lambda q, A_pre_add, S, x_list, n: q.put(multi_thread_add(A_pre_add, S, x_list, n)), args=(que, A_pre_add, S, x_list[start:end], n)))
	for t in threads:
		t.start()
	for t in threads:
		t.join()

	while not que.empty():
		product *= que.get()

	A_post_add = pow(A_pre_add, product, n)
	return A_post_add, prove_exponentiation(A_pre_add, product, A_post_add, n)
		
def delete(A0, A, S, x, n):
	if x not in S.keys():
		return A
	else:
		del S[x]
		product = 1
		for element in S.keys():
			nonce = S[element]
			product *= hash_to_prime(element,ACCUMULATED_PRIME_SIZE,nonce = nonce)[0]
		Anew = pow(A0, product, n)
		return Anew

def batch_delete(A0, S, x_list, n):
	for x in x_list:
		del S[x]
		
	if len(S) == 0:
		return A0
	else:
		product = 1
		for element in S.keys():
			nonce = S[element]
			product *= hash_to_prime(element, ACCUMULATED_PRIME_SIZE, nonce)[0]
		Anew = pow(A0, product, n)
		return Anew  	

def prove_membership(A0, S, x, n):
	if x not in S.keys():
		return None
	else:
		product = 1
		for element in S.keys():
			if element != x:
				nonce = S[element]
				product *= hash_to_prime(element, ACCUMULATED_PRIME_SIZE, nonce)[0]
		A = pow(A0, product, n)
		return A
		
def prove_membership_with_NIPoE(g, S, x, n, w):
	u = prove_membership(g, S, x, n)
	x_prime, x_nonce = hash_to_prime(x=x, nonce=S[x])
	(Q, l_nonce) = prove_exponentiation(u, x_prime, w, n)
	return Q, l_nonce, u
	
def batch_prove_membership_with_NIPoE(A0, S, x_list, n, w):
	u = batch_prove_membership(A0, S, x_list, n)
	nonce_list = []
	for x in x_list:
		nonce_list.append(S[x])
	product = __calculate_primes_product(x_list, nonce_list)
	(Q, l_nonce) = prove_exponentiation(u, product, w, n)
	return Q, l_nonce, u
	
	
def verify_membership(A, x, nonce, proof, n):
	return __verify_membership(A, hash_to_prime(x=x, num_of_bits=ACCUMULATED_PRIME_SIZE, nonce=nonce)[0], proof, n)
	
def __verify_membership(A, x, proof, n):
	return pow(proof, x, n) == A
	
def batch_prove_membership(A0, S, x_list, n):
	product = 1
	for element in S.keys():
		if element not in x_list:
			print("Yo", element)
			nonce = S[element]
			product *= hash_to_prime(element, ACCUMULATED_PRIME_SIZE, nonce)[0]
	A = pow(A0, product, n)
	return A

def batch_verify_membership(A, x_list, nonce_list, proof, n):
	product = __calculate_primes_product(x_list, nonce_list)
	return __verify_membership(A, product, proof, n)

def batch_verify_membership_with_NIPoE(Q, l_nonce, u, x_list, nonces_list, w, n):
	product = __calculate_primes_product(x_list, nonces_list)
	return __verify_exponentiation(Q, l_nonce, u, product, w, n)	
	
def __calculate_primes_product(x_list, nonce_list):
	if len(x_list) != len(nonce_list):
		return None
	
	primes_list = [hash_to_prime(x, nonce=nonce_list[i])[0] for i, x in enumerate(x_list)]
	product = calculate_product(primes_list)
	return product
	
	

	
def prove_non_membership(A0, S, x, x_nonce, n):
	if x in S.keys():
		return None
	else:
		product = 1
		for element in S.keys():
			nonce = S[element]
			product *= hash_to_prime(element, ACCUMULATED_PRIME_SIZE, nonce)[0]
		prime = hash_to_prime(x, ACCUMULATED_PRIME_SIZE, x_nonce)[0]
		a, b = bezout_coefficients(prime, product)
		if a < 0 :
			positive_a = -a
			inverse_A0 = mul_inv(A0, n)
			d = pow(inverse_A0, positive_a, n)
		else:
			d = pow(A0, a, n)
		return d, b
		
def verify_non_membership(A0, A_final, d, b, x, x_nonce, n):
	prime = hash_to_prime(x, ACCUMULATED_PRIME_SIZE, x_nonce)[0]
	if b < 0:
		positive_b = -b
		inverse_A_final = mul_inv(A_final, n)
		second_power = pow(inverse_A_final, positive_b, n)
	else:
		second_power = pow(A_final, b, n)
	return (pow(d, prime, n) * second_power) % n == A0
	
			

# NI-POE: non-interactive version of section 3.1 BBF18 (POE)
# Receives:
# u - the accumulator value before add
# x - the (prime) element which was added to the accumulator
# w - the accumulator after the addition of x
# n - the modulus
# Returns:
# Q, x - the NIPOE
# nonce - the nonce used for hash_to_prime to receive l (for saving work to the verifier)
def prove_exponentiation(u, x, w, n):
	l, nonce = hash_to_prime(concat(x, u, w)) # Fiat-Shamir instead of interactive challenge
	q = x // l
	Q = pow(u, q, n)
	return Q, nonce

# Verify NI-PoE
# we pass l_nonce for apeed up. The verifier has to reproduce l itself
def verify_exponentiation(Q, l_nonce, u, x, x_nonce, w, n):
	x = hash_to_prime(x=x, nonce=x_nonce)[0]
	return __verify_exponentiation(Q, l_nonce, u, x, w, n)

# helper function, does not do hash_to_prime on x
def __verify_exponentiation(Q, l_nonce, u, x, w, n):
	l = hash_to_prime(concat(x, u, w), nonce=l_nonce)[0]
	r = x % l
	# check (Q^l)(u^r) == w
	return (pow(Q, l, n) % n) * (pow(u, r, n) % n) % n == w
	
def create_all_membership_witnesses(A0, S, n):
	# tik = time.time()
	primes = [hash_to_prime(x=x, num_of_bits = ACCUMULATED_PRIME_SIZE, nonce=S[x])[0] for x in S.keys()]
	# tok = time.time()
	# print(tok-tik)
	#print(primes)
	# tik = time.time()
	v = root_factor(A0, primes, n)
	# tok = time.time()
	# print(tok-tik)
	return v
	
def root_factor(g, primes, N):
	n = len(primes)
	if n == 1:
		return [g]
		
	n_tag = n // 2
	primes_L = primes[0:n_tag]
	tik = time.time()
	product_L = calculate_product(primes_L)
	#print('product_L', product_L)
	g_L = pow(g, product_L, N)
	#print('g_L', g_L)
	
	primes_R = primes[n_tag:n]
	product_R = calculate_product(primes_R)
	#print('product_R', product_R)
	g_R = pow(g, product_R, N)
	#print('g_R',g_R)
	#print(time.time()-tik);
	L = root_factor(g_R, primes_L, N)
	R = root_factor(g_L, primes_R, N)
	
	return L + R
	
def aggregate_membership_witnesses(A, witnesses_list, x_list, nonce_list, n):
	#primes = [hash_to_prime(x=x_list[i], ACCUMULATED_PRIME_SIZE, nonce=nonce_list[i])[0] for i in range(len(x_list))]
	primes = []
	for i in range(len(x_list)):
		prime = hash_to_prime(x_list[i], ACCUMULATED_PRIME_SIZE, nonce_list[i])[0]
		primes.append(prime)
	
	#print(primes)	
	agg_wit = witnesses_list[0]
	product = primes[0]
	#print(agg_wit)
	#print(product)
	for i in range(len(x_list))[1:]:
		agg_wit = shamir_trick(agg_wit,witnesses_list[i], product, primes[i], n)
		product *= primes[i]
		
	return agg_wit, prove_exponentiation(agg_wit, product, A, n)

# agg_indexes: in case proofs_list actually relate to some aggregation of the inputs in x_list, it should contain pairs
# of statr index and end index.
def batch_delete_using_membership_proofs(A_pre_delete, S, x_list, proofs_list, n, agg_indexes=[]):
	is_aggregated = len(agg_indexes) > 0
	if is_aggregated and len(proofs_list) != len(agg_indexes):
		return None
	if (not is_aggregated) and len(x_list) != len(proofs_list):
		return None
		
	members = []
	if is_aggregated:
		# sanity - verify each and every proof individually
		
		for i, indexes in enumerate(agg_indexes):
			current_x_list = x_list[indexes[0]: indexes[1]]
			current_nonce_list = [S[x] for x in current_x_list]
			product = __calculate_primes_product(current_x_list, current_nonce_list)
			members.append(product)
			for x in current_x_list:
				del S[x]
				
	else:
		for x in x_list:
			members.append(hash_to_prime(x, ACCUMULATED_PRIME_SIZE, S[x])[0])
			del S[x]
			
	A_post_delete = proofs_list[0]
	product = members[0]
	
	for i in range(1,len(members)):
		A_post_delete = shamir_trick(A_post_delete, proofs_list[i], product, members[i], n)
		product *= members[i]
		
	return A_post_delete, product, prove_exponentiation(A_post_delete, product, A_pre_delete, n)
	
def witness_update_after_batch_delete(A_post_delete,product, S, proofs, n):
	for x in S.keys():
		hash_prime = hash_to_prime(x, ACCUMULATED_PRIME_SIZE, S[x])[0]
		proofs[x] = shamir_trick(A_post_delete,proofs[x], product,x)			

x = np.arange(256, 3073)
y =[]
for xi in x:
	y.append(sys.getsizeof((1<<1024))*8)
print(x, y)