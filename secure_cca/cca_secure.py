import sys
import random

seed_size = 16
generator = 223
modulus = 36389

def l(k):
    # return k**2 - 2*k + 1
    return 2*k

def xor(a,b):
    # if(len(a)!=len(b)):
    #     print("Error while performing XOR (Lengths not equal)")
    #     print("A len:",len(a))
    #     print("B len:",len(b))
    #     return
    result = ''
    for i in range(min(len(a),len(b))):
        result += str(int(a[i])^int(b[i]))
    return result


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
    r = "1111111111111111"
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

    

def CBC_MAC(key,msg):

    msg = padding(msg,seed_size)

    n = len(msg)
    n_bit_string = bin(n).replace("0b",'')
    n_bit_string = n_bit_string.zfill(seed_size)
    # print("n_bit_string:",n_bit_string)
    tag = PRF(key,n_bit_string)
    while(len(msg)>0):
        end_length = min(seed_size,len(msg))
        # print("tag:",tag)
        # end_length = seed_size
        temp = msg[:end_length]
        msg = msg [end_length:]
        r = xor(tag,temp)
        tag = PRF(key,r)
    return tag

def CCA_gen(n):
    key1 = rand_bit_string(n)
    key2 = rand_bit_string(n)
    print("key1:",key1)
    print("key2:",key2)
    return key1,key2


def verify(key,m,t):
    temp = CBC_MAC(key,m)
    if(temp==t):
        return 1
    return 0


def CCA_encrypt(key1,key2,msg):
    # msg = padding(msg,seed_size)
    c = encrypt(key1,msg)
    t = CBC_MAC(key2,c)
    return c,t
    # cipher = c+t
    # return cipher

def CCA_decrypt(key1,key2,c,t):
    if(verify(key2,c,t)==0):
        print("Message Authentication Failed")
        return
    return decrypt(c,key1)


seed = input("Enter message:")
key1,key2=CCA_gen(seed_size)
# tag = CBC_MAC(key2,seed)
c,t = CCA_encrypt(key1,key2,seed)
print("Encrypted cipher:",c)
print("CBC MAc tag for msg:",t)

result = CCA_decrypt(key1,key2,c,t)
print("Message After Decryption:",result)