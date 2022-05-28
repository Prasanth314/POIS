import sys
import random

n=16
q=35381
g=7
h=3
opad = 0x36
ipad = 0x5c

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

message = rand_bit_string(2*n)
x1 = message[:len(message)//2]
x2 = message[len(message)//2:]
print("Message:",message)
print("Fixed Length Hash:",fixed_length_hash(x1,x2))

