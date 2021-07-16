#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 17:44:30 2019

@author: berend
"""

# Plot_panels:

import matplotlib.pyplot as plt



def plotpanels(sf, border = 1, save_base_name = 'subfig', ext = '.png', spines_lw = 0.3):
    
    mm = 25.4
        
    size_x,size_y = sf.figsize


    for l in sf.labels:
        fig = plt.gcf()
        fig.clear()

        ax_size = sf.get_fig_ax_pos(l)[2:4]
        

        figsize = (ax_size[0]*size_x + 2*border/mm, ax_size[1]*size_y + 2*border/mm)
        
    
        fig.set_size_inches(figsize)
        
        ax_pos = [border/mm/figsize[0], border/mm/figsize[1], ax_size[0]*size_x/figsize[0],ax_size[1]*size_y/figsize[1]]

        
        ax = fig.add_axes(ax_pos)
        ax.tick_params(axis='both', direction = sf.tickdirection, 
                            length = sf.ticklength, width = sf.tickwidth)    
        
        
        label_axis(l, ax, sf)
        
        axtw = sf.plotfuncs[l](ax)
        
        move_spines(ax, lw = spines_lw)
        
        if axtw is not None:
            move_spines(axtw, lw = spines_lw)
        
        fig.savefig(save_base_name + l + ext, dpi = 600)
        
        
def move_spines(ax, zorder = 10, lw = None):
        for loc,spine in ax.spines.items():
            spine.set_zorder(zorder)
            if lw is not None:
                spine.set_linewidth(lw) 
    
    
def label_axis(l, ax, sf):
    """Label the axes depending on given parameters and xi, yi"""
    

    ## the corner plot always gets labels, except if labels are set to 'none':
    whichlabels = sf.axislabel_params['whichlabels']
    ax.set_xlabel(sf.axislabel_params['xlabel'], fontname=sf.axislabel_params['font'], fontsize=sf.axislabel_params['fontsize'])                
    ax.set_ylabel(sf.axislabel_params['ylabel'], fontname=sf.axislabel_params['font'], fontsize=sf.axislabel_params['fontsize'])
    
    if l in sf.custom_ax.keys():
        ax.set_xticklabels([])
        ax.set_xlabel('')
        ax.set_yticklabels([])
        ax.set_ylabel('')                
    else:
        xi,yi = sf.label_pos[l]
        if whichlabels == 'none':
            ax.set_xticklabels([])
            ax.set_xlabel('')
            ax.set_yticklabels([])
            ax.set_ylabel('')
        elif not whichlabels == 'full':
            if xi == 0 and yi != 0:
                if whichlabels in ['outside', 'ally']:
                    ax.set_xticklabels([])
                    ax.set_xlabel('')
            elif xi != 0 and yi == 0:
                if whichlabels in ['outside', 'allx']:
                    ax.set_yticklabels([])
                    ax.set_ylabel('')                    
            elif xi != 0 and yi != 0:
                if whichlabels in ['outside', 'allx']:
                    ax.set_yticklabels([])
                    ax.set_ylabel('')
                if whichlabels in ['outside', 'ally']:
                    ax.set_xticklabels([])
                    ax.set_xlabel('')    
    
    
    