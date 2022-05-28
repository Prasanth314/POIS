import sys
import random

seed_size = 16
generator = 223
modulus = 36389

def l(k):
    # return k**2 - 2*k + 1
    return 2*k




def padding(msg,nl):
    if((len(msg))%nl!=0):
        new_length = (int(len(msg)/nl) + 1)*nl
        msg = msg.ljust(new_length,'0')
    return msg

def rand_bit_string(n):
    result=''
    for i in range(n):
        result += str(random.randint(0,1))
    return result

def function_H(x,y):
    mod_exp = bin(pow(generator, int(x,2),modulus)).replace('0b','')
    mod_exp = mod_exp.zfill(seed_size)

    hardCoreBit = 0
    for i in range(len(x)):
        hardCoreBit = (hardCoreBit ^ (int(x[i]) & int(y[i])))%2
    
    return mod_exp+y+str(hardCoreBit)

def function_G(seed):
    msg=seed
    result=''
    seedsize=len(seed)
    for i in range(l(seedsize)):
        x = msg[:len(msg)//2]
        y = msg[len(msg)//2:]
        msg = function_H(x,y)
        result += msg[-1]
        msg = msg[:-1]
    return result

def PRF(k,x):
    key_length=len(k)
    # print(key_length_half)
    # x=x[::-1]
    for i in x:
        k=function_G(k)
        if i==0:
            k=k[:key_length]
        else:
            k=k[key_length:]
        # print("K value:",k)
    return k



def encrypt(key,msg):
    # key = n bit string
    # r = n bit string

    # key = "1111111111111111"
    # r = "1111111111111111"
    r = rand_bit_string(seed_size)
    cipher = r
    
    # msg = padding(msg,seed_size)
    print("CPA encrypt msg length:",len(msg))
    while(len(msg)>0):
        r = PRF(key,r)
        end_length = min(seed_size,len(msg))
        temp = msg[:end_length]
        msg = msg [end_length:]
        result = ''
        for i in range(len(temp)):
            result += str(int(r[i])^int(temp[i]))
        cipher += result
    return cipher

def decrypt(cipher,key):
    cipher_length_half = len(cipher)//2
    r = cipher[:seed_size]
    cipher = cipher[seed_size:]
    msg = ''
    while(len(cipher)>0):
        r = PRF(key,r)
        end_length = min(seed_size,len(cipher))
        temp = cipher[:end_length]
        cipher = cipher[end_length:]
        result = ''
        for i in range(len(temp)):
            result += str(int(r[i])^int(temp[i]))
        msg += result
    return msg


msg = input("Enter a message:")
key = rand_bit_string(seed_size)
cipher = encrypt(key,msg)
print("Encrypted message:",cipher)
print("Message after Decryption:",decrypt(cipher,key))