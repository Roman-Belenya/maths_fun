#!/usr/bin/env python
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt

xs = []
betas = []

for beta in np.arange(0, 10, 0.001):

    print(beta)
    
    # initial value of x
    x = 0.5
    
    # iteate first 2000 times to stabilize
    for i in range(5000):
        x = (x-x**2) * beta # beta*x(1 - x)
    
    # continue iterating and save vals
    xss = x
    for i in range(10000):
        x = (x-x**2) * beta
        
        betas.append(beta)
        xs.append(x)
        
        if abs(xss - x) < 0.001:
            break
    
plt.scatter(betas, xs, s=0.01)
plt.xlim(3,10)
plt.show()




