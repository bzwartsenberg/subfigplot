#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 15:34:14 2018

@author: berend
"""

## Plotting class
import matplotlib.pyplot as plt
from matplotlib import rc


class GridPlot():
    
    def __init__(self,nx = 2, ny = 2, xsize = 4, ysize = 3, sizetype = 'subplot',
                 xspace = 0.25, yspace = 0.25, xmarg = 0.5, ymarg = 0.5, 
                 fontsize = 15, labelfontsize = 20, font = 'Myriad Pro', tickdirection = 'in',
                 ticklength = 3, tickwidth = 1,
                 xlabel = None, ylabel = None, axislabels = 'full'):
        """Initialize the class
        Args:
            nx,ny: number of subplots in the grid
            xsize, ysize: sizes in x and y direction
            sizetype: if subplot, xsize and ysize refer to subplot size, if global it is the global size
            xspace, yspace, xmarg, ymarg: x and y spacings, and x and y margins
            fontsize: fontsize
            font: font for labels etc
            tickdirection: way the ticks are pointing
            xlabel: label for all of the x axes
            ylabel: label for all of the y axes
            axislabels: option to turn some labels off, 'full' is all labels
                'ally' turns all xlabels off, except the lowest row, 'allx'
                turns all ylabels off except the leftmost row, 'outside' only
                the outside row, 'none' turns all axis labels off
                
            Creates an .fig .axes attributes, the latter is a list of lists to the axes as
            [xi,yi] from bottom left
            """
        
        #it's a bit sloppy to set this globally, maybe change this
        rc('font',**{'family':'sans-serif','sans-serif':['Myriad Pro'], 'size' : fontsize})
                    
        ## first determine the dimensions
        
        self.nx = nx
        self.ny = ny
        self.xsize = xsize
        self.ysize = ysize
        self.sizetype = sizetype
        self.xspace = xspace
        self.yspace = yspace
        self.xmarg = xmarg
        self.ymarg = ymarg
        self.fontsize = fontsize
        self.labelfontsize = labelfontsize
        self.font = font
        self.tickdirection = tickdirection
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.axislabels = axislabels
        
        self.figsizex, self.figsizey, self.subsizex, self.subsizey = self.getsizes()
        
        print('Making figure of size: %0.2f by %0.2f' % (self.figsizex,self.figsizey))
        print('Sub figures of size: %0.2f by %0.2f' % (self.subsizex,self.subsizey))
        
        
        self.fig = plt.figure(figsize = (self.figsizex,self.figsizey))
        self.axes = []
        
        for xi in range(nx):
            yaxes = []
            for yi in range(ny):
                yaxes.append(self.fig.add_axes(self.get_subfigpos(xi,yi)))
                yaxes[-1].tick_params(axis='both', direction = tickdirection, 
                                length = ticklength, width = tickwidth)
                self.labelaxes(xi,yi,yaxes[-1])
            self.axes.append(yaxes)
            
        
        
#            





    def getsizes(self):
        """Calc sizes of the actual figure and the subfigures"""
        
        
        if self.sizetype == 'global':
            figsizex = self.xsize
            figsizey = self.ysize
            subsizex = (figsizex - 2*self.xmarg - (self.nx-1)*self.xspace)/self.nx
            subsizey = (figsizey - 2*self.ymarg - (self.ny-1)*self.yspace)/self.ny
        elif self.sizetype == 'subplot':
            subsizex = self.xsize
            subsizey = self.ysize
            figsizex = 2*self.xmarg + self.nx*subsizex + (self.nx-1)*self.xspace
            figsizey = 2*self.ymarg + self.ny*subsizey + (self.ny-1)*self.yspace

        return figsizex, figsizey, subsizex, subsizey

            
    def get_subfigpos(self, xi, yi):
        """Get the list of positions to pass to add_axes
        Args:
            xi,xj: grid position of the sub figure"""
        
        pos = []
        pos.append((self.xmarg + xi*(self.xspace + self.subsizex))/self.figsizex)
        pos.append((self.ymarg + yi*(self.yspace + self.subsizey))/self.figsizey)
        pos.append(self.subsizex/self.figsizex)
        pos.append(self.subsizey/self.figsizey)
        return pos
            
    def labelaxes(self,xi,yi,ax):
        """Label the axes depending on given parameters and xi, yi"""
        
        if self.xlabel is not None:
            ax.set_xlabel(self.xlabel, fontname=self.font, fontsize=self.labelfontsize)                
        if self.ylabel is not None:
            ax.set_ylabel(self.ylabel, fontname=self.font, fontsize=self.labelfontsize)

        ## the corner plot always gets labels, except if labels are set to 'none':
        if self.axislabels == 'none':
            ax.set_xticklabels([])
            ax.set_xlabel('')
            ax.set_yticklabels([])
            ax.set_ylabel('')
        elif not self.axislabels == 'full':
            if xi == 0 and yi != 0:
                if self.axislabels in ['outside', 'ally']:
                    ax.set_xticklabels([])
                    ax.set_xlabel('')
            elif xi != 0 and yi == 0:
                if self.axislabels in ['outside', 'allx']:
                    ax.set_yticklabels([])
                    ax.set_ylabel('')                    
            elif xi != 0 and yi != 0:
                if self.axislabels in ['outside', 'allx']:
                    ax.set_yticklabels([])
                    ax.set_ylabel('')
                if self.axislabels in ['outside', 'ally']:
                    ax.set_xticklabels([])
                    ax.set_xlabel('')
                    
    def get_figax(self,i = 0,j = 0):
        
        return (self.fig, self.axes[i][j])
                    
            
                    
if __name__ == "__main__":
    
    ##test
    
    gp = GridPlot(nx = 2, ny = 2, xsize = 2, ysize = 2, sizetype = 'subplot',
                 xspace = 0.2, yspace = 0.2, xmarg = 0.5, ymarg = 0.5, 
                 fontsize = 15, labelfontsize = 20, font = 'Myriad Pro', tickdirection = 'in',
                 xlabel = 'asdf', ylabel = '', axislabels = 'outside')
    
    print(gp.fig.get_size_inches())
    
    for i in range(2):
        for j in range(2):
            gp.axes[i][j].plot([1,2,3])
    
    plt.savefig('testfig.png')
    plt.show()
    
    
    
            
            