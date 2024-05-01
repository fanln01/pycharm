'''
得到除两个端点外的范围间每个节点的导数
'''
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
'''
得到两个端点的导数
'''
def get_derivative_node(a,b,d,e,f):
			if d==e or f==e:
			   return 0
			delta_k_0=(e-d)/(b-a)
			der=1.5*delta_k_0-0.5*f
			return der
'''
求目标点的单调三次hermite多项式插值
'''
def cubic_hermite_polynomial(x, y):
    import numpy as np
    n = len(x)
    m = len(y)
    if n != m:
        print('Please double check your input arrays. Make sure each x corresponds to a y.')
        return
    elif n <= 1:
        print('Please input more than two numbers in an array.')
        return
    coefficients = []
    for i in range(0, n-1):
        key_0 = x[i+1] - x[i]
        if n == 2:
            d_1 = (y[1] - y[0]) / (x[1] - x[0])
            d_2 = d_1
        else:
            if i == 0:
                d_2 = get_derivative(x[0], x[1], x[2], y[0], y[1], y[2])
                d_1 = get_derivative_node(x[0], x[1], y[0], y[1], d_2)
            elif i == n-2:
                d_1 = get_derivative(x[n-3], x[n-2], x[n-1], y[n-3], y[n-2], y[n-1])
                d_2 = get_derivative_node(x[n-2], x[n-1], y[n-2], y[n-1], d_1)
            else:
                d_1 = get_derivative(x[i-1], x[i], x[i+1], y[i-1], y[i], y[i+1])
                d_2 = get_derivative(x[i], x[i+1], x[i+2], y[i], y[i+1], y[i+2])
        # Calculate the coefficients of the cubic polynomial
        a = y[i]
        b = d_1
        c = (3 * (y[i+1] - y[i]) - (2 * d_1 + d_2) * key_0) / (key_0 ** 2)
        d = (2 * (y[i] - y[i+1]) + (d_1 + d_2) * key_0) / (key_0 ** 3)
        coefficients.append([a, b, c, d])
    return np.array(coefficients)


if __name__ == '__main__':
			x=[0.1,0.25,0.5,0.75,1,3,5,7,10,20,30,50]
			y=[3.4809,3.4945,3.4626,3.5059,3.5359,3.5500,3.5600,3.5670,3.57,3.57,3.58,3.58]
			cubic_hermite_polynomial(x,y,0.26)
			