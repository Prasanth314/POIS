import sys

seed_size = 16
generator = 223
modulus = 36389

def l(k):
    # return k**2 - 2*k + 1
    return 2*k
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


print("Enter message of size 16")
msg=input()
print("PRG:",function_G(msg))