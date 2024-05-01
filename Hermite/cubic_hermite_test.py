def get_derivative(a,b,c,d,e,f):
			if d==e or f==e:
			   return 0
			delta_k_0=(e-d)/(b-a)
			delta_k_1=(f-e)/(c-b)
			der=2/((1/delta_k_0)+(1/delta_k_1))
			if (der/delta_k_0)<0 or (der/delta_k_1)<0:
				der=0
			elif math.sqrt(((der/delta_k_0)**2+(der/delta_k_1)**2))>3:
				der=der/(math.sqrt(((der/delta_k_0)**2+(der/delta_k_1)**2))/3)
			return der

def get_derivative_node(a,b,d,e,f):
			if d==e or f==e:
			   return 0
			delta_k_0=(e-d)/(b-a)
			der=1.5*delta_k_0-0.5*f
			return der

def cubic_hermite(x,y,target):
	"""
	    >>> cubic_hermite([0,2],[1,22,3], 3)
	    Please double check your input arrays. Make sure each x corresponds to a y.
	    >>> cubic_hermite([0,2],[1,22], 'a')
	    Please input your target as a number.
	    >>> cubic_hermite([5],[21], 3.6)
	    Please input more than two numbers in an array.
	    >>> cubic_hermite([0,2],[1,22], 3)
	    Your target is out of range. Please input your target again.
	    >>> cubic_hermite([0.1,0.25,0.5,0.75,1,3,5,7,10,20,30,50],[3.4809,3.4945,3.4626,3.5059,3.5359,3.5500,3.5600,3.5670,3.57,3.57,3.58,3.58], 0.25)
	    3.4945
	    >>> cubic_hermite([0.1,0.25,0.5,0.75,1,3,5,7,10,20,30,50],[3.4809,3.4945,3.4626,3.5059,3.5359,3.5500,3.5600,3.5670,3.57,3.57,3.58,3.58], 0.26)
	    3.49435
	"""
	import math
	n=len(x)
	m=len(y)
	if n!=m:
		print('Please double check your input arrays. Make sure each x corresponds to a y.')
		return
	elif isinstance(target, int)==0 and isinstance(target, float)==0:
			print('Please input your target as a number.')
			return
	elif n<=1:
		print('Please input more than two numbers in an array.')
		return
	elif target>x[n-1]:
		print('Your target is out of range. Please input your target again.')
		return
	for i in range(0,n-1):
		if target<x[i+1] and target>x[i]:
			key_0=x[i+1]-x[i]
			key_1=x[i+1]-target
			key_2=target-x[i]
			H_1=3*((key_1**2)/(key_0**2))-2*((key_1**3)/(key_0**3))
			H_2=3*((key_2**2)/(key_0**2))-2*((key_2**3)/(key_0**3))
			H_3=((key_1**2)/key_0)-((key_1**3)/(key_0**2))
			H_4=((key_2**3)/(key_0**2))-((key_2**2)/key_0)
			if n==2:
			   d_1=(y[1]-y[0])/(x[1]-x[0])
			   d_2=d_1
			else:
			   if i==0:
			       d_2=get_derivative(x[0],x[1],x[2],y[0],y[1],y[2])
			       d_1=get_derivative_node(x[0],x[1],y[0],y[1],d_2)
			   elif i==n-2:
			       d_1=get_derivative(x[n-3],x[n-2],x[n-1],y[n-3],y[n-2],y[n-1])
			       d_2=get_derivative_node(x[n-2],x[n-1],y[n-2],y[n-1],d_1)
			   else:
			       d_1=get_derivative(x[i-1],x[i],x[i+1],y[i-1],y[i],y[i+1])
			       d_2=get_derivative(x[i],x[i+1],x[i+2],y[i],y[i+1],y[i+2])
			result=y[i]*H_1+y[i+1]*H_2+d_1*H_3+d_2*H_4
			result=round(result,5)
			break
	for o in range(0,n):
			if target==x[o]:
			      result=y[o]
			      break
	return result

if __name__ == '__main__':
	import doctest
	doctest.testmod(verbose=True)