#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 15:49:24 2018

@author: berend
"""
import numpy as np

def create_grid_pcolormesh(x,y):
    
    if len(x.shape) > 1:
        x = x[0,:]
        y = y[:,0]
    
    xnew = np.zeros(x.shape[0]+1)
    ynew = np.zeros(y.shape[0]+1)
        
    xnew[1:-1] = (x[1:] + x[:-1])/2
    ynew[1:-1] = (y[1:] + y[:-1])/2
    
    #extrapolate the end values:
    xnew[0] = xnew[1] - x[1] + x[0]
    ynew[0] = ynew[1] - y[1] + y[0]

    xnew[-1] = xnew[-2] + x[-1] - x[-2]
    ynew[-1] = ynew[-2] + y[-1] - y[-2]
    
    return xnew,ynew



def to_sym(A, vmin, vmax, zero = 0.0):
    """Convert to symmetrical colorscale, this means if a divergence map
    goes from -0.5 to 1.0, you can represent it through the full colorscale
    but still keep 0.0 at 0.0.
    Args:
        A: the array to transform
        vmin: the value in array that will be transformed to -1.
        vmax: the value in the array that will be transformed to 1.
        zero: the value that will be transformed to zero"""
    
    
    return A/np.piecewise(A, [A < zero], [-vmin,vmax])


def sym_colorbar(ax, vmin,vmax, cmap, zero=0.0,  inside_labels=[],
                 textprops={}, horizontal=False):
    
    y = np.linspace(vmin,vmax, 200)
    x = np.linspace(-1,1,2)
    if horizontal:
        x, y = y, x
    
    X,Y = np.meshgrid(x,y)

    if horizontal:
        Z = to_sym(X,vmin,vmax,zero = zero)
    else:
        Z = to_sym(Y,vmin,vmax,zero = zero)

    X,Y = create_grid_pcolormesh(X,Y)

    ax.pcolormesh(X,Y,Z,cmap = cmap, vmin = -1, vmax = 1., rasterized=True)
    if horizontal:
        ax.set_yticks([])
        ax.axis([vmin, vmax, -1,1])
    else:
        ax.set_xticks([])
        ax.axis([-1,1,vmin,vmax])

    if inside_labels:
        ylen = vmax - vmin
        
        ax.text(0., vmin + 0.02*ylen, inside_labels[0],ha = 'center', va = 'bottom',rotation = 90, **textprops)
        ax.text(0., vmax - 0.02*ylen, inside_labels[1],ha = 'center', va = 'top',rotation = 90, **textprops)
    
    
    
def reg_colorbar(ax, vmin,vmax, cmap, zero = 0.0, inside_labels = [],
                 textprops = {}, norm=None, horizontal=False):
    
    y = np.linspace(vmin,vmax, 200)
    x = np.linspace(-1,1,2)
    if horizontal:
        x, y = y, x
    
    X,Y = np.meshgrid(x,y)

    if horizontal:
        Z = np.array(X)
    else:
        Z = np.array(Y)
    
    X,Y = create_grid_pcolormesh(X,Y)
    
    ax.pcolormesh(X,Y,Z,cmap = cmap, vmin = vmin, vmax = vmax, norm=norm, rasterized=True)
    if horizontal:
        ax.set_yticks([])
        ax.axis([vmin, vmax, -1,1])
    else:
        ax.set_xticks([])
        ax.axis([-1,1,vmin,vmax])

    if inside_labels:
        ylen = vmax - vmin
        
        ax.text(0., vmin + 0.02*ylen, inside_labels[0],ha = 'center', va = 'bottom',rotation = 90, **textprops)
        ax.text(0., vmax - 0.02*ylen, inside_labels[1],ha = 'center', va = 'top',rotation = 90, **textprops)
