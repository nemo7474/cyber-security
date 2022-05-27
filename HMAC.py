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
   # print("your input string in utf_8 is : ",'(', data, ')')
   # print(hex_sha)
    decimal_sha= int(hex_sha,16)
    #print("hash of your string in decimal is :",decimal_sha)
    binary_sh=bin(decimal_sha)
   # print(binary_sh)
    return binary_sh


ipad=""
for i in range(0, 64):
    ipad=ipad+"00110110"
print ("Your ipad is is = ", len(ipad),"bits " )
print("ipad =",ipad)    
    
opad=""
for i in range(0, 64):
    opad=opad+"01011100"
print("Your opad is = ",len(opad), "bits") 
print("opad =",opad)   
key=input("Enter a 8 bits as key")
keypadded=""
for i in range(0, 64):
    keypadded=keypadded+key
print("your key after padded to be 512 bit is",keypadded)    
 
#####################
"here i take the 512 bit key paddin xor with i padded "

XOR1=int(ipad,2) ^ int(keypadded,2) 
xor1res='{0:b}'.format(XOR1) # xor is 512 bit as result from padded key XOR with ipad


message="abc"
message=message+xor1res #Here i connect the message with result of the xor key padded with ipad
"calculation of sha-1 of first time "
fsha= calculate_hash(message)
fsha=fsha.replace('0','',1)
print("First applying of sha -1 taking the message + xor of (keypadded ,ipad)")
print("result is = ",fsha, " its = ",len(fsha),"bits")
##################################

"here i take the 512 bits of key xor with 512 bit of opad"
XOR2=int(opad,2) ^ int(keypadded,2)
xor2res='{0:b}'.format(XOR2)

conc=fsha+xor2res
print("result of concatination of 160 bits of first sha-1 + (padded key xor opad ")
print(conc)

second_sha =calculate_hash(conc)
#second_sha=second_sha.replace('1','',1)
print("last applying of sha -1 taking conc=fsha+ xor2res ")
print(second_sha)
print("# bits at last sha output = ",len(second_sha),"bits")






