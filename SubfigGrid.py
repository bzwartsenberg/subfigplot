#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 12:31:42 2018

@author: berend
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from DrawObjects import textbox 
import bc

"""



"""

class SubfigGrid():
    def __init__(self,figsizesx, figsizesy, xspaces, yspaces, labels, label_pos,plotfuncs,
                 text_params = {}, tick_params = {}, axislabel_params = {}, label_params = {},
                 units = 'mm'):
    
        self.mm = 1/25.4

        print('Calculated fig size: %0.2f by %0.2f %s' % (sum(figsizesx)+sum(xspaces),sum(figsizesy)+sum(yspaces),units))
        
        
        if units == 'mm':
            figsizesx = [x*self.mm for x in figsizesx]
            figsizesy = [y*self.mm for y in figsizesy]
            xspaces = [x*self.mm for x in xspaces]
            yspaces = [y*self.mm for y in yspaces]
            self.uc = 1/25.4
        else:
            self.uc = 1.
        
        figsizex = sum(figsizesx)+sum(xspaces)
        figsizey = sum(figsizesy)+sum(yspaces)
                
        self.figsize = (figsizex,figsizey)
        
        self.units = units

        self.figsizesx = figsizesx
        self.figsizesy = figsizesy
        self.xspaces = xspaces
        self.yspaces = yspaces
        
        self.labels = labels
        self.label_pos = dict(zip(self.labels,label_pos))

        ##text params:
        self.labelfontsize = text_params['labelfontsize'] if 'labelfontsize' in text_params else 10
        self.ticklabelfontsize = text_params['ticklabelfontsize'] if 'ticklabelfontsize' in text_params else 7
        self.font = text_params['font'] if 'font' in text_params else 'Myriad Pro'
        
        #tick params
        self.ticklength = tick_params['ticklength'] if 'ticklength' in tick_params else 2.0
        self.tickdirection = tick_params['tickdirection'] if 'tickdirection' in tick_params else 'in'
        self.tickwidth = tick_params['tickwidth'] if 'tickwidth' in tick_params else 1.0
        
        #axislabel params
        # auto label like in GridPlot, and for which axes.
        axislabel_params_std = {'xlabel' : '',
                                'ylabel' : '',
                                'font' : 'Myriad Pro',
                                'fontsize' : 10,
                                'whichlabels' : 'full', #can be full, none, allx, ally, outside
                                }
        self.axislabel_params = dict(axislabel_params_std, **axislabel_params)
        
        #label params
        #should overwrite all that were missing, but take all from label_params if they are there.        
        label_params_std = {'bwidth' : 5*self.mm/self.uc,
                            'bheight' : 3*self.mm/self.uc,
                            'loc' : 'tl',
                            'makelabels' : True,
                            'box_props' : {},
                            'text_props' : {},
                            }
        self.label_params = dict(label_params_std, **label_params) 
        

        #set rc params:
        rc('font',**{'family':'sans-serif','sans-serif':[self.font], 'size' : self.ticklabelfontsize})
            
        
        self.fig = plt.figure(figsize = self.figsize)
        self.axes = self.make_axes()   
        
        for label in self.labels:
            try:
                plotfuncs[label](self.axes[label])
            except KeyError:
                print('No plot function found for %s or error in function' % label)
                pass
        
        self.label_axes()
            
        if self.label_params['makelabels']:
            self.make_subfiglabels()

        self.move_spines()

        self.remove_text_spines()

        
    def get_fig_ax_pos(self,label):
        
        if label == 'text':
            pos = [0,0,self.figsize[0],self.figsize[1]]
        else:
            pos = []
            pos.append(sum(self.xspaces[:self.label_pos[label][0]+1])+sum(self.figsizesx[:self.label_pos[label][0]]))
            pos.append(sum(self.yspaces[:self.label_pos[label][1]+1])+sum(self.figsizesy[:self.label_pos[label][1]]))
            pos.append(self.figsizesx[self.label_pos[label][0]])
            pos.append(self.figsizesy[self.label_pos[label][1]])
            
            
        return [p/s for p,s in zip(pos,2*[self.figsize[0],self.figsize[1]])]     


    def make_axes(self):
        
        
        axes = {}
        
        for label in self.labels:
            axes[label] = self.fig.add_axes(self.get_fig_ax_pos(label))
            axes[label].tick_params(axis='both', direction = self.tickdirection, 
                                length = self.ticklength, width = self.tickwidth)    

        return axes 
        
        
    def make_subfiglabels(self):
        
        for label in self.labels[0:len(self.label_pos)]:
            bbox = self.axes[label].get_window_extent().transformed(self.fig.dpi_scale_trans.inverted())
            ax_xlim,ax_ylim = self.axes[label].get_xlim(),self.axes[label].get_ylim()
            axwidth = abs(ax_xlim[1]-ax_xlim[0])*self.label_params['bwidth']*self.uc/bbox.width
            axheight = abs(ax_ylim[1]-ax_ylim[0])*self.label_params['bheight']*self.uc/bbox.height
           
            if self.label_params['loc'] == 'tl':
                ptx,pty = (ax_xlim[0]),(ax_ylim[1]-axheight)
            elif self.label_params['loc'] == 'tr':
                ptx,pty = (ax_xlim[1] - axwidth),(ax_ylim[1]-axheight)
            elif self.label_params['loc'] == 'bl':
                ptx,pty = (ax_xlim[0]),(ax_ylim[0])
            elif self.label_params['loc'] == 'br':
                ptx,pty = (ax_xlim[1] - axwidth),(ax_ylim[0])
            box_props_std = dict(facecolor='white', alpha=1.0, lw = 0.5, edgecolor = 'black', zorder = 4) 
            textkwargs_std = dict(zorder = 4)
            textbox(self.axes[label],label, (ptx), (pty), axwidth, axheight, 
                    boxkwargs = dict(box_props_std, **self.label_params['box_props']), 
                    textkwargs = dict(textkwargs_std, **self.label_params['text_props']))
            
    def label_axes(self):
        """Label the axes depending on given parameters and xi, yi"""
        

        ## the corner plot always gets labels, except if labels are set to 'none':
        whichlabels = self.axislabel_params['whichlabels']
        for xi in range(len(self.figsizesx)):
            for yi in range(len(self.figsizesy)):
                
                k,v = list(self.label_pos.keys()), list(self.label_pos.values())
                ax = self.axes[k[v.index((xi,yi))]]
                ax.set_xlabel(self.axislabel_params['xlabel'], fontname=self.axislabel_params['font'], fontsize=self.axislabel_params['fontsize'])                
                ax.set_ylabel(self.axislabel_params['ylabel'], fontname=self.axislabel_params['font'], fontsize=self.axislabel_params['fontsize'])
                
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
        
             
          
    def remove_text_spines(self):
        if 'text' in self.labels:
                
            for loc,spine in self.axes['text'].spines.items():
                spine.set_visible(False)
            self.axes['text'].set_xticks([])
            self.axes['text'].set_yticks([])   
            self.axes['text'].patch.set_alpha(0.0)
            self.axes['text'].axis([0.0,self.figsize[0]/self.uc,0.0,self.figsize[1]/self.uc])

        
    def move_spines(self, zorder = 10):
        for label in self.labels:
            for loc,spine in self.axes[label].spines.items():
                spine.set_zorder(zorder)            


                 
            
            
if __name__ == '__main__':
    
    #make some data:
    x = np.linspace(-5,10, 200)
    
    y1 = x**2 - 0.1*x**3
    y2 = x
    y3 = np.sin(x)
    y4 = 0.5**x    
    
    def plot_a(ax):
        ax.plot(x,y1, color = bc.red)
    def plot_b(ax):
        ax.plot(x,y2, color =  bc.green)    
    def plot_c(ax):
        ax.plot(x,y3, color =  bc.blue)    
    def plot_d(ax):
        ax.plot(x,y4)            
    
    figsizesx = [20, 30]
    figsizesy = [25,35]
    xspaces = [6,2,6]
    yspaces = [6,2,6]
    labels = ['a','b','c','d']
    label_pos = [(0,1),(1,1),(0,0),(1,0)]
    text_params = {'font' : 'Myriad Pro',
                   'fontsize': 12}
    tick_params = {'ticklength' : 2,
                   'tickdirection': 'in'}

    axislabel_params = {'xlabel' : 'test',
                            'ylabel' : 'asdf',
                            'font' : 'Myriad Pro',
                            'fontsize' : 10,
                            'whichlabels' : 'outside', #can be full, none, allx, ally, outside
                            }      
                            
    label_params = {'bwidth' : 5,
                        'bheight' : 3,
                        'loc' : 'tr',
                        'makelabels' : True,
                        'box_props' : {'fc' : 'grey', 'lw' : 2, 'alpha' : 0.5, 'ec' : 'purple'},
                        'text_props' : {'color' : 'white'},
                        }                            
    plotfuncs = [plot_a, plot_b, plot_c, plot_d]
    plotfuncs = dict(zip(labels,plotfuncs))
    
    
    mf = SubfigGrid(figsizesx, figsizesy, xspaces, yspaces, labels, label_pos,plotfuncs,
                 text_params = text_params, tick_params = tick_params, 
                 axislabel_params = axislabel_params, label_params = label_params,
                 units = 'mm')
    
    
#    mf.fig.savefig('fig.png', dpi = 600)        
    plt.show()


