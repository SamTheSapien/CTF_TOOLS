from Crypto.PublicKey import RSA
import gmpy2
import math

def int2Text(number, size):
    text = "".join([chr((number >> j) & 0xff) for j in reversed(range(0, size << 3, 8))])
    return text.lstrip("\x00")

N = 126390312099294739294606157407778835887
C = 13612260682947644362892911986815626931
e = 65537L
#http://factordb.com/index.php?query=58900433780152059829684181006276669633073820320761216330291745734792546625247

p = 9336949138571181619
q = 13536574980062068373
r=(p-1)*(q-1)
d = long(gmpy2.divm(1, e, r))
print (d)
print("\n")
f1 = pow(C,d,N)
print (f1)
print (int2Text(f1,100))
rsa = RSA.construct((N,e,d,p,q))
pt = rsa.decrypt(C)

print (pt)  # returns 6872557977505747778161182217242712228364873860070580111494526546045
print (int2Text(pt,100)) #returns timctf{th0sE_rOoKIe_numB3rz}


