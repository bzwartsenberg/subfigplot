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
    
    
def annotate_line(ax, label, atxval = None, atn = None, text = None, x_off = 1., y_off = 1., 
                  rotation = None, textkwargs = {}, unit = 'mm', rotation_avg = 1):
    """Annotate a label in an axis as text next to the line, on the point specified
    args:
        ax: the axes
        atxval, atn: at least one should be given, atn specifies the bin, atxval specifies the x_val
        label: the label of the line to look for
        text: text to annotate (if not given, label is used)
        x_off,y_off offsets of the text to the point on the curve specified
        rotation: rotation off the text. If None, use the approximate slope of the curve"""
        
    
    #getline
    for line in ax.lines:
        if line.get_label() == label:
            break
        
    if atn is None:
        if atxval is None:
            raise ValueError('Either atn or atxval must be not None')
        else:
            atn = (np.abs(line.get_xdata() - atxval)).argmin()
            
    #get x,y val:
    if atxval is not None: 
        x,y = atxval, line.get_ydata()[atn]
    else:
        x,y = line.get_xdata()[atn], line.get_ydata()[atn]
        
    if unit == 'mm':
        x_off *= ax.get_figure().dpi/25.4
        y_off *= ax.get_figure().dpi/25.4
    elif unit == 'in':
        x_off *= ax.get_figure().dpi
        y_off *= ax.get_figure().dpi


#    print('x point used:', x)
#    print('y point calculated:', y)
        
    ## transform offsets to axis values
    r0,r1 = ax.transData.inverted().transform([(-x_off,-y_off),(0.,0.)])
    x_off_ax,y_off_ax = r1-r0

#    print('x_offset in coord space:', x_off_ax)
#    print('y_offset in coord space:', y_off_ax)

    
    #get text:
    if text is None:
        text = label
    
    ## get color, and add to "std_textkwargs"
    std_textkwargs = {'fontname' : 'Myriad Pro',
                      'fontsize' : 10,
                        'color' : line.get_color(),
                        'va' : 'bottom',
                        'ha' : 'left',
                        'rotation' : 0.0
                        }   
    textkwargs = dict(std_textkwargs, **textkwargs)
    
    ##plot text
    t = ax.text(x + x_off_ax, y + y_off_ax, text, **textkwargs)
    
    
    
    if rotation is None: #set rotation based on curve
        bb = t.get_window_extent(renderer=ax.get_figure().canvas.get_renderer())
        sign = 1. if t.get_ha() == 'left' else -1. #if left aligned, go right, else go left
        
#        print('Sign used is ', sign)
        
        r0,r1 = ax.transData.inverted().transform([(0.,0.),(sign*bb.width,0)])
        t_xw_ax = (r1-r0)[0] #get the text offset in coordinate space.
#        print('width in coordinate space is ', t_xw_ax)
        
        t_start_atn = (np.abs(line.get_xdata() - (x + x_off_ax))).argmin()
        t_end_atn = (np.abs(line.get_xdata() - (x + x_off_ax + t_xw_ax))).argmin()
        
        #could add some averging here?
        avg = int((rotation_avg - 1)/2)
        t_yend_ax = np.mean(line.get_ydata()[t_end_atn-avg:t_end_atn+avg+1])
        t_ystart_ax = np.mean(line.get_ydata()[t_start_atn-avg:t_start_atn+avg+1])
        
#        print('Height start, end and diff in coordinate space is ',t_ystart_ax, t_yend_ax, t_yend_ax - t_ystart_ax)
#        print('Coords to be transformed: ', x + x_off_ax,t_ystart_ax, x + x_off_ax + t_xw_ax, t_yend_ax)
        r0,r1 = ax.transData.transform([(x + x_off_ax,t_ystart_ax),(x + x_off_ax + t_xw_ax,t_yend_ax)])
#        print('Display coordinates: ', r0, r1)
#        print('Display differences: ', (r1-r0)[0], (r1-r0)[1])
        
        rotation = np.arctan2((r1-r0)[1],(r1-r0)[0])*180/np.pi
#        print('Rotation is: ', rotation)

        
    t.set_rotation_mode('anchor')
    t.set_rotation(rotation)

        
