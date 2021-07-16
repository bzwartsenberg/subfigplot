#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 08:33:07 2018

@author: berend
"""
import matplotlib.pyplot as plt
###Random subfigures with extras:
    
    
class make_figure():
    def __init__(self,figsizesx, figsizesy, xspaces, yspaces):
    
        
        figsizex = sum(figsizesx)+sum(xspaces)
        figsizey = sum(figsizesy)+sum(yspaces)
        
        self.figsize = (figsizex,figsizey)
        print('Calculated fig size: %0.2f by %0.2f in' % self.figsize)
        
        fig = plt.figure(figsize = self.figsize)
        axes = []

        self.figsizesx = figsizesx
        self.figsizesy = figsizesy
        self.xspaces = xspaces
        self.yspaces = yspaces
        
        self.labels = ['a','b','c','d','e','f','g','h','i','bar_ls','bar_bandwt']
        self.label_pos = dict(zip(self.labels,[(1,1),(2,1),(3,1),(4,1),(0,0),(1,0),(2,0),(3,0),(4,0)]))
        self.axes_pos = {'a' : [sum(self.xspaces[:])]}

        
        
    def get_fig_ax_pos(self,label):
        
        if label == 'bar_ls':
            pos = []
        elif label == 'bar_bandwt':
            pos = []
        else:
            pos = []
            pos.append(sum(self.xspaces[:self.label_pos[label][0]+1])+sum(self.figsizesx[:min(self.label_pos[label][0]-1,0)]))
            pos.append(sum(self.yspaces[:self.label_pos[label][1]+1])+sum(self.figsizesy[:min(self.label_pos[label][1]-1,0)]))
            pos.append(self.figsizesx[self.label_pos[label][0]])
            pos.append(self.figsizesy[self.label_pos[label][1]])
            
            
        return pos
    