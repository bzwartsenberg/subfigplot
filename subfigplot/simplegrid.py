#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 10:43:26 2018

@author: berend
"""

from subfiggrid import SubfigGrid



class SimpleGrid(SubfigGrid):
    """Create a subfiggrid with standard parameters that is easy to adapt."""
    
    def __init__(self,nx = 1, ny = 1, figsizesx = 70., figsizesy = 70., 
                 xspaces = 7., yspaces = 7., labels = None, label_pos = None, 
                 plotfuncs = {},text_params = {}, tick_params = {}, axislabel_params = {}, 
                 label_params = {}, units = 'mm', custom_ax = {}):
        """Create a SubFig grid with std parameters
        Args:
            nx, ny: number of plots in x and y direction
            figsizesx, figsizesy: size of the subfigures in x and y, can be float or list
            xpaces, yspaces: distance between subfigs, can be float or list
            labels: figure labels, if None, use 'a', 'b', 'c' etc. 
            label_pos: list of grid positions, if none, use top to bottom, left to right
            plotfuncs: dictionary of functions to plot for every axis
            text_params: text parameters  (see SubfigGrid)
            tick_params: tick parameters  (see SubfigGrid)
            axislabel_params: axis label params  (see SubfigGrid)
            label_params: sub fig labelling params (see SubfigGrid)
            units: units to use, 'mm' or 'in'
            custom_ax: positions of axes in (units) to overwrite pos described by  label_pos
            """
        self.nx = nx
        self.ny = ny
        if not type(figsizesx) == list:
            figsizesx = [figsizesx for i in range(nx)]
        if not type(figsizesy) == list:
            figsizesy = [figsizesy for i in range(ny)]
        if not type(xspaces) == list:
            xspaces = [xspaces for i in range(nx+1)]
        if not type(yspaces) == list:
            yspaces = [yspaces for i in range(ny+1)]


        if labels is None:
            labels = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p',
                      'q','r','s','t','u','v','w','x','y','z'][0:(nx*ny)]
        if label_pos is None:
            label_pos = [(i,j) for j in reversed(range(ny)) for i in range(nx)]

        text_params_std = {'font' : 'Myriad Pro',
                       'fontsize': 14}
        text_params = dict(text_params_std, **text_params)               
        
        tick_params_std = {'ticklength' : 2,
                       'tickdirection': 'in'}
        tick_params = dict(tick_params_std, **tick_params)               

        
        axislabel_params_std = {'xlabel' : '',
                                'ylabel' : '',
                                'font' : 'Myriad Pro',
                                'fontsize' : 12,
                                'whichlabels' : 'outside', #can be full, none, allx, ally, outside
                                }      
        axislabel_params = dict(axislabel_params_std, **axislabel_params)               

                                
        label_params_std = {'bwidth' : 6,
                            'bheight' : 6,
                            'loc' : 'tr',
                            'makelabels' : False,
                            'box_props' : {'fc' : 'grey', 'lw' : 0, 'alpha' : 0.5, 'ec' : 'black'},
                            'text_props' : {'color' : 'white', 'fontsize' : 12},
                            }
        label_params = dict(label_params_std, **label_params)               
        
        plotfuncs_std = {l : (lambda *args: None) for l in labels}
        plotfuncs = dict(plotfuncs_std,**plotfuncs)
    
    
        super().__init__(figsizesx, figsizesy, xspaces, yspaces, labels, label_pos,plotfuncs,
                     text_params = text_params, tick_params = tick_params, 
                     axislabel_params = axislabel_params, label_params = label_params,
                     units = units, custom_ax = custom_ax)
        
        self.a = self.axes
