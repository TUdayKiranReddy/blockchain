import secrets
import time
import threading
import queue
import os
import matplotlib.pyplot as plt
from helpfunctions import *
from main import *

# Boneh's stateless blockchain
m = np.array(np.arange(20))
m = (m+1)*100
#print(m)
time_boneh = []	
mem_boneh = []
for i in m:
	n, A0, S = setup()
	#print(m[i])
	x = create_list(i)
	A,nipoe = batch_add(A0,S,x,n)
	W = create_all_membership_witnesses(A0, S, n)
	
	S_D = dict()
	for utxo in S.keys():
		if len(S_D) != i:
			S_D[utxo] = S[utxo]
			
	
	y = create_list(2*i)
	tik = time.time()
	A_post, product, nipoe = batch_delete_using_membership_proofs(A, S, S_D, W, n)
	A_final, nipoe = batch_add(A_post, S, y, n)
	tok = time.time()
	time_boneh.append(tok-tik)
	print("m:", i, "\t\tTime Taken: ", tok-tik)
print(time_boneh)
with open("time_boneh.txt", "w") as f:
	for t in time_boneh:
		f.write(str(t)+" ")
f.close()

#Minichain
time_minichain = []
for i in m:
	n, A0, S = setup()
	x = create_list(i)
	MMR = merkletools.MerkleTools()
	peaks = create_list(20)
	tik = time.time()
	STXO_C, nipoe = batch_add(A0,S,x,n)
	for j in range(len(peaks)):
		MMR.add_leaf(str(peaks[j]), True)
	MMR.make_tree()
	TXO_C = MMR.get_merkle_root()
	tok = time.time()
	time_minichain.append(tok-tik)
	print("m:", i, "\t\tTime Taken: ", tok-tik)
print(time_minichain)
with open("time_minichain.txt", "w") as f:
	for t in time_minichain:
		f.write(str(t)+" ")
f.close()

#Proposed
time_proposed = []
for i in m:
	n, A0, S = setup()
	x = create_list(i)
	y = create_list(2*i)
	
	tik = time.time()
	STXO_C, nipoe = batch_add(A0,S,x,n)
	TXO_C, nipoe = batch_add(A0,S,y,n)
	tok = time.time()
	time_proposed.append(tok-tik)
	v_STXO  create_all_membership_witnesses(STXO_C, S, n)
	v_TXO  create_all_membership_witnesses(TXO_C, S, n)
	print("m:", i, "\t\tTime Taken: ", tok-tik)
	print(batch_prove_membership_with_NIPoE())
	
print(time_proposed)
with open("time_proposed.txt", "w") as f:
	for t in time_proposed:
		f.write(str(t)+" ")
f.close()

plt.figure()
plt.title("Time Taken By Boneh's Algorithm")
plt.plot(3*m, time_boneh, '-*')
plt.grid()
plt.savefig('time_boneh.png')

plt.figure()
plt.title("Time Taken By MiniChain Algorithm")
plt.plot(3*m, time_minichain, '-*')
plt.grid()
plt.savefig("time_minichain.png")


plt.figure()
plt.title("Time Taken By Our Proposed Algorithm")
plt.plot(3*m, time_proposed, '-*')
plt.grid()
plt.savefig("time_proposed.png")

plt.figure()
plt.plot(3*m, time_proposed, '-*', label='Proposed')
plt.plot(3*m, time_minichain, '-*', label='MiniChain')
plt.grid()
plt.legend()
plt.savefig("provsmini.png")


# plt.figure()
# plt.plot(3*m, time_boneh, '-*', label='Boneh')
# plt.plot(3*m, time_minichain, '-*', label='MiniChain')
# plt.plot(time_proposed, '-*', label='Proposed')
# plt.grid()
# plt.legend()
# plt.savefig("all.png")


plt.show()



	



	


