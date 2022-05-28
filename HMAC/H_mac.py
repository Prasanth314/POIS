import sys
import random

n=16
q=35381
g=7
h=3
opad = 0x36
ipad = 0x5c


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

def fixed_length_hash(x1,x2):
    # x1 and x2 are of length n
    g_pow_x1 = pow(g, int(x1,2),q)
    h_pow_x2 = pow(h, int(x2,2),q)
    result = (g_pow_x1 * h_pow_x2) % q
    result = bin(result).replace('0b','').zfill(n)
    return result

def rand_bit_string(n):
    result=''
    for i in range(n):
        result += str(random.randint(0,1))
    return result





def MD_transform(x,r):
    # r is of length n
    # Divide x into blocks of size n
    
    x_length_bin = bin(len(x)).replace('0b','').zfill(n)
    x=padding(x,n)
    while(len(x)>0):
        temp = x[:n]
        x = x[n:]
        r = fixed_length_hash(temp,r)
    result = fixed_length_hash(x_length_bin,r)
    return result


def H_MAC(key,r,m):
    ipad_bin_string = bin(ipad).replace('0b','').zfill(8)
    ipad_bin_string = ipad_bin_string*(n//8)
    opad_bin_string = bin(opad).replace('0b','').zfill(8)
    opad_bin_string = opad_bin_string*(n//8)

    k = xor(key,ipad_bin_string)
    r2 = fixed_length_hash(k,r)
    r2 = MD_transform(m,r2)
    k = xor(key,opad_bin_string)
    r3 = fixed_length_hash(k,r)
    H_MAC_tag = fixed_length_hash(r2,r3)
    return H_MAC_tag

message = input("Enter message:")

key = rand_bit_string(n)
r = rand_bit_string(n)
print("H MAC:",H_MAC(key,r,message))