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


###############################################################
def pointAddition(x1, y1, x2, y2, a, b, mod):
	
	if x1 == x2 and y1 == y2:
		#doubling
		beta = (3*x1*x1 + a) * (findModularInverse(2*y1, mod))
        

	
	else:
		#point addition
		beta = (y2 - y1)*(findModularInverse((x2 - x1), mod))

	x3 = beta*beta - x1 - x2
	y3 = beta*(x1 - x3) - y1
	
	x3 = x3 % mod
	y3 = y3 % mod
	
	while(x3 < 0):
		x3 = x3 + mod
	
	while(y3 < 0):
		y3 = y3 + mod
	
	return x3, y3
##########################################################




def applyDoubleAndAddMethod(x0, y0, k, a, b, mod):
	
	x_temp = x0
	y_temp = y0
	
	kAsBinary = bin(k) #0b1111111001
	kAsBinary = kAsBinary[2:len(kAsBinary)] #1111111001
	#print(kAsBinary)
	
	for i in range(1, len(kAsBinary)):
		currentBit = kAsBinary[i: i+1]
		#always apply doubling
		x_temp, y_temp = pointAddition(x_temp, y_temp, x_temp, y_temp, a, b, mod)
		
		if currentBit == '1':
			#add base point
			x_temp, y_temp = pointAddition(x_temp, y_temp, x0, y0, a, b, mod)
	
	return x_temp, y_temp



def compute_R(KE,XA,YA,a,b,mod):
    xr , yr =applyDoubleAndAddMethod(XA, YA, KE, a, b, mod)
    return xr,yr
    




def compute_S(hx,d,xr,KE,q):
    s=((hx+d*xr)*findModularInverse(KE, q))%q
    return s
def compute_u1_u2(w,hx,q,r):
    u1=(w*hx)%q
    u2=(w*r)%q
    return u1,u2
def compute_p(u1,u2,XA,YA,XB,YB,a,b,q):
    xtemp,ytemp=applyDoubleAndAddMethod(XA, YA, u1, a, b, q)
    xtemp1,ytemp1=applyDoubleAndAddMethod(XB, YB, u2, a, b, q)
    XP,YP=pointAddition(xtemp, ytemp, xtemp1, ytemp1, a, b, q)
    return XP,YP



"E : y2 ≡ x3+2x+2 mod 17"
print("E : y2 ≡ x3+2x+2 mod 17")

p,a,b,q=17,2,2,19
XA,YA=5,1
print("A is point genrator = ",'(',XA,',',YA,')')
d=7
message=input("Enter your message: ")

hx=calculate_hash(message)%q
print("your hash of message is = ",hx)

print("Enter KE in range 0 to ",q,"not out range ")
KE=int(input())
if(0<KE<q):
    print ("KE is in range and can be used ")
else:
    print("KE is no valid ")
    exit()
    


XB,YB=applyDoubleAndAddMethod(XA, YA, d, a, b, p)
print("your point B is =d*A=",applyDoubleAndAddMethod(XA, YA, d, a, b, p) )
################
"Signture "
xr,yr=compute_R(KE, XA, YA, a, b, p)
print("R=KE*A  =",compute_R(KE, XA, YA, a, b, p))
r=xr
print ("r = x of R =",r)
s=compute_S(hx, d, xr, KE, q)
print("s ≡ (h(x)+d · r)kE−1 mod q. =",s)


####################
"verification"
w=findModularInverse(s, q)
print("w ≡ s−1 mod q.=",w)
u1,u2=compute_u1_u2(w, hx, q, r)
print("u1 ≡ w· h(x) mod q.=",u1)
print('u2 ≡ w· r mod q.=',u2)
xp,yp = compute_p(u1, u2, XA, YA, XB, YB, a, b, p)
print("P = u1 A+u2 B.=",compute_p(u1, u2, XA, YA, XB, YB, a, b, p))
if(xp==r):
    print("Valid signtrue because :"
          "xp = ",xp ,"r =",r,
          "and they are the same value"
          
          )
    
else:
    print("Invalid signture")










    
    
    
       
    
    
    


























