import numpy
from heapq import *
import random
from helpfunctions import *
from main import *

global t_min
t_min = dict()
t_min[1] = 86400.0
class Event:
	def __init__(self, dest, orig, action, payload):
		self.dest = dest
		self.orig = orig
		self.action = action
		self.payload = payload

	def __lt__(self, other):
		return 0


class Block:
	def __init__(self, prev, height, time, miner_id, size, valid,num_tx):
		self.prev = prev
		self.height = height
		self.time = time
		self.miner_id = miner_id
		self.size = size
		self.valid = valid
		#self.Acc = A0
		self.num_tx = num_tx
		

class Link:
	def __init__(self, dest, latency, bandwidth):
		self.dest = dest
		self.latency = latency
		self.bandwidth = bandwidth
		self.fulluntil = 0.0
	
	def occupy(self, t, t_size):
		base_t = t
		if self.fulluntil > base_t: base_t = self.fulluntil
		base_t += self.latency
		base_t += t_size/self.bandwidth
		self.fulluntil = base_t
		return base_t

class Miner:
	def __init__(self, miner_id, hashrate, verifyrate, blocksize, seed_block, event_q,A0,n,S,A,proofs,t):
		self.miner_id = miner_id
		self.hashrate = hashrate
		self.verifyrate = verifyrate
		self.verifyfulluntil = 0.0
		
		self.blocksize = blocksize
		self.h_p = 0
		self.k = 5
		self.k_c = 3
		self.num_reaffirmatins = 0
		self.pulse_block_length = 10
		self.pulse_block_hash = None
		self.blocks = dict()
		self.chain_head = '*'
		self.longest_chain = dict()
		self.size_secure_chain = dict()
		self.chain_size = dict()
		self.size_coin_prune = dict()
		self.coin_prune = dict()
		
		self.blocks_new = []
		self.requested = dict()
		self.t_min = dict()
		self.t_next = dict()
		
		self.t = t
		self.event_q = event_q
		self.A0 = A0
		self.n = n
		self.S = dict()
		self.A = dict()
		self.proofs = dict()
		#self.S_d = dict()
		#self.S_a = dict()
		self.S = S
		self.A = A
		self.proofs = proofs
		# if self.miner_id == 0:
			# print(self.S)
			# print(self.A)
			# print(proofs)
		self.links = []
		self.add_block(seed_block)
		

	def mine_block(self):
		t_next = self.t + numpy.random.exponential(1/self.hashrate, 1)[0]
		#print('Next block creation time of miner %d : %.3f' %(self.miner_id,t_next))
		t_size = self.blocksize #1024*200*numpy.random.random()
		n_tx = random.randint(int(len(self.S)/4),int(len(self.S)/3))
		n_inputs = random.randint(1,2)
		n_outputs = random.randint(1,3)
		
		if self.miner_id == 0:
			if self.blocks[self.chain_head].height % self.pulse_block_length == 0:
				self.h_p = self.blocks[self.chain_head].height
				self.longest_chain_selection()
				self.pulse_block_hash = self.chain_head
				self.num_reaffirmations = 0
				
			if self.blocks[self.chain_head].height - self.h_p == self.k :
				self.size_secure_chain[self.blocks[self.chain_head].height] = 0.0
				self.longest_chain_selection()
				for x in sorted(list(self.longest_chain.keys())):
					if x < self.h_p:
						del self.longest_chain[x]
				#self.size_secure_chain[self.blocks[self.chain_head].height] = len(self.longest_chain.keys())
				self.pulse_block_hash = self.chain_head
				if self.num_reaffirmations >= self.k_c:
					for x in sorted(list(self.coin_prune.keys())):
						if x < self.h_p:
							del self.coin_prune[x]
				
			self.longest_chain_selection()	
			#self.size_secure_chain[self.blocks[self.chain_head].height] = len(self.longest_chain.keys())
			self.size_secure_chain[self.blocks[self.chain_head].height] = self.calculate_size()
			self.size_coin_prune[self.blocks[self.chain_head].height] = self.calculate_coinPrune_size()
			if self.blocks[self.chain_head].miner_id in [2,3,5,9,11]:
				self.num_reaffirmations += 1
					
				
		# if self.blocks[self.chain_head].height+1 not in t_min:
			# t_min[self.blocks[self.chain_head].height+1] = t_next
			# self.state_transition(n_tx,n_inputs,n_outputs,self.A[len(self.A)-1])
			# print(self.miner_id, t_min,self.blocks[self.chain_head].height)
			# t_block = Block(self.chain_head, self.blocks[self.chain_head].height + 1, t_next, self.miner_id, t_size, 1,self.A[len(self.A)-1],n_tx)
			# #t_block = Block(self.chain_head, self.blocks[self.chain_head].height + 1, t_next, self.miner_id, t_size, 1,n_tx)
			# self.send_event(t_next, self.miner_id, 'block', t_block)

		# if t_next < t_min[self.blocks[self.chain_head].height+1]:
			# t_min[self.blocks[self.chain_head].height + 1] = t_next
			# self.state_transition(n_tx,n_inputs,n_outputs,self.A[len(self.A)-1])
			# print(self.miner_id, t_min,self.blocks[self.chain_head].height)
			# t_block = Block(self.chain_head, self.blocks[self.chain_head].height + 1, t_next, self.miner_id, t_size, 1,self.A[len(self.A)-1],n_tx)
		t_block = Block(self.chain_head, self.blocks[self.chain_head].height + 1, t_next, self.miner_id, t_size, 1,n_tx)
		self.send_event(t_next, self.miner_id, 'block', t_block)

	def verify_block(self, t_block):
		if (t_block.miner_id == self.miner_id) and (t_block.prev != self.chain_head):
			#print('%02d: block %s is to be ignored (old mining block event from before chain_head changed).' % (self.miner_id, hash(t_block)))
			return -1
		if t_block.valid != 1: 
			print('%02d: block %s is invalid.' % (self.miner_id, hash(t_block)))
			return -1
		if t_block.prev not in self.blocks: 
			#print('%02d: need previous block to verify block %s.' % (self.miner_id, hash(t_block)))
			return 0
		if t_block.height != self.blocks[t_block.prev].height + 1:
			print('%02d: height of block %s is invalid (%d / %d).' % (self.miner_id, hash(t_block), t_block.height, self.blocks[t_block.prev].height))
			return -1
		return 1

	def add_block(self, t_block):
		self.blocks[hash(t_block)] = t_block
		if (self.chain_head == '*'):
			self.chain_head = hash(t_block)
			if self.miner_id < 13 :
				self.mine_block()
			return
		if (t_block.height > self.blocks[self.chain_head].height):
			self.chain_head = hash(t_block)
			self.announce_block(self.chain_head)
			if self.miner_id < 13 :
				self.mine_block()

	def occupy(self, t, t_size):
		base_t = t
		if self.verifyfulluntil > base_t: base_t = self.verifyfulluntil
		base_t += t_size/self.verifyrate
		self.verifyfulluntil = base_t
		return base_t

	def process_new_blocks(self):
		rerun = 1
		while rerun == 1:
			rerun = 0
			blocks_later = []
			for t_block in self.blocks_new:
				validity = self.verify_block(t_block)
				if validity == 1: 
					#self.add_block(t_block)
					t = self.occupy(self.t, t_block.size)
					self.send_event(t, self.miner_id, 'addblock', t_block)
					#rerun = 1
				if validity == 0:
					blocks_later.append(t_block)
					self.request_block(-1, t_block.prev)
			self.blocks_new = blocks_later


	def receive_event(self, t, t_event):
		self.t = t
		if t_event.action == 'addblock':
			if t_event.orig != self.miner_id: print('received addblock not from myself!')
			self.add_block(t_event.payload)
			self.process_new_blocks()
		if t_event.action == 'block':
			self.blocks_new.append(t_event.payload)
			self.process_new_blocks()
		if t_event.action == 'newhead':
			if t_event.payload not in self.blocks:
				self.request_block(t_event.orig, t_event.payload)
		if t_event.action == 'getblock':
			if t_event.payload in self.blocks:
				self.send_block(t_event.orig, t_event.payload)

	def send_event(self, t, to, action, payload):
		t_event = Event(to, self.miner_id, action, payload)
		heappush(self.event_q, (t, t_event))
		# if t_event.dest == 0 or t_event.orig == 0:
			# if action ==  'addblock':
				# print('%0.4f %d %d %s %s %d %0.4f' %(t,t_event.orig,t_event.dest,t_event.action,t_event.payload.height,t_event.payload.miner_id, t_event.payload.time))
			# print('%0.4f %d %d %s %s' %(t,t_event.orig,t_event.dest,t_event.action,t_event.payload))
		#if t_event.action == 'addblock':
		#	print('%0.4f %d %d %s %s %d %0.4f' %(t,t_event.orig,t_event.dest,t_event.action,t_event.payload.height,t_event.payload.miner_id, t_event.payload.time))
			

	def add_link(self, dest, latency, bandwidth):
		t_link = Link(dest, latency, bandwidth)
		self.links.append(t_link)

	def announce_block(self, t_hash):
		for t_link in self.links:
			t_arrival = t_link.occupy(self.t, 0)
			self.send_event(t_arrival, t_link.dest, 'newhead', t_hash)

	def request_block(self, to, t_hash):
		if t_hash in self.requested: return
		self.requested[t_hash] = 1
		for t_link in self.links:
			if (t_link.dest == to) or (to == -1):
				t_arrival = t_link.occupy(self.t, 0)
				self.send_event(t_arrival, t_link.dest, 'getblock', t_hash)

	def send_block(self, to, t_hash):
		for t_link in self.links:
			if t_link.dest == to:
				t_block = self.blocks[t_hash]
				k = random.randint(1,len(self.links))
				t_arrival = t_link.occupy(self.t, t_block.size)
				self.send_event(t_arrival, t_link.dest, 'block', t_block)

	def state_transition(self,n_tx_per_block,n_inputs,n_outputs,A_pre_delete):
		S_d = dict()
		S_a = dict()
		for utxo in self.S.keys():
			S_d[utxo] = self.S[utxo]
			if len(S_d) == n_tx_per_block*n_inputs:
				break
				
		proofs_list = []
		for x in S_d.keys():
			proofs_list.append(self.proofs[x])
			
		A_post, product, nipoe = batch_delete_using_membership_proofs(A_pre_delete, self.S, S_d, proofs_list, self.n)
		
		y = create_list(n_tx_per_block*n_outputs)
		A_final,nipoe_add = batch_add(A_post, self.S, y, self.n)
		self.A[len(self.A)] = A_final
		W = create_all_membership_witnesses(self.A0,self.S, self.n)
		j = 0
		for x in self.S.keys():
			self.proofs[x] = W[j]
			j += 1
			
	def longest_chain_selection(self):
		t_hash = self.chain_head
		#print(self.blocks[self.pulse_block_hash].height)
		while t_hash != self.pulse_block_hash:
			t_block = self.blocks[t_hash]
			if (t_hash not in self.longest_chain):
				self.longest_chain[t_block.height] = t_block
				self.chain_size[t_block.height] = t_block.size
				self.coin_prune[t_block.height] = t_block
			t_hash = t_block.prev
			
		#print(len(self.longest_chain.keys()))
		#print(self.h_p)	
		#print(sorted(list(self.longest_chain.keys())))
		
		
	def calculate_size(self):
		s = 0
		for x in range(min(list(self.longest_chain.keys())),max(list(self.longest_chain.keys()))):
			s += self.chain_size[x]
			
		return s
		
	def calculate_coinPrune_size(self):
		s = 0
		for x in range(min(list(self.coin_prune.keys())),max(list(self.coin_prune.keys()))):
			s += self.chain_size[x]
			
		return s
			
			
				
				 
			
			
		
			
		
		
