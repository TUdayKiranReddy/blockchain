import secrets 
import math
from helpfunctions import *
from main import *
from unittest import TestCase
import time
import threading

def create_list(size):
	res = []
	for x in range(size):
		x = secrets.randbelow(pow(2,256))
		res.append(x)
	return res
	


class AccumulatorTest():
	def test_hash_to_prime(self):
		x = secrets.randbelow(pow(2,256))
		h, nonce = hash_to_prime(x, 128)
		#self.assertTrue(is_prime(h))
		#self.assertTrue(h, math.log2(h) < 128)
		print(is_prime(h))
		print(math.log2(h) < 128)
		
	def test_add_and_delete_element(self):
		x1 = secrets.randbelow(pow(2,256))
		x2 = secrets.randbelow(pow(2,256))
		
		n, A0, S = setup()
		# Add first element
		A1 = add(A0, S, x1, n)
		nonce = S[x1]
		
		proof = prove_membership(A0, S, x1, n)
		print(len(S) == 1)
		print(A0 == proof)
		print('Verification of membership proof of x1 : %s' %(verify_membership(A1, x1, nonce, proof, n)))
	
		# second addition
		A2 = add(A1, S, x2, n)
		nonce = S[x2]
		proof = prove_membership(A0, S, x2, n)
		print(len(S) == 2)
		print(A1 == proof)
		print('Verification of membership proof of x2 : %s' %(verify_membership(A2, x2, nonce, proof, n)))

		# delete
		A1_new = delete(A0, A2, S, x1, n)
		proof = prove_membership(A0, S, x2, n)
		proof_none = prove_membership(A0, S, x1, n)
		print(len(S) == 1)
		print(A0 == proof)
		print(proof_none == None)
		print('Verification of membership proof of x2 : %s' %(verify_membership(A1_new, x2, nonce, proof, n)))

	def test_proof_of_exponent(self):
		# do regular accumulation
		n, A0, S = setup()
		x1 = secrets.randbelow(pow(2,256))
		x2 = secrets.randbelow(pow(2,256))
		A1 = add(A0, S, x1, n)
		A2 = add(A1, S, x2, n)
		
		Q, l_nonce, u = prove_membership_with_NIPoE(A0, S, x1, n, A2)
		is_valid = verify_exponentiation(Q, l_nonce, u, x1, S[x1], A2, n)
		print("Verification of membership proof with NI-PoE for element x1: %s" %(is_valid))
		
		
	def test_batch_add(self):
		n, A0, S = setup()
		
		elements_list = create_list(2000)
		#print(elements_list)
		A = A0
		for x in elements_list:
			A = add(A, S, x, n)
		A_final = A
		S = dict()
		t1 = time.time()
		print('start=', t1)
		A_batch_final, nipoe = batch_add(A0, S, elements_list, n)
		t2 = time.time()
		print('stop=', t2)
		print(t2-t1)
		print(A_final == A_batch_final)
		nonces_list = list(map(lambda e: hash_to_prime(e)[1], elements_list))
		#print(nonces_list)
		is_valid = batch_verify_membership_with_NIPoE(nipoe[0], nipoe[1], A0, elements_list, nonces_list, A_batch_final, n)
		print(is_valid)
		
	def test_batch_proof_of_membership(self):
		n, A0, S = setup()
		
		elements_list = create_list(10)
		
		A = A0
		for x in elements_list:
			A = add(A, S, x, n)
		A_final = A
		
		elements_to_prove_list = [elements_list[4], elements_list[7], elements_list[8]]
		A_intermediate  = batch_prove_membership(A0, S, elements_to_prove_list, n)
		nonces_list = list(map(lambda e: hash_to_prime(e)[1], elements_to_prove_list))
		is_valid = batch_verify_membership(A_final, elements_to_prove_list, nonces_list, A_intermediate, n)
		
		print(is_valid)
		
	def test_batch_proof_of_membership_with_NIPoE(self):
		 n, A0, S = setup()
		 elements_list = create_list(10)
		 
		 A = A0
		 for x in elements_list:
			 A = add(A, S, x, n)
		 A_final = A
		 
		 elements_to_prove_list = [elements_list[4], elements_list[7], elements_list[8]]
		 Q, l_nonce, u = batch_prove_membership_with_NIPoE(A0, S, elements_to_prove_list, n, A_final)
		 nonces_list = list(map(lambda e: hash_to_prime(e)[1], elements_to_prove_list))
		 is_valid = batch_verify_membership_with_NIPoE(Q, l_nonce, u, elements_to_prove_list, nonces_list, A_final, n)
		 print(is_valid)
		 
	def test_shamir_trick(self):
		n = 23
		A0 = 2
		
		prime1 = 3
		prime2 = 5
		
		A1 = pow(A0, prime1, n)
		A2 = pow(A1, prime2, n)
		print(A1, A2)
		proof1 = pow(A0, prime2, n)
		proof2 = pow(A0, prime1, n)
		print(proof1, proof2)
		agg_proof = shamir_trick(proof1, proof2, prime1, prime2, n)
		power = pow(agg_proof, prime2 * prime1, n)
		
		print(power == A2)
		
	def test_shamir_trick_2(self):
		n, A0, S = setup()
		
		elements_list = create_list(2)
		
		A1 = add(A0, S, elements_list[0], n)
		A2 = add(A1, S, elements_list[1], n)
		
		prime0 = hash_to_prime(elements_list[0], nonce=S[elements_list[0]])[0]
		prime1 = hash_to_prime(elements_list[1], nonce=S[elements_list[1]])[0] 		
		
		proof0 = prove_membership(A0, S, elements_list[0], n)
		proof1 = prove_membership(A0, S, elements_list[1], n)
		
		tik = time.time()
		agg_proof = shamir_trick(proof0, proof1, prime0, prime1, n)
		tok = time.time()
		print(tok-tik)
		
		is_valid = pow(agg_proof, prime0 * prime1, n) == A2
		print(is_valid)
		
	def test_prove_non_membership(self):
		n, A0, S = setup()
		
		elements_list = create_list(3)
		
		A1 = add(A0, S, elements_list[0], n)
		A2 = add(A1, S, elements_list[2], n)
		A3 = add(A2, S, elements_list[2], n)
		
		proof = prove_non_membership(A0, S,elements_list[0], S[elements_list[0]], n)
		print(proof)
		
		x = create_list(1)[0]
		prime, x_nonce = hash_to_prime(x)
		proof = prove_non_membership(A0, S, x, x_nonce, n)
		is_valid = verify_non_membership(A0, A3, proof[0], proof[1], x, x_nonce, n)
		print(is_valid)
		
	def test_batch_delete(self):
		n, A0, S = setup()
		
		elements_list = create_list(100)
		
		A = A0
		for i in range(len(elements_list)):
			A = add(A, S, elements_list[i], n)
		A_pre_delete = A
		
		
		elements_to_delete_list = elements_list[0:50]
		nonces_list = list(map(lambda e: hash_to_prime(e)[1], elements_to_delete_list))
		
		#tik = time.time()
		#proofs = list(map(lambda x: prove_membership(A0, S, x, n), elements_to_delete_list))
		#tok = time.time()
		#print(tok-tik)
		
		tik = time.time()
		proofs = list(create_all_membership_witnesses(A0, S, n))
		tok = time.time()
		print(tok-tik)
		
		print(len(proofs))
		t1 = time.time()
		A_post_delete, nipoe = batch_delete_using_membership_proofs(A_pre_delete, S, elements_to_delete_list, proofs[0:50], n)
		t2 = time.time()
		print(t2-t1)
		is_valid = batch_verify_membership_with_NIPoE(nipoe[0], nipoe[1], A_post_delete, elements_to_delete_list, nonces_list, A_pre_delete, n)
		print(is_valid)
		
	def test_create_all_membership_witnesses(self):
		n, A0, S = setup()
		
		elements_list = create_list(2000)
		
		A1, nipoe = batch_add(A0, S, elements_list, n)
		tik = time.time()
		witnesses = create_all_membership_witnesses(A0, S, n)
		tok = time.time()
		print(tok-tik)
		elements_list = list(S.keys())
		
		#for i, witness in enumerate(witnesses):
		#	print(verify_membership(A1, elements_list[i], S[elements_list[i]], witness, n))
	
	def test_agg_mem_witnesses(self):
		n, A0, S = setup()
		
		elements_list = create_list(100)
		
		
		A1, nipoe = batch_add(A0, S, elements_list, n)
		tik = time.time()
		witnesses = create_all_membership_witnesses(A0, S, n)
		tok = time.time()
		print(tok-tik)
		elements_list = list(S.keys())
		
		#for i, witness in enumerate(witnesses):
		#	print(verify_membership(A1, elements_list[i], S[elements_list[i]], witness, n))
		
		nonces_list = [S[x] for x in elements_list]
		#print(elements_list)
		#print(nonces_list)
		tik = time.time()
		agg_wit, nipoe = aggregate_membership_witnesses(A1, witnesses, elements_list, nonces_list, n)
		tok = time.time()
		print(tok-tik)
		#print(agg_wit)
		#print(A1)
		is_valid = batch_verify_membership_with_NIPoE(nipoe[0], nipoe[1], agg_wit, elements_list, nonces_list, A1, n)
		#print(is_valid)
		
	def test_batch_delete_using_product(self):
		n, A0, S = setup()
		
		elements_list = create_list(1e4)
		
		tik = time.time()
		nonce_list = list(map(lambda e: hash_to_prime(e)[1], elements_to_delete_list))
		primes_list = [hash_to_prime(x, nonce=nonce_list[i])[0] for i, x in enumerate(elements_to_delete_list)]
		p = calculate_product(primes_list)
		A_pre_delete = pow(A0, p, n)

		tok = time.time()
		print(tok-tik)
		
		# elements_to_delete_list = elements_list
		# t3 = time.time()
		# nonce_list = list(map(lambda e: hash_to_prime(e)[1], elements_to_delete_list))
		# primes_list = [hash_to_prime(x, nonce=nonce_list[i])[0] for i, x in enumerate(elements_to_delete_list)]
		# p = calculate_product(primes_list)
		
		# p_inv = mul_inv(p, n)
		# A_post_delete = pow(A_pre_delete, p_inv, n)
		# t4 = time.time()
		# print(t4-t3)
		# print(A0 == A_post_delete)
		
	def test_mul_inv(self):
		n, A0, S = setup()
		x = secrets.randbelow(pow(2,256))
		A = pow(2,7,11)
		print(A)
		x_inv = mul_inv(7, 11)
		print(x_inv)
		A1 = pow(A,x_inv,11)
		print(A1)
		print(A1 == A0)
		
	
		

#x_list = create_list(8)
#print(x_list)

Acc_test = AccumulatorTest()
#Acc_test.test_hash_to_prime()
#Acc_test.test_add_and_delete_element()
#Acc_test.test_proof_of_exponent()
#Acc_test.test_batch_add()
#Acc_test.test_batch_proof_of_membership()
#Acc_test.test_batch_proof_of_membership_with_NIPoE()
#Acc_test.test_shamir_trick()
#Acc_test.test_shamir_trick_2()
#Acc_test.test_prove_non_membership()
Acc_test.test_batch_delete()
#Acc_test.test_create_all_membership_witnesses()
#Acc_test.test_agg_mem_witnesses()
#Acc_test.test_batch_delete_using_product()
#Acc_test.test_mul_inv()
