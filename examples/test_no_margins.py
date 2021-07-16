#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 18:35:53 2018

@author: berend
"""

##no margins test:
    
    
import matplotlib.pyplot as plt
import numpy as np


x = np.linspace(-np.pi,np.pi,100)
y = x
X,Y = np.meshgrid(x,y)

Z = np.cos(X)+np.cos(Y)

fig = plt.figure(figsize = (2,2))

ax = fig.add_axes([0.0,0.0,1.0,1.0])
ax.imshow(Z)

fig.savefig('test.png')