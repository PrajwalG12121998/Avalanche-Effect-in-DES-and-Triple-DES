
#Avalanche Effect
import random
import numpy as np
import matplotlib.pyplot as plt
import statistics
import itertools
from Crypto.Cipher import DES
from Crypto.Cipher import DES3

sysrandom = random.SystemRandom()

#Initialize a randomArray to get 10000 plaintext
randArray = []

#Calculate Hamming distance
def HammingDistance(bits0,bits1):
    #print('bits0: {:016x}'.format(bits0))
    #print('bits1: {:016x}'.format(bits1))
    return bin(bits0 ^ bits1).count("1")

def randomBitFlip(bits0):
    #print('bits0: {:016x}'.format(bits0))
    
    bitnum = random.randint(0,63)
    bits1 = bits0 ^ (1 << bitnum)
    #print('bits0: {:016x}'.format(bits0))
    randArray.append(bits1)
        
    
#Appending first random 64 bit number
randArray.append(sysrandom.getrandbits(64))

#Create 10000 plaintext which differ only by one bit
for i in range(0,10000):
    randomBitFlip(randArray[i])
    
#countTotalBits(randArray[0])    
#countTotalBits(randArray[5])
hamming_d = []

key = '01234567'
des = DES.new(key, DES.MODE_ECB)

for i in range(0,10000):
    
    ciphertext1 = des.encrypt(randArray[i].to_bytes(8,'little'))
    ciphertext2 = des.encrypt(randArray[i+1].to_bytes(8,'little'))
    #print(ciphertext1);
    #print('ciphertext1: {:016x}'.format(ciphertext1))
    #print(ciphertext2);
    #print(type(ciphertext1))
    d = HammingDistance(int.from_bytes(ciphertext1,'little'),int.from_bytes(ciphertext2,'little'))    
    hamming_d.append(d)


print(max(hamming_d))
print(min(hamming_d))
print("Mean: ",statistics.mean(hamming_d))
print("Standard Deviation: ",statistics.stdev(hamming_d))

#ciphertext1 = des.encrypt(randArray[0].to_bytes(8,'little'))
#plaintext1 = des.decrypt(ciphertext1)
#print(HammingDistance(int.from_bytes(plaintext1,'little'),randArray[0]))

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


##############################################################################################


#3DES Avalanche Effect

tkey = '0123456789012345' #key size 16bytes
tdes = DES3.new(tkey,DES.MODE_ECB)

hamming_d_t = []

for i in range(0,10000):
    tciphertext1 = tdes.encrypt(randArray[i].to_bytes(8,'little'))
    tciphertext2 = tdes.encrypt(randArray[i+1].to_bytes(8,'little'))
    
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

Lbins = [28,36]
plt.hist(des_and_3des, Lbins,
         histtype='bar',
         stacked=False,
         label = labels,
         fill=True,
         alpha=0.8, # opacity of the bars
         edgecolor = "k")
plt.xlabel('Bits Flipped With 1 bit change in PT')
plt.ylabel('Frequency')   
plt.legend()
plt.show()

################################################################################################

#3DES Avalanche Effect with 24 bytes key size

#tkey2 = '012345678901234567890123'
#tdes2 =  DES3.new(tkey2,DES.MODE_ECB)
#hamming_d_t2 = []

#for i in range(0,10000):
#    t2ciphertext1 = tdes2.encrypt(randArray[i].to_bytes(32,'little'))
#    t2ciphertext2 = tdes2.encrypt(randArray[i+1].to_bytes(32,'little'))

#    d = HammingDistance(int.from_bytes(t2ciphertext1,'little'),int.from_bytes(t2ciphertext2,'little'))    
#    hamming_d_t2.append(d)    

#max(hamming_d_t2)
#min(hamming_d_t2)
#print(statistics.mean(hamming_d_t2))
#print(statistics.stdev(hamming_d_t2))


##################################################################################################


 