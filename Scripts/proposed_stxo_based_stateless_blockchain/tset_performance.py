import secrets
import time
import threading
import queue
import os
from main import *  
import matplotlib.pyplot as plt


TOTAL_TRANSACTINS_PER_BLOCK = 1000
RATIO_OP_IP = 2

nTXO =  int(RATIO_OP_IP*TOTAL_TRANSACTINS_PER_BLOCK/(RATIO_OP_IP+1))
nSTXO = TOTAL_TRANSACTINS_PER_BLOCK - nTXO

THREAD_MAX = int(os.cpu_count()/2)

# def BATCH_ADD(A0_STXO, A0_TXO, STXO, TXO, x_list_STXO, x_list_TXO, N_STXO, N_TXO)
# 	A_STXO,nipoe_STXO = batch_add(A0_STXO,STXO,x_list_STXO, N_STXO)
# 	A_TXO,nipoe_TXO = batch_add(A0_TXO,TXO,x_list_TXO, N_TXO)
# 	#W_STXO = create_all_membership_witnesses(A_STXO, STXO, N_STXO)
# 	#W_TXO = create_all_membership_witnesses(A_TXO, TXO, N_TXO)
# 	return A_STXO, nipoe_STXO, A_TXO, nipoe_TXO#, W_STXO, W_TXO

x_list_STXO = create_list(nSTXO)
x_list_TXO = create_list(nTXO)
y = []
#print(x)
time_to_batchAdd = []
nPoints = 10
stxo_step = int(nSTXO/nPoints)
txo_step = int(nTXO/nPoints)
for i in range(nPoints):
	n_TXO, A0_TXO, TXO = setup()
	n_STXO, A0_STXO, STXO = setup()
	
	tik = time.time()
	que = queue.Queue()
	t_TXO = threading.Thread(target=batch_add, args=(A0_TXO, TXO, x_list_TXO[0:(i+1)*txo_step], n_TXO))
	t_STXO = threading.Thread(target=batch_add, args=(A0_STXO, STXO, x_list_STXO[0:(i+1)*stxo_step], n_STXO))
	
	t_TXO.start()
	t_STXO.start()

	t_TXO.join()
	t_STXO.join()

	A1_TXO, nipoe_TXO = que.get()
	A1_STXO, nipoe_STXO = que.get()
	
	#W = create_all_membership_witnesses(A0, S, n)
	tok = time.time()
	print("Lenth:", (i+1)*200, "\t\tTime Taken: ", tok-tik)
	time_to_batchAdd.append(tok-tik)
	y.append((i+1)*200)

print(time_to_batchAdd)
plt.plot(y,time_to_batchAdd, label='batchAdd')
plt.grid()
plt.show()
