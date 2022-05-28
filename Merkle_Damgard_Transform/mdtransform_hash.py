import sys
import random

n=16
q=35381
g=7
h=3
opad = 0x36
ipad = 0x5c

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

# message = rand_bit_string(2*n)
message = input("Enter message:")
r = rand_bit_string(n)
# print("Message:",message)
print("Merkle Damgard Transform:",MD_transform(message,r))