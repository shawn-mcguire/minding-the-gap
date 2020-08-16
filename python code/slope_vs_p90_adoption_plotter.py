#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 10:17:43 2019

creates 1d bar plot of policy adoption rate broken out by p90 and slope

@author: shawnmcguire
"""
#%%

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
  
Y_LIM = 1.0 # axis limit for plot
COLOR_1 = 'orange' # bar colors
COLOR_2 = 'grey'
HEIGHT = 0.03 # vert position of n label
WIDTH = 0.7 # horiz position of n label
N_SIZE = 8 # n_label text size
BAR_WIDTH = 0.2 

#%%%
''' USER ENTRIES '''

#title = ('90th - 10th income percentile vs adoption rate \n All domains \n \
#        (cases with abs(p90 - p10) < .15 excluded)')

neg_slope_low = -1
neg_slope_high = -.15
pos_slope_low = .15
pos_slope_high = 1

#pos_label = '90th - 10th > ' + str(pos_slope_low)
#neg_label = '90th - 10th < ' + str(neg_slope_high)

# flag to show or hide n labels (number of policy cases for each bar)
n_flag = True

#%%%
''' CREATE DATAFRAMES FOR PLOT '''

# read pickled dataframes 
neg_slope = slope_vs_p90_outcome_calculator(neg_slope_low, neg_slope_high)
pos_slope = slope_vs_p90_outcome_calculator(pos_slope_low, pos_slope_high)

# create copies of pos_slope and neg slope to create dataframes for:
# pass_rate, num cases (n) label, int n, and 95% confidence interval, ci
pos_slope_pass_rate = pos_slope.copy()
neg_slope_pass_rate = neg_slope.copy()
pos_slope_n = pos_slope.copy()
neg_slope_n = neg_slope.copy()
pos_slope_int_n = pos_slope.copy()
neg_slope_int_n = neg_slope.copy()
pos_slope_ci = pos_slope.copy() 
neg_slope_ci = pos_slope.copy()

# fill in pass rate, n, int_n, and ci dataframes with proper values
# note ci dataframe uses standard error function
# note that pos/neg_slope_n is for the 'n = x' bar labels, pos/neg_slope_int_n
# is for creating int n value for error bars
for j in range(4):
    pos_slope_pass_rate.iloc[0,j] = float(pos_slope_pass_rate.iloc[0,j].
                                          split(' ')[0])                                       
    neg_slope_pass_rate.iloc[0,j] = float(neg_slope_pass_rate.iloc[0,j].
                                          split(' ')[0])
                                         
    pos_slope_n.iloc[0,j] = pos_slope_n.iloc[0,j].split('  ')[1]
    neg_slope_n.iloc[0,j] = neg_slope_n.iloc[0,j].split('  ')[1]
 
    pos_slope_int_n.iloc[0,j] = int(pos_slope_n.iloc[0,j].split('=')[1])
    neg_slope_int_n.iloc[0,j] = int(neg_slope_n.iloc[0,j].split('=')[1])

    pos_slope_ci.iloc[0,j] = standard_error(pos_slope_pass_rate.iloc[0,j],
                                               pos_slope_int_n.iloc[0,j])                                             
    neg_slope_ci.iloc[0,j] = standard_error(neg_slope_pass_rate.iloc[0,j],
                                               neg_slope_int_n.iloc[0,j])
 
#%%
''' CREATE PLOT '''    
   
# title and labels
title = ('90th - 10th income percentile vs adoption rate \n All domains \n \
        (cases with abs(p90 - p10) < ' + str(abs(pos_slope_low)) + ' excluded)')
pos_label = '90th - 10th > ' + str(pos_slope_low)
neg_label = '90th - 10th < ' + str(neg_slope_high)
 
# ax1 bar heights and error bar values
ax1_bars1 = pos_slope_pass_rate.loc[0,:]
ax1_err1 = pos_slope_ci.iloc[0,:].tolist()
ax1_bars2 = neg_slope_pass_rate.loc[0,:]
ax1_err2 = neg_slope_ci.iloc[0,:].tolist()

# x position of all bars
r1 = np.arange(len(ax1_bars1))
r2 = [x + BAR_WIDTH for x in r1]

# create figure and subplots
fig = plt.figure()
ax1 = plt.subplot(111)
 
# ax1
ax1.bar(r1, ax1_bars1, width = BAR_WIDTH, color = COLOR_1, edgecolor = 'black', yerr=ax1_err1, capsize=6, label=pos_label)
ax1.bar(r2, ax1_bars2, width = BAR_WIDTH, color = COLOR_2, edgecolor = 'black', yerr=ax1_err2, capsize=6, label=neg_label)
ax1.set_xticks([])
ax1.set_ylim(0,Y_LIM)
ax1.yaxis.set_label_position("right")
ax1_pos_labels = pos_slope_n.loc[0] # add labels for num cases, n
ax1_neg_labels = neg_slope_n.loc[0]

# turn n labels on/off based on n_flag
if n_flag:
    for i in range(4):
        ax1.text(x = r1[i]-(WIDTH * BAR_WIDTH),y = ax1_bars1[i]+ HEIGHT, s = ax1_pos_labels[i], size = N_SIZE)
        ax1.text(x = r1[i]+(WIDTH * BAR_WIDTH),y = ax1_bars2[i]+ HEIGHT, s = ax1_neg_labels[i], size = N_SIZE)

ax1.legend(frameon=False, ncol=2, loc=2, prop={'size': 10})

# label only outer axes
for ax in fig.get_axes():
    ax.label_outer()

# add common labels
plt.xticks([r + 0.5 * BAR_WIDTH for r in range(len(ax1_bars1))], ['< -1 std', '-1 std', '1 std', '> 1 std'])
fig.text(0.5, .02, '90th income percentile preference', ha = 'center')
fig.text(0.05, 0.5, 'probability of adoption', va='center', rotation='vertical')
plt.suptitle(title)

plt.show()

# %%

