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
    found = False
    for line in ax.lines:
        if line.get_label() == label:
            found = True
            break
    if not found:
        raise RuntimeError('Axis label not found')
        
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


def annotate_scatter(ax, label, atxval = None, atn = None, text = None, x_off = 1., y_off = 1., 
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
    found = False
    for col in ax.collections:
        if col.get_label() == label:
            found = True
            break
    if not found:
        raise RuntimeError('Axis label not found')
        
    if atn is None:
        if atxval is None:
            raise ValueError('Either atn or atxval must be not None')
        else:
            atn = (np.abs(col.get_offsets()[:,0] - atxval)).argmin()
            
    #get x,y val:
    x,y = col.get_offsets()[atn,0], col.get_offsets()[atn,1]
        
    if unit == 'mm':
        x_off *= ax.get_figure().dpi/25.4
        y_off *= ax.get_figure().dpi/25.4
    elif unit == 'in':
        x_off *= ax.get_figure().dpi
        y_off *= ax.get_figure().dpi

        
    ## transform offsets to axis values
    r0,r1 = ax.transData.inverted().transform([(-x_off,-y_off),(0.,0.)])
    x_off_ax,y_off_ax = r1-r0

    
    #get text:
    if text is None:
        text = label
        
    if col.get_facecolors().shape[0] > 1:
        textcolor = col.get_facecolors()[atn]
    else:
        textcolor = col.get_facecolors()[0]
        
    
    ## get color, and add to "std_textkwargs"
    std_textkwargs = {'fontname' : 'Myriad Pro',
                      'fontsize' : 10,
                        'color' : textcolor,
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
        
        t_start_atn = (np.abs(col.get_offsets()[:,0] - (x + x_off_ax))).argmin()
        t_end_atn = (np.abs(col.get_offsets()[:,0] - (x + x_off_ax + t_xw_ax))).argmin()
        
        #could add some averging here?
        avg = int((rotation_avg - 1)/2)
        t_yend_ax = np.mean(col.get_offsets()[t_end_atn-avg:t_end_atn+avg+1,1])
        t_ystart_ax = np.mean(col.get_offsets()[t_start_atn-avg:t_start_atn+avg+1,1])
        
        r0,r1 = ax.transData.transform([(x + x_off_ax,t_ystart_ax),(x + x_off_ax + t_xw_ax,t_yend_ax)])
        
        rotation = np.arctan2((r1-r0)[1],(r1-r0)[0])*180/np.pi

        
    t.set_rotation_mode('anchor')
    t.set_rotation(rotation)



    
def axis_corner_box(ax, text, bwidth, bheight, loc = 'tl', box_props = {}, text_props = {}, units = 'mm'):
    
    """Axis cornerbox
    Args:
        ax: the axis to plot on
        text: the text to plot
        bwidth: box width in "units"
        bheight: box height in "units"
        loc: location, tl (top left), tr, bl, br
        box_props: matplotlib box properties
        text_props: matplotlib text properties
        units: mm or in"""
    
    if units == 'mm':
        uc = 1/25.4
    else:
        uc = 1.


    bbox = ax.get_window_extent().transformed(ax.get_figure().dpi_scale_trans.inverted())
    ax_xlim,ax_ylim = ax.get_xlim(),ax.get_ylim()
    axwidth = (ax_xlim[1]-ax_xlim[0])*bwidth*uc/bbox.width
    axheight = (ax_ylim[1]-ax_ylim[0])*bheight*uc/bbox.height


    if loc == 'tl':
        ptx,pty = (ax_xlim[0]),(ax_ylim[1]-axheight)
    elif loc == 'tr':
        ptx,pty = (ax_xlim[1] - axwidth),(ax_ylim[1]-axheight)
    elif loc == 'bl':
        ptx,pty = (ax_xlim[0]),(ax_ylim[0])
    elif loc == 'br':
        ptx,pty = (ax_xlim[1] - axwidth),(ax_ylim[0])
        
    print('Making text: ', text)

    box_props_std = dict(facecolor='white', alpha=1.0, lw = 0.5, edgecolor = 'black', zorder = 4) 
    text_props_std = dict(zorder = 4)
    box_props = dict(box_props_std, **box_props)
    text_props = dict(text_props_std, **text_props)
    textbox(ax,text, (ptx), (pty), axwidth, axheight, 
            boxkwargs = box_props, 
            textkwargs = text_props)

        
