#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 09:43:42 2018

@author: berend
"""

from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import numpy as np


c0 = (255/255.,255/255.,255/255.)
c1 = (98/255., 138/255., 229/255.)
c2 = (67/255., 209/255., 85/255.)


lightbluegreen = LinearSegmentedColormap.from_list('lightbluegreen',[c0,c1,c2])





if __name__ == '__main__':
    x = np.linspace(0,10,500)
    y = np.linspace(0,10,500)
    
    x,y = np.meshgrid(x,y)
    
    z = np.sqrt(x**2 + y**2)
    
    fig,ax = plt.subplots(figsize = (5,5))
    
    ax.pcolormesh(x,y,z, cmap = lightbluegreen)
    
    
    ax.axis([0,10,0,10])