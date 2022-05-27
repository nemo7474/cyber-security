import sys
import random
import math

class SHA1:
    def __init__(self):
        self.__H = [
            0x67452301,
            0xEFCDAB89,
            0x98BADCFE,
            0x10325476,
            0xC3D2E1F0
            ]

    def __str__(self):
        return ''.join((hex(h)[2:]).rjust(8, '0') for h in self.__H)

    # Private static methods used for internal operations.
    @staticmethod
    def __ROTL(n, x, w=32):
        return ((x << n) | (x >> w - n))

    @staticmethod
    def __padding(stream):
        l = len(stream)  # Bytes
        hl = [int((hex(l*8)[2:]).rjust(16, '0')[i:i+2], 16)
              for i in range(0, 16, 2)]

        l0 = (56 - l) % 64
        if not l0:
            l0 = 64

        if isinstance(stream, str):
            stream += chr(0b10000000)
            stream += chr(0)*(l0-1)
            for a in hl:
                stream += chr(a)
        elif isinstance(stream, bytes):
            stream += bytes([0b10000000])
            stream += bytes(l0-1)
            stream += bytes(hl)

        return stream

    @staticmethod
    def __prepare(stream):
        M = []
        n_blocks = len(stream) // 64

        stream = bytearray(stream)

        for i in range(n_blocks):  # 64 Bytes per Block
            m = []

            for j in range(16):  # 16 Words per Block
                n = 0
                for k in range(4):  # 4 Bytes per Word
                    n <<= 8
                    n += stream[i*64 + j*4 + k]

                m.append(n)

            M.append(m[:])

        return M

    @staticmethod
    def __debug_print(t, a, b, c, d, e):
        print('t = {0} : \t'.format(t),
              (hex(a)[2:]).rjust(8, '0'),
              (hex(b)[2:]).rjust(8, '0'),
              (hex(c)[2:]).rjust(8, '0'),
              (hex(d)[2:]).rjust(8, '0'),
              (hex(e)[2:]).rjust(8, '0')
              )

    # Private instance methods used for internal operations.
    def __process_block(self, block):
        MASK = 2**32-1

        W = block[:]
        for t in range(16, 80):
            W.append(SHA1.__ROTL(1, (W[t-3] ^ W[t-8] ^ W[t-14] ^ W[t-16]))
                     & MASK)

        a, b, c, d, e = self.__H[:]

        for t in range(80):
            if t <= 19:
                K = 0x5a827999
                f = (b & c) ^ (~b & d)
            elif t <= 39:
                K = 0x6ed9eba1
                f = b ^ c ^ d
            elif t <= 59:
                K = 0x8f1bbcdc
                f = (b & c) ^ (b & d) ^ (c & d)
            else:
                K = 0xca62c1d6
                f = b ^ c ^ d

            T = ((SHA1.__ROTL(5, a) + f + e + K + W[t]) & MASK)
            e = d
            d = c
            c = SHA1.__ROTL(30, b) & MASK
            b = a
            a = T

            #SHA1.debug_print(t, a,b,c,d,e)

        self.__H[0] = (a + self.__H[0]) & MASK
        self.__H[1] = (b + self.__H[1]) & MASK
        self.__H[2] = (c + self.__H[2]) & MASK
        self.__H[3] = (d + self.__H[3]) & MASK
        self.__H[4] = (e + self.__H[4]) & MASK

    # Public methods for class use.
    def update(self, stream):
        stream = SHA1.__padding(stream)
        stream = SHA1.__prepare(stream)

        for block in stream:
            self.__process_block(block)

    def digest(self):
        pass

    def hexdigest(self):
        s = ''
        for h in self.__H:
            s += (hex(h)[2:]).rjust(8, '0')
        return s


def findModularInverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return -1

##############################################################
def calculate_hash(x):

    data = str(x).encode("UTF-8")
    h = SHA1()
    h.update(data)
    hex_sha = h.hexdigest()
    print("your input string in utf_8 is : ",'(', data, ')')
    print(hex_sha)
    decimal_sha= int(hex_sha,16)
    print("hash of your string in decimal is :",decimal_sha)
    return decimal_sha

###########################################################
def generate_primes(lower,upper):
    for num in range(lower, upper + 1):
   # all prime numbers are greater than 1
     if num > 1:
       for i in range(2, num):
           if (num % i) == 0:
               break
       else:
           return num

############################################################   
    
def DSA ():
   # message=input("Enter your message ")
    #calculate_hash(message)
    #p=generate_primes(pow(2,1023), pow(2, 1024))
    #q=generate_primes(pow(2,159 ),pow(2, 160))
    p,q,d=59,29,23
    alpha =3
    if(math.gcd(alpha,q)==1):
        print("it is a valid alpha ")
    else:
        print("it is not valid alpha ")
        return 0
    
    bita=pow(alpha, d)%p
    print("Bit is alpha power d % p=",bita)
    print (" will send ",'(',p,',',q,',',alpha,',',bita,')' )
    print ("signature calculation steps ")
    
    hx=17
    print("h(x) after take mod q",hx)
    
    KE=25
    print("key ephemeral KE =",KE)
    
    
    rtemp=pow(alpha,KE)%p
    r=rtemp%q
    print ("r is alpha power kE %p then %q=",r)
    s=((hx+d*r)*findModularInverse(KE, q))%q
    print("s is sha(x) + d*r * inverse of kE % q",s)
    print("signture will be send as ",'(','(',r,s,')',')')
    print("verification ")
    w=findModularInverse(s, q)
    print ("w is inverse of s % q",w)
    u1=(w*hx)%q
    print("u1 is w*h(x) % q", u1)
    u2=(w*r)%q
    print("u2 is w*r % q",u2)
    vtemp=(pow(alpha, u1)*pow(bita, u2))%p
    v=vtemp%q
    print ("v is alpha**u1 * bita**u2 % p then %q",v)
    
    if(v==r):
        print("valid signture with " ,"v=",v ,"r=",r )
        
    else:
        print("invalid signture ")
DSA()