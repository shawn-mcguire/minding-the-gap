#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 13:28:16 2019

standard error calculator
    
calculates standard error from p and n

@author: shawnmcguire
"""

#%%
def standard_error(p,n):
    import numpy as np
    SE = np.sqrt(p*(1-p)/n)
    return SE
    
#%%