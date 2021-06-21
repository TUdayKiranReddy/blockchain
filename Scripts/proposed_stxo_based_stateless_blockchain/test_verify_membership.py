import secrets
import time
import threading
import queue
import tracemalloc
import os
import resource
import matplotlib.pyplot as plt
from helpfunctions import *
import merkletools
import numpy as np
from main import *


# Proposed
i = 10

n, A0, S_STXO = setup()
S_TXO = dict()

x = create_list(i)
y = create_list(2*i)


STXO_C, nipoe = batch_add(A0, S_STXO, x, n)
TXO_C, nipoe = batch_add(A0, S_TXO, y, n)

Q_STXO, l_nonce_STXO, u_STXO = batch_prove_membership_with_NIPoE(A0, S_STXO, x, n, STXO_C)
Q_TXO, l_nonce_TXO, u_TXO = batch_prove_membership_with_NIPoE(A0, S_TXO, y, n, TXO_C)


tik = time.time()
nonces_list_STXO = [hash_to_prime(xi)[1] for xi in x]
if batch_verify_membership_with_NIPoE(Q_STXO, l_nonce_STXO, u_STXO, x, nonces_list_STXO, STXO_C, n):
	print("STXO_C Batch Membership Verified.")
else:
	print("STXO_C Batch Membership Not Verified!")
tiok  = time.time()

nonces_list_TXO = [hash_to_prime(yi)[1] for yi in y]
if batch_verify_membership_with_NIPoE(Q_TXO, l_nonce_TXO, u_TXO, y, nonces_list_TXO, TXO_C, n):
	print("TXO_C Batch Membership Verified.")
else:
	print("TXO_C Batch Membership Not Verified!")

tok = time.time()	
print("Total Transactions: ", 3*i)
print("Total Time taken: {} seconds".format(tok-tik))
print("Time taken by STXO Set: {} seconds".format(tiok-tik))
print("Time taken by TXO Set: {} seconds".format(tok-tiok))
print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
