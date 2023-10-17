import numpy as np

#Problem: Least Squares Adjustment of measurements of angles of a triangle
    #Angles are in degrees
    #One-sigma precisions of each measurement are 0.5 degrees of standard deviation
    #Measurements are uncorrelated (current angle total = 181deg)

#Method 1: Observations Only
    #n = 3
    #n0 = 2
    #r = 1
    #u = 0
    #c = 1

sigma = np.eye(3) * 0.25
A = np.array([[1, 1, 1]])
Atran = A.transpose()

#Measurements
l1 = 35
l2 = 70
l3 = 76
f = np.array([[180 - l1 -l2 - l3]])
print('f is:', f)

#Equivalent covariance matrix
sig_e = A @ sigma @ Atran
print('SIGMA_e is:', sig_e)

#Equivalent weight matrix
W = np.linalg.inv(sig_e)
print('W is:', W)

#Residuals
v = sigma @ Atran @ W @ f
print('v is:', v)

#Covariance of residuals
sigma_v = sigma @ Atran @ W @ A @ sigma
print('SIGMA_v is:', sigma_v)

#Adjusted observations
l = np.array([[l1], [l2], [l3]])
l_hat = l + v
print('L_hat is:', l_hat)

#Covariance matrix of adjusted observations
sigma_lhat = sigma - sigma_v
print('SIGMA_lhat is:', sigma_lhat)


#Method 2: Indirect Observations
    #n = 3
    #n0 = 2
    #r = 1
    #u = 2
    #c = 3

B = np.array([
    [-1, 0],
    [0, -1],
    [1, 1],
])
f2 = np.array([[-l1], [-l2], [180-l3]])
Btran = B.transpose()
W2 = np.linalg.inv(sigma)

N = Btran @ W2 @ B
print('N is:', N)

t = Btran @ W2 @ f2
print('t is:', t)

#Parameter values
Qd = np.linalg.inv(N)
delta = Qd @ t
print('DELTA is:', delta)

#Residuals
v2 = f2 - (B @ delta)
print('V is:', v2)

lhat2 = l + v2
print('lhat2 is:', lhat2)

#Covariance of parameters
sig_delta = np.linalg.inv(N)
print('SIGMA_delta is:', sig_delta)

#Covariance of Residuals
sigma_v2 = sigma - (B @ sig_delta @ Btran)
print('SIGMA_v is:', sigma_v2)

#Covariance Matrix of adjusted observations
sigma_lhat2 = sigma - sigma_v2
print('SIGMA_lhat is:', sigma_lhat2)

print('OO SIGMA_lhat is:', sigma_lhat)
print('IO SIGMA_lhat is:', sigma_lhat2)

equality_check = sigma_lhat - sigma_lhat2
print('Difference between OO and IO covariance is:', equality_check)

