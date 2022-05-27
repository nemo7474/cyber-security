
def findModularInverse(a, mod):
			
	while(a < 0):
		a = a + mod
	
	#a = a % mod
	
	x1 = 1; x2 = 0; x3 = mod
	y1 = 0; y2 = 1; y3 = a
	q = int(x3 / y3)
	t1 = x1 - q*y1
	t2 = x2 - q*y2
	t3 = x3 - (q*y3)
	while(y3 != 1):
		x1 = y1; x2 = y2; x3 = y3
		y1 = t1; y2 = t2; y3 = t3
		q = int(x3 / y3)
		t1 = x1 - q*y1
		t2 = x2 - q*y2
		t3 = x3 - (q*y3)
		
	
	while(y2 < 0):
		y2 = y2 + mod
	
	return y2
#################################################

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

####################################################
#Main

private_A=7  #private key of Alice
print("private key of Alice=",private_A )

private_B=3  #private key of Bob
print("private key of Alice=",private_B )

modules=229  # p of the elptic curve
print("prime number used in curve =",modules)

px=5
py=1
print("intial point used=" , '(',px ,',' ,py,')')

m=12
print("plaintext is =",m)

xpk,ypk=applyDoubleAndAddMethod(5, 1, private_A, 2, 2, modules)
print("public key of Alice is :", '(',xpk ,',' ,ypk,')') #public of Alice 7.(5,1)

x1pk,y1pk=applyDoubleAndAddMethod(5, 1, private_B, 2, 2, modules)
print("public key of Bob is:", '(',x1pk ,',' ,y1pk,')')

#at Alice 
shx,shy=applyDoubleAndAddMethod(x1pk, y1pk, private_A, 2, 2, 229)
print(shx,shy)

print("shared key at Alice is :", '(',shx ,',' ,shy,')')
shx1,shy1=applyDoubleAndAddMethod(xpk, ypk, private_B, 2, 2, 229)
print("shared key at Bob is :", '(',shx1 ,',' ,shy1,')')

print("Shared keys are same ")

cipher =(m*shx1)%modules
print("The cipher text is = ",cipher)
invers=findModularInverse(shx1, modules)
plain=(cipher*invers)%modules
print("The plaintext is = ",plain)







