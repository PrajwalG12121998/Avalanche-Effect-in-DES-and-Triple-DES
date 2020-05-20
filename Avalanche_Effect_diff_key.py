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

#Initialize a randomArray to get 10000 Key
randKeyArray = []

#Calculate Hamming distance
def HammingDistance(bits0,bits1):
    #print('bits0: {:016x}'.format(bits0))
    #print('bits1: {:016x}'.format(bits1))
    return bin(bits0 ^ bits1).count("1")

def randomBitFlip(bits0):
    #print('bits0: {:016x}'.format(bits0))
    bitnum = random.randint(0,63)
    bits1 = bits0 ^ (1 << bitnum)
    randKeyArray.append(bits1)

randKeyArray.append(sysrandom.getrandbits(64))



#Create 10000 key which differ only by one bit
for i in range(0,10000):
    randomBitFlip(randKeyArray[i])

hamming_d = []

plaintext = '12345678'

for i in range(0,10000):
    
    des1 = DES.new(randKeyArray[i].to_bytes(8,'little'), DES.MODE_ECB)
    des2 = DES.new(randKeyArray[i+1].to_bytes(8,'little'), DES.MODE_ECB)
   
    ciphertext1 = des1.encrypt(plaintext)
    ciphertext2 = des2.encrypt(plaintext)
    #print(ciphertext1);
    #print(ciphertext2);
    #type(ciphertext1)
    d = HammingDistance(int.from_bytes(ciphertext1,'little'),int.from_bytes(ciphertext2,'little'))    
    hamming_d.append(d)


print(max(hamming_d))
print(min(hamming_d))
print("Mean: ",statistics.mean(hamming_d))
print("Standard Deviation: ",statistics.stdev(hamming_d))

#Plot an histogram to show the frequrncy of the bits change

np_hamming_d = np.array(hamming_d)

uniqueVal_des, occurCount_des = np.unique(np_hamming_d, return_counts=True)


x = uniqueVal_des
y = occurCount_des
colors = itertools.cycle(['b','r'])
plt.ylabel('Frequency')
plt.xlabel('No of Bits Flipped in DES')
for i in range(len(y)):
    plt.bar(x[i], y[i], color=next(colors))
plt.show()


###########################################################################################


#3DES Avalanche Effect

def randomBitFlip_3DES(bits0):
    #print('bits0: {:016x}'.format(bits0))
    bitnum = sysrandom.randint(0,127)
    bits1 = bits0 ^ (1 << bitnum)
    randKeyArray_3DES.append(bits1)

randKeyArray_3DES = []

randKeyArray_3DES.append(sysrandom.getrandbits(128))


for i in range(0,10000):
    randomBitFlip_3DES(randKeyArray_3DES[i])


hamming_d_t = []

for i in range(0,10000):
    tdes1 = DES3.new(randKeyArray_3DES[i].to_bytes(16,'little'),DES.MODE_ECB)
    tdes2 = DES3.new(randKeyArray_3DES[i+1].to_bytes(16,'little'),DES.MODE_ECB)
    
    tciphertext1 = tdes1.encrypt(plaintext)
    tciphertext2 = tdes2.encrypt(plaintext)
    
    d = HammingDistance(int.from_bytes(tciphertext1,'little'),int.from_bytes(tciphertext2,'little'))    
    hamming_d_t.append(d)    
    
    
print(max(hamming_d_t))
print(min(hamming_d_t))
print("Mean 3DES: ",statistics.mean(hamming_d_t))
print("Standard Deviation 3DES: ",statistics.stdev(hamming_d_t))

np_hamming_d_t = np.array(hamming_d_t)

uniqueVal_3des, occurCount_3des = np.unique(np_hamming_d_t, return_counts=True)


x = uniqueVal_3des
y = occurCount_3des
colors = itertools.cycle(['b','r'])
plt.ylabel('Frequency')
plt.xlabel('No of Bits Flipped in DES3')
for i in range(len(y)):
    plt.bar(x[i], y[i], color=next(colors))
plt.show()


#Comparison in Avalanche effect between 3DES and des
#Plotting both graph simultaneously
des_and_3des = np.column_stack((np_hamming_d,np_hamming_d_t))

colors = ['red', 'blue']
labels = ['DES','3DES']

Lbins = [31,33]
plt.hist(des_and_3des, Lbins,
         histtype='bar',
         stacked=False,
         label = labels,
         fill=True,
         alpha=0.8, # opacity of the bars
         edgecolor = "k")
plt.xlabel('Bits Flipped With 1 bit change in key')
plt.ylabel('Frequency')   
plt.legend()
plt.show()




