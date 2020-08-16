
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 13:16:15 2019

@author: shawnmcguire
"""
#%%

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
 
Y_LIM = 1
COLOR_1 = 'green'
COLOR_2 = 'yellow'
h = 0.05
w = 0.6
n_size = 8
barWidth = 0.2

#%%%
''' user entries '''

title = '90th - 10th income percentile vs adoption rate \n ECYN domain only'
df_pos_slope = './df_pos_slope_vs_adoption_ECYN.pkl'
df_neg_slope = './df_neg_slope_vs_adoption_ECYN.pkl'
pos_label = '90th - 10th > 0'
neg_label = '90th - 10th < 0'

#%%%

pos_slope = pd.read_pickle(df_pos_slope)
neg_slope = pd.read_pickle(df_neg_slope)

# create copies of pos_slope and neg slope for pass_rate and number of cases, n, dataframes
pos_slope_pass_rate = pos_slope.copy()
pos_slope_n = pos_slope.copy()
neg_slope_pass_rate = neg_slope.copy()
neg_slope_n = neg_slope.copy()

# parse pos_slope dataframe to fill in separate dataframes for pass rate and number of cases
for i in range(4):
    for j in range(4):
        pos_slope_pass_rate.iloc[i,j] = float(pos_slope_pass_rate.iloc[i,j].split(' ')[0])
        pos_slope_n.iloc[i,j] = pos_slope_n.iloc[i,j].split('  ')[1]
        neg_slope_pass_rate.iloc[i,j] = float(neg_slope_pass_rate.iloc[i,j].split(' ')[0])
        neg_slope_n.iloc[i,j] = neg_slope_n.iloc[i,j].split('  ')[1]

# ax1 to 4 bar heights
ax1_bars1 = pos_slope_pass_rate.loc['> 1 std',:]
ax1_bars2 = neg_slope_pass_rate.loc['> 1 std',:]

ax2_bars1 = pos_slope_pass_rate.loc['mean to 1 std',:]
ax2_bars2 = neg_slope_pass_rate.loc['mean to 1 std',:]

ax3_bars1 = pos_slope_pass_rate.loc['mean to -1 std',:]
ax3_bars2 = neg_slope_pass_rate.loc['mean to -1 std',:]

ax4_bars1 = pos_slope_pass_rate.loc['< -1 std',:]
ax4_bars2 = neg_slope_pass_rate.loc['< -1 std',:]

# x position of all bars
r1 = np.arange(len(ax1_bars1))
r2 = [x + barWidth for x in r1]

# create figure and subplots
fig = plt.figure()
ax1 = plt.subplot(411)
ax2 = plt.subplot(412)
ax3 = plt.subplot(413)
ax4 = plt.subplot(414)
 
# ax1
ax1.bar(r1, ax1_bars1, width = barWidth, color = COLOR_1, edgecolor = 'black', capsize=7, label=pos_label)
ax1.bar(r2, ax1_bars2, width = barWidth, color = COLOR_2, edgecolor = 'black', capsize=7, label=neg_label)
ax1.set_xticks([])
ax1.set_ylim(0,Y_LIM)
ax1.yaxis.set_label_position("right")
ax1.set_ylabel('net int \ngrp align \n> 1 std', rotation=0, fontsize=10, labelpad=5, ha = 'left')
ax1_pos_labels = pos_slope_n.loc['> 1 std'] # add labels for num cases, n
ax1_neg_labels = neg_slope_n.loc['> 1 std']
for i in range(4):
    ax1.text(x = r1[i]-(w*barWidth),y = ax1_bars1[i]+ h, s = ax1_pos_labels[i], size = n_size)
    ax1.text(x = r1[i]+(w*barWidth),y = ax1_bars2[i]+ h, s = ax1_neg_labels[i], size = n_size)
ax1.legend(frameon=False, ncol=2, loc=2, prop={'size': 8})

#ax2
ax2.bar(r1, ax2_bars1, width = barWidth, color = COLOR_1, edgecolor = 'black', capsize=7, label='pos slope')
ax2.bar(r2, ax2_bars2, width = barWidth, color = COLOR_2, edgecolor = 'black', capsize=7, label='neg slope')
ax2.set_xticks([])
ax2.set_ylim(0,Y_LIM)
ax2.yaxis.set_label_position("right")
ax2.set_ylabel('net int \ngrp align \nmean to 1 std', rotation=0, fontsize=10, labelpad=5, ha = 'left')
ax2_pos_labels = pos_slope_n.loc['mean to 1 std'] # add labels for num cases, n
ax2_neg_labels = neg_slope_n.loc['mean to 1 std']
for i in range(4):
    ax2.text(x = r1[i]-(w*barWidth),y = ax2_bars1[i]+ h, s = ax2_pos_labels[i], size = n_size)
    ax2.text(x = r1[i]+(w*barWidth),y = ax2_bars2[i]+ h, s = ax2_neg_labels[i], size = n_size)

#ax3
ax3.bar(r1, ax3_bars1, width = barWidth, color = COLOR_1, edgecolor = 'black', capsize=7, label='pos slope')
ax3.bar(r2, ax3_bars2, width = barWidth, color = COLOR_2, edgecolor = 'black', capsize=7, label='neg slope')
ax3.set_xticks([])
ax3.set_ylim(0,Y_LIM)
ax3.yaxis.set_label_position("right")
ax3.set_ylabel('net int \ngrp align \nmean to -1 std', rotation=0, fontsize=10, labelpad=5, ha = 'left')
ax3_pos_labels = pos_slope_n.loc['mean to -1 std'] # add labels for num cases, n
ax3_neg_labels = neg_slope_n.loc['mean to -1 std']
for i in range(4):
    ax3.text(x = r1[i]-(w*barWidth),y = ax3_bars1[i]+ h, s = ax3_pos_labels[i], size = n_size)
    ax3.text(x = r1[i]+(w*barWidth),y = ax3_bars2[i]+ h, s = ax3_neg_labels[i], size = n_size)

#ax4
ax4.bar(r1, ax4_bars1, width = barWidth, color = COLOR_1, edgecolor = 'black', capsize=7, label='pos slope')
ax4.bar(r2, ax4_bars2, width = barWidth, color = COLOR_2, edgecolor = 'black', capsize=7, label='neg slope')
ax4.set_ylim(0,Y_LIM)
ax4.yaxis.set_label_position("right")
ax4.set_ylabel('net int \ngrp align \n< -1 std', rotation=0, fontsize=10, labelpad=5, ha = 'left')
ax4_pos_labels = pos_slope_n.loc['< -1 std'] # add labels for num cases, n
ax4_neg_labels = neg_slope_n.loc['< -1 std']
for i in range(4):
    ax4.text(x = r1[i]-(w*barWidth),y = ax4_bars1[i]+ h, s = ax4_pos_labels[i], size = n_size)
    ax4.text(x = r1[i]+(w*barWidth),y = ax4_bars2[i]+ h, s = ax4_neg_labels[i], size = n_size)

# label only outer axes
for ax in fig.get_axes():
    ax.label_outer()

# add common labels
plt.xticks([r + 0.5 * barWidth for r in range(len(ax1_bars1))], ['< -1 std', 'mean to -1 std', 'mean to 1 std', '> 1 std'])
fig.text(0.5, .02, '90th income percentile preference', ha = 'center')
fig.text(0.05, 0.5, 'probability of adoption', va='center', rotation='vertical')
plt.suptitle(title)

plt.show()

# %%