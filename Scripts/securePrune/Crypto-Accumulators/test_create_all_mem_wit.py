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
import csv

def create_list(size):
	res = []
	for x in range(size):
		x = secrets.randbelow(pow(2,256))
		res.append(x)
	return res


n, A0, S = setup()

x = create_list(300)
#print(x)
for i in range(11):
	n, A0, S = setup()
	x = create_list((i+1)*1000)
	tik = time.time()
	A,nipoe = batch_add(A0,S,x,n)
	tok = time.time()
	print("Time elapsed for batchAdd of %d elements: %f" %(1000*(i+1),tok-tik))
	tik = time.time()
	W = create_all_membership_witnesses(A0, S, n)
	tok = time.time()
	print("Time elapsed for all membership creations of %d elements: %f" %(1000*(i+1),tok-tik))
	

