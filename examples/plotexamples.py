#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 12:26:11 2017

@author: berend
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


## take a look at https://python4astronomers.github.io/plotting/advanced.html
##### plot functions #####

#EXAMPLE DATA
X = np.linspace(-20,20,200)
Y = np.linspace(-10,10,200)
XX,YY = np.meshgrid(X,Y)
RR = np.sqrt(XX**2+YY**2)
ZZ = (1-RR**2)*np.exp(-RR**2/2)*XX
Z0 = Y**0
Z1 = Y**1
Z2 = Y**2
Z3 = Y**3
Z4 = Y**4
Z5 = Y**5



#IMAGE PLOTS


fig,ax = plt.subplots(figsize = (6,6)) #make the figure, 1 row, 1 col, size 6x6 in
vmin = np.min(ZZ) # cmap min
vmax = np.max(ZZ) # cmap max
im = ax.pcolormesh(XX,YY, ZZ, cmap = 'Spectral_r', vmin = vmin, vmax = vmax)
ax.axis([X[0],X[-1],Y[0],Y[-1]]) #set axis
ax.set_ylabel('yaxis', size = 24) #set axis label and size
ax.tick_params(labelsize = 15) #set tick label size
#alternatively, cmapobj = cm.Spectral_r
# cmapobj.setgamma(0.5) #set gamma to 0.5
# colormesh(XX,YY,ZZ,cmap = cmapobj) 

ax.set_xticks([-20.0,0.0,20.0]) # set custom major ticks for xaxis
ax.set_xticklabels(['spam','eggs','banana'], size = 24, rotation = 45) #set tick labels for ticks
#rotation also 'horizontal' or 'vertical'

fig.subplots_adjust(right = 0.9) #add 10% to figure
cbar_ax = fig.add_axes([0.925,0.1,0.05,0.8]) #make new axes in that space
fig.colorbar(im, cax = cbar_ax) # add a colorbar linked to the image in that space
cbar_ax.tick_params(labelsize = 18) #set the ticks for the colorbar
plt.show() #fig.show() will give warnings with Ipython


#ax.imshow(X,Z, asp = .., extent = ...)


## SUBPLOTS WITH LINEPLOTS
fig,axes = plt.subplots(3,2,figsize = (8,12)) #make the figure, 1 row, 1 col, size 6x6 in
axes[0,0].scatter(Y,Z0, color = 'blue', marker = '.', linewidth = 0.0)
axes[0,1].loglog(Y,Z1,color = 'black')
axes[1,0].plot(Y,Z2, linestyle = 'none', color = 'red', marker = 's')
axes[1,0].hlines(50,-100,100,linestyle = 'dashed', color = 'gray')
axes[1,0].vlines(0,-100,100,linestyle = 'dashed', color = 'gray')
axes[1,0].axis([Y[0],Y[-1],-10,100])
#with legend: (label is defined in plot!)
axes[1,1].plot(Y,Z3,color = 'black', linestyle = 'dashed', label = '$Z = X^3$') #also linestyle = '- -'
legend = axes[1,1].legend(loc='upper left', shadow=False, fontsize=20)
legend.get_frame().set_facecolor('#3897b7')
axes[2,0].scatter(Y,Z4,c = Z1,s = Z2, cmap = 'autumn', linewidth = 0.0)
r = (Z3-np.min(Z3))/(np.max(Z3)-np.min(Z3))
g = np.linspace(0.439,0.439,200) # color gradient for red
b = np.linspace(0.768,0.768,200)
a = Z2/np.max(Z2) #transparency
c = np.array([r,g,b,a]).T
axes[2,1].scatter(Y,Z5, c = c, linewidth = 0.0)
for axax in axes:
    for ax in axax:
        ax.tick_params(labelsize = 8)
        
        
fig,ax1 = plt.subplots(figsize = (4,4))
ax1.semilogy(Y,Z2,linestyle = 'none', color = 'red', marker = 'o')
ax2 = ax1.twinx()
ax2.plot(Y,Z1,linestyle = 'none', color = 'black', marker = '^')
for label in ax1.get_xmajorticklabels():
    label.set_rotation(45)
plt.show()

fig, ax = plt.subplots(figsize = (4,4))
x = np.linspace(0,10.,20)
yerr = np.sqrt(x)
ax.errorbar(x, x, yerr = yerr, marker = 'o', capsize = 5)
plt.show()

fig, ax = plt.subplots(figsize = (4,4))
ax.fill_between(Y, 0, Z2, color = 'grey')
plt.show()



#surface plot. 
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Make data
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x = 10 * np.outer(np.cos(u), np.sin(v))
y = 10 * np.outer(np.sin(u), np.sin(v))
z = 10 * np.outer(np.ones(np.size(u)), np.cos(v))

# Plot the surface
ax.plot_surface(x, y, z, color='b')

plt.show()