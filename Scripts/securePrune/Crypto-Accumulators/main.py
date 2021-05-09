import secrets

from helpfunctions import *

RSA_KEY_SIZE = 2048 # RSA key size for 128 bits of security
RSA_PRIME_SIZE = int(RSA_KEY_SIZE / 2)
ACCUMULATED_PRIME_SIZE = 128 # take from: LLX, "Universal accumulators with efficient nonmembership proofs", construction 1


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

def batch_add(A_pre_add, S, x_list, n):
	product = 1
	for x in x_list:
		if x not in S.keys():
			hash_prime, nonce = hash_to_prime(x)
			S[x] = nonce
			product *= hash_prime
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
	primes = [hash_to_prime(x=x, num_of_bits = ACCUMULATED_PRIME_SIZE, nonce=S[x])[0] for x in S.keys()]
	#print(primes)
	return root_factor(A0, primes, n)
	
def root_factor(g, primes, N):
	n = len(primes)
	if n == 1:
		return [g]
		
	n_tag = n // 2
	primes_L = primes[0:n_tag]
	product_L = calculate_product(primes_L)
	#print('product_L', product_L)
	g_L = pow(g, product_L, N)
	#print('g_L', g_L)
	
	primes_R = primes[n_tag:n]
	product_R = calculate_product(primes_R)
	#print('product_R', product_R)
	g_R = pow(g, product_R, N)
	#print('g_R',g_R)
	
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
	
#n, A0, S = setup()
#print(n)
# print(n)
# print(A0)
# print(A0 < n)
# print(S)

# # Addition of an element to Accumulator
# x  = secrets.randbelow(pow(2, 256))
# A1 = add(A0, S, x, n)

# # Addition of second element to A1
# y = secrets.randbelow(pow(2,256))
# A2 = add(A1, S, y, n)

# Anew = delete(A0, A2, S, y, n)
# #print(Anew == A1)

# #print(A0)
# #print(x)
# #print(A1)
# nonce = S[x]
# #print(nonce)
# A2 = add(A1, S, y, n)

# proof = prove_menbership(A0, S, y, n)
# nonce = S[y]
# prime = hash_to_prime(x=y, nonce=nonce)[0]
# A2_proof = pow(proof, prime, n)
# if (A2 == A2_proof):
	# print("prooof for y is correct")
	
# y_prime = hash_to_prime(y,nonce = nonce)[0]
# y_nonce = S[y]
# Q, l_nonce = prove_exponetiation(A1, y_prime, A2, n)
# b = verify_exponentiation(Q, l_nonce, A1, y, y_nonce, A2, n)
# print(b)
# if b:
	# print("NI-PoE is verified successfully for y")
	
# z = secrets.randbelow(pow(2, 256))
# z_prime, z_nonce = hash_to_prime(z,num_of_bits = ACCUMULATED_PRIME_SIZE)
# d, b = prove_non_membership(A0, S, z, z_nonce, n)

# b = verify_non_membership(A0, A2, d, b, z, z_nonce, n)
# if b:
	# print("Non-membership of z is verified successfully")

#x_list = [secrets.randbelow(pow(2,256)) for i in range(4)]
#print(x_list)

# A = batch_add(A2, S, x_list, n)[0]
# print(A2)
# print(A)
# proof = batch_prove_membership(A0, S, x_list, n)
# print(proof == A2)
# nonce_list = [hash_to_prime(x)[1] for x in x_list]
# print(nonce_list)

# b = batch_verify_membership(A, x_list, nonce_list, proof, n)
# if b:
	# print("Batch membership of x_list verified successfully")

#A = batch_add(A0, S, x_list, n)
#print(S)	
#witnesses_list = create_all_membership_witnesses(A0, S, n)
#print(witnesses_list)

# primes = []
# for i in range(len(x_list)):
	# print(x_list[i], S[x_list[i]])
	# #prime = hash_to_prime(x_list[i], ACCUMULATED_PRIME_SIZE, S[x_list[i]])[0]
	# #primes.append(primes)
	# print(witnesses_list[i])
	# b = verify_membership(A, x_list[i], S[x_list[i]], witnesses_list[i], n)
	# if b:
		# print('Memebrship proof for %d is verified successfully' %i)
