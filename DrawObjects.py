#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 14:43:56 2018

@author: berend
"""
import matplotlib.pyplot as plt
import numpy as np


def textbox(ax, text, x, y, xsize, ysize, textkwargs = {}, boxkwargs = {}):
    
    box = plt.Rectangle((x,y),xsize,ysize, **boxkwargs)
    
    ax.add_patch(box)
    
    text_x = x + xsize/2
    text_y = y + ysize/2
    
    ax.text(text_x, text_y, text, va = 'center', ha = 'center', **textkwargs)

            
       
def arrow(ax, xstart, ystart, xend, yend, style = '->',  capsize = 1.0, caplength = 2.0,  lineprops = {}):
    
    ### styles: <->, <-, -> <|-|>, <|- and -|>

    ## plot line:
    
    if not 'lw' in lineprops:
        lineprops['lw'] = 1.
    if not 'color' in lineprops:
        lineprops['color'] = 'black'
    
    xstart_dis, ystart_dis = ax.transData.transform((xstart,ystart))
    xend_dis, yend_dis = ax.transData.transform((xend,yend))
    
    
    uvec1 = np.array([xend_dis - xstart_dis, yend_dis - ystart_dis])
    uvec2 = np.array([-yend_dis + ystart_dis,xend_dis - xstart_dis])

    
    uvec1 /= np.linalg.norm(uvec1)
    uvec2 /= np.linalg.norm(uvec2)
    
    start_dis = np.array([xstart_dis,ystart_dis])
    end_dis = np.array([xend_dis,yend_dis])

    width_pt = lineprops['lw']*capsize*2
    length_pt = lineprops['lw']*caplength*2    
    ##caps:
    pt_el = end_dis - uvec1*length_pt + uvec2*width_pt
    pt_em = end_dis - uvec1*length_pt
    pt_er = end_dis - uvec1*length_pt - uvec2*width_pt
    pt_sl = start_dis + uvec1*length_pt + uvec2*width_pt
    pt_sm = start_dis + uvec1*length_pt
    pt_sr = start_dis + uvec1*length_pt - uvec2*width_pt   
    
    if style == '->':
        pts = [start_dis, end_dis, pt_el, end_dis, pt_er]
    elif style == '-|>':
        pts = [start_dis, end_dis, pt_el, pt_er, end_dis, pt_el, pt_em]
    elif style == '<->':
        pts = [pt_sl, start_dis, pt_sr, start_dis, end_dis, end_dis, pt_el, end_dis, pt_er]
    elif style == '<-':
        pts = [pt_sl, start_dis, pt_sr, start_dis, end_dis]
    elif style == '<|-|>':
        pts = [pt_sm, pt_sl, start_dis, pt_sr, pt_sm, pt_em, pt_el, end_dis, pt_er, pt_em]
    elif style == '<|-|>':
        pts = [pt_sm, pt_sl, start_dis, pt_sr, pt_sl, start_dis, end_dis]
        
    pts = ax.transData.inverted().transform(pts)
    ax.plot(pts[:,0],pts[:,1], **lineprops)