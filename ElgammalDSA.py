import math

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
#At Bob 
p,alpha,d=97,23,67
#bita=(pow(alpha, d))%p
bita=15
print("Bita = alpha power d ",bita)
print("Bob will send ",'(',p,',',alpha, ',',bita ,')',"to Alice")
#############################################
x=57
print(findModularInverse(5, 96))
print("Message=",x)
KE=31
gcd=math.gcd(KE,p-1)
if(gcd==1):
    print("KE is valid and has inverse= " ,findModularInverse(KE, p-1))
else:
    print("KE has no inverse")
    
    
print ("Bob will compute r and s to make signture ")
    
#r=(pow(alpha,KE))%p
#s=((x-d*r)*31) % (p-1)
r=33
s=51
print ("r and s =",r,s)


#At Alice 
#compute t 
print("Alice will compute t then compare it with alpha power x mod p")
t=(pow(bita,r)*pow(r,s))%p
sign=pow(alpha, x)%p
print("After comparing t:",t,'==','sign:',sign ,"they are equal to othre ")
if(t==sign):
    print("Its valid signture ")
else:
    print("Its not valid signture ")


    
    




