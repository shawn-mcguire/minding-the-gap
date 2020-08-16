#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 14:47:18 2019

this code creates a matrix, pass_matrix, for a pos or neg opinion slope pass rate 
with p90 and net interest group alignment on xy axes
instructions:
    1. select slope of data to be used
    2. select p90 and netiga bounds in user entries
    3. run
    4. use the created pass_matrix in slope_vs_adoption_plotter.py

note:  the matrix is filled in left to right, top to bottom.  that is why p90 bounds
start out low and netiga bounds start out high
@author: shawnmcguire
"""
#%%
import pandas as pd
import numpy as np


data = pd.read_csv('./gilens_data_sm_copy.csv')
data = data.iloc[0:1836]

# calculate mean and std of netiga values and p90 values
p90_mean = data.pred90_sw.mean()
p90_std = data.pred90_sw.std()
netiga_mean = data.IntGrpNetAlign.mean()
netiga_std = data.IntGrpNetAlign.std()

#%%
''' USER ENTRIES '''

# select desired slope (p90 - p10) of data to be used
slope_low = 0
slope_high = 1

# set low and high values to increment netiga and p90 in loop
#p90_low = p90_mean -(2*p90_std)
p90_low = 0  # set to 0 to include everything less than 1 std below mean
p90_high = p90_mean - p90_std
netiga_low = netiga_mean + netiga_std
#netiga_high = netiga_mean + (2*netiga_std)
netiga_high = 100 # set to 100 to include everything greater than 1 std above mean

# flag to filter only ECYN domain data
ecyn_flag = True
#%%
# counter for number of cases
num_cases_total = 0

# select desired slope (p90 - p10) of data to be used
data = data[(data['pred90 - pred10'] > slope_low) & 
            (data['pred90 - pred10'] < slope_high)]

# select ECYN data only
if ecyn_flag:
    data = data[data.ECYN == 1]

# create dataframe for pass rate matrix
pass_matrix = pd.DataFrame(columns = ['< -1 std','-1 std to mean', 'mean to 1 std', '> 1 std'], 
                           index = ['> 1 std','mean to 1 std', 'mean to -1 std', '< -1 std'])

# for all columns, p
for p in range(4):
    # fill in all rows, n 
    for n in range(4):
        # select subset of data based on netiga and p90
        data_subset = data[
                           (data['IntGrpNetAlign'] > netiga_low) &
                           (data['IntGrpNetAlign'] <= netiga_high) &
                           (data['pred90_sw'] > p90_low) &
                           (data['pred90_sw'] <= p90_high)
                          ]
        # divide subset into cases that passed (data_p) or not (data_np)
        data_p = data_subset[data_subset['Binary Outcome'] == 1]
        data_np = data_subset[data_subset['Binary Outcome'] == 0]
        
        # count number of cases 
        num_cases = len(data_subset)
        num_pass = len(data_p)
        num_no_pass = len(data_np)
        num_cases_total = num_cases_total + num_cases 
        
        # calculate pass rate
        if num_cases > 0:    
            pass_rate = str(round(num_pass / num_cases, 2)) # if num_cases else 0
            pass_rate = pass_rate + '  n=' + str(num_cases) # add num cases, n, if desired
        else:
            pass_rate = 0
        
        # fill pass_matrix w current pass rate
        pass_matrix.iloc[n,p] = pass_rate 
        
        # reset netiga_low and netiga_high to fill in next cell down in current column
        netiga_high = netiga_low
        netiga_low = netiga_low - netiga_std
        # on final row, reset netiga_low to include all less than 1 std below mean
        if n == 2:
            netiga_low = -100
        
    # reset netiga and p90 to fill next column, p + 1
    netiga_low = netiga_mean + netiga_std
    netiga_high = 100
    
    p90_low = p90_high
    p90_high = p90_high + p90_std
    
    # on final column, set p90_high to 100 to include everything above 1 std above mean
    if p == 2:
        p90_high = 100 
    
    

