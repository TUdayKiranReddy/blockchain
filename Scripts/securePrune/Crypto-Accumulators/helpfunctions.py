import random
import hashlib
import secrets
import math

def is_prime(num):
	if num < 2:
		return False    # 0,1, negative numbers are not prime
		
	# About 1/3 of the time we can quickly determine if num is not prime
	# by dividing by the first few dozen prime numbers. This is quicker 
	# thna rabin_muller(), but unlike rabin_muller() is not guarantees to 
	# prove that a number is prime
	
	lowPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]
	
	if num in lowPrimes:
		return True
		
	# see if low primes can divide num
	for prime in lowPrimes:
		if(num % prime == 0):
			return False
			
	# If all else fails, call rabin_muller() to determine if num is a prime
	
	return rabin_muller(num)



def rabin_muller(num):
	
	s = num-1
	t = 0
	while s % 2 == 0:
		s = s // 2
		t += 1
		
	for trails in range(5):
		a = random.randrange(2, num - 1)
		v = pow(a,s,num)
		if v != 1 :
			i = 0
			while v != num-1 :
				if i == t-1 :
					return False
				else:
					i += 1
					v = (v ** 2) % num
					
	return True
	
def generate_large_prime(num_of_bits):
	while True:
		num = secrets.randbelow(pow(2,num_of_bits))
		if is_prime(num):
			return num
			
def generate_two_distinct_primes(num_of_bits):
	p = generate_large_prime(num_of_bits)
	while True:
		q = generate_large_prime(num_of_bits)
		if q != p :
			return p, q
	
	
	
def xgcd(b,a):
	x0, x1, y0, y1 = 1, 0, 0, 1
	while a != 0:
		q, b, a = b // a, a, b%a
		x0, x1 = x1, x0 - q * x1
		y0, y1 = y1, y0 - q * y1
		
	return b, x0, y0
	
def mul_inv(b,n):
	g, x, _ = xgcd(b,n)
	if g == 1:
		return x % n	

def bezout_coefficients(a,b):
	o = xgcd(a, b)
	return o[1], o[2]

def concat(*arg):
	res = ""
	for i in range(len(arg)):
		res += str(arg[i])
	return int(res)	
	
def calculate_product(lst):
	r = 1
	for x in lst:
		r *= x
	return r	
	
def hash_to_length(x, num_of_bits):
	pseudo_random_hex_string = ""
	num_of_blocks = math.ceil(num_of_bits / 256)
	for i in range(num_of_blocks):
		pseudo_random_hex_string += hashlib.sha256(str(x + i).encode()).hexdigest()
		
	if num_of_bits % 256 > 0:
		pseudo_random_hex_string = pseudo_random_hex_string[int((num_of_bits % 256)/4):] # we do assume divisible by 4
	return int(pseudo_random_hex_string, 16)
	
def hash_to_prime(x, num_of_bits=128, nonce=0):
	while True:
		num = hash_to_length(x + nonce, num_of_bits)
		if is_prime(num):
			return num, nonce
		nonce = nonce + 1
			
def shamir_trick(pi1, pi2, x1, x2, n):
	# we omit the validity check of (x1^pi1 == x2^pi2) for perfomance reasons, assume caller validates
	
	# find a,b s.t. a*x + b*y = 1 (mod n)
	a,b = bezout_coefficients(x1, x2)
	if a < 0:
		positive_a = -a
		inverse_pi2 = mul_inv(pi2, n)
		power1 = pow(pi1, b, n)
		power2 = pow(inverse_pi2, positive_a, n)
		
	elif b < 0 :
		positive_b = -b
		inverse_pi1 = mul_inv(pi1, n)
		power1 = pow(inverse_pi1, positive_b, n)
		power2 = pow(pi2, a, n)
	else:
		power1 = pow(pi1, b, n)
		power2 = pow(pi2, a, n)
		
	pi = power1 * power2
	return pi
			
# print(is_prime(120671))
	
# b = is_prime(99701321131212323)
# print(b)

# b = rabin_muller(9970132231312312454327641)
# print(b)
# num_of_bits = 128
# # num = secrets.randbelow(pow(2, num_of_bits))	
# # print(num)	
# # print(is_prime(num))
	
# p = generate_large_prime(num_of_bits)
# print(p)

# p, q = generate_two_distinct_primes(num_of_bits)
# print(p, q)

g, a, b = xgcd(58109,2579)
print(g)

# x = 3
# n = 7
# m = mul_inv(x,n)
# print(m)
	
# a, b = bezout_coefficients(55,15)
# print(a, b)	
	
# #s = concat(["swaroop","swarupa","Rithanyaa","Srivathsava"])
# #print(s)
	
# r = calculate_product([1,2,3,4,5])
# print(r)	
	
	
	
# print(generate_large_prime(256))
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
		
