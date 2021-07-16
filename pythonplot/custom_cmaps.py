#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 09:43:42 2018

@author: berend
"""

from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import numpy as np
import palettable

cmap1 = palettable.cartocolors.sequential.Teal_6.mpl_colormap
scolors1 = palettable.cartocolors.qualitative.Prism_10.mpl_colors



##light blue green:
c0 = (255/255.,255/255.,255/255.)
c1 = (98/255., 138/255., 229/255.)
c2 = (67/255., 209/255., 85/255.)


lightbluegreen = LinearSegmentedColormap.from_list('lightbluegreen',[c0,c1,c2])



teal_steps = 7
clrs_teal = cmap1(np.linspace(0.,1.,num = teal_steps))
scolors_sub = [scolors1[i] for i in [3,4,5,6,7,8,9,0]]
clrs_prism = np.ones((len(scolors_sub), 4))
clrs_prism[:,0:3] = np.array(scolors_sub)
TealRainbow = LinearSegmentedColormap.from_list('Tealrainbow1', np.concatenate([clrs_teal, clrs_prism]))




            
teal_steps = 5
clrs_teal = cmap1(np.linspace(0.,1.,num = teal_steps))
scolors_sub = [scolors1[i] for i in [0,9,8,7,6,5]]
clrs_prism = np.ones((len(scolors_sub), 4))
clrs_prism[:,0:3] = np.array(scolors_sub)
TealRainbow2 = LinearSegmentedColormap.from_list('Tealrainbow2', np.concatenate([clrs_teal, clrs_prism]))




if __name__ == '__main__':
    x = np.linspace(0,10,500)
    y = np.linspace(0,10,500)
    
    x,y = np.meshgrid(x,y)
    
    z = np.sqrt(x**2 + y**2)
    
    fig,ax = plt.subplots(figsize = (5,5))
    
    ax.pcolormesh(x,y,z, cmap = lightbluegreen)
    
    
    ax.axis([0,10,0,10])
    
    
    
    
    
    