# -*- coding: utf-8 -*-

import random
import numpy as np
import matplotlib.pyplot as plt
import statistics
import itertools
import time
from Crypto.Cipher import DES
from Crypto.Cipher import DES3

sysrandom = random.SystemRandom()

#Initialize a randomArray to get 10000 plaintext
randArray = []

def randomBitFlip(bits0):
    #print('bits0: {:016x}'.format(bits0))    
    bitnum = random.randint(0,63)
    bits1 = bits0 ^ (1 << bitnum)
    #print('bits0: {:016x}'.format(bits0))
    randArray.append(bits1)

randArray.append(sysrandom.getrandbits(64))

#Create 10000 plaintext which differ only by one bit
for i in range(0,10000):
    randomBitFlip(randArray[i])

encryption_t_des = []
decryption_t_des = []

key = '01234567'
des = DES.new(key, DES.MODE_ECB)

for j in range(0,100):
    start = time.perf_counter_ns()
    for i in range(0,10000):    
        ciphertext = des.encrypt(randArray[i].to_bytes(8,'little'))
    
    end = time.perf_counter_ns()
    encryption_t_des.append(end-start)
print("Mean encryption time DES: ",statistics.mean(encryption_t_des))
#1134.44
#10.17ms

#Decryption time
for j in range(0,100):
    start = time.perf_counter_ns()

    for i in range(0,10000):
        plaintext = des.decrypt(ciphertext_des[i].to_bytes(8,'little'))
    
    end = time.perf_counter_ns()
    decryption_t_des.append(end-start)
    
print("Mean decryption time DES: ",statistics.mean(decryption_t_des))
#1112.21
#10.25ms
###################################################################################################

encryption_t_des3 = []
decryption_t_des3 = []

tkey = '0123456789012345' #key size 16bytes
tdes = DES3.new(tkey,DES.MODE_ECB)

for j in range(0,100):
    start = time.perf_counter_ns()
    for i in range(0,10000):    
        tciphertext = tdes.encrypt(randArray[i].to_bytes(8,'little'))    
         
    end = time.perf_counter_ns()
    encryption_t_des3.append(end-start)
    
print("Mean 3DES: ",statistics.mean(encryption_t_des3))
#1947.27
#18.95ms

#decryption in 3des
for j in range(0,100):
    start = time.perf_counter_ns()
    for i in range(0,10000):
        plaintext = tdes.decrypt(ciphertext_des3[i].to_bytes(8,'little'))
        
    end = time.perf_counter_ns()
    decryption_t_des3.append(end - start)    
print("Mean: ",statistics.mean(decryption_t_des3))
#1417.05
#13.24ms

##################################################################################################
x = ['ENCRYPT-DES','ENCRYPT-DES3','DECRYPT-DES','DECRYPT-DES3']
y = [10.17,18.95,10.25,13.24]
colors = itertools.cycle(['b', 'g', 'b','g'])
plt.ylabel('Time in ms(milli seconds)')
plt.xlabel('Encryption or Decryption')
for i in range(len(y)):
    plt.bar(x[i], y[i], color=next(colors))
plt.show()
