"""
Stock analysis functions for real stock data, and for simulated stock data
    jarque bera test
    Auto Correlation functions
     
@author: nadeem
"""


import pandas as pd
import math
from scipy import stats
import numpy as np

class Real_stock_analysis(object):
    
    def __init__(self, location):
        table = pd.read_csv(location)
        self.matrix = table.as_matrix()[:,1:]
    
    def returns(self):
        total = []
        for col in range( int(self.matrix.shape[1]) ):
            ret = [( math.log( self.matrix[n+1,col] ) - math.log( self.matrix[n,col] ) ) for n in range(int(self.matrix.shape[0])-1 )]
            total.append(ret)
        return total
    
    def jarque_bera(self, ret, axis=0):
        resids = np.asarray(ret)
        
        # Calculate residual skewness and kurtosis
        skew = stats.skew(resids, axis=axis)
        kurtosis = 3 + stats.kurtosis(resids, axis=axis)

        # Calculate the Jarque-Bera test for normality
        n = len(resids)
        jb = (n/6.0)*( skew**2 + ( (kurtosis-3)**2/4.0 ) )
        
        return jb
    
    def jb_100(self):
        return map(self.jarque_bera, self.returns())
    
    def standard_autocorr_values(self, ret):
        auto_100 = []
        for stock in ret:
            autocorrs = np.correlate( stock, stock, mode = 'full' )
            auto_100.append( autocorrs[autocorrs.size/2] )
        return auto_100

    def abs_autocorr_values(self, ret):
        abs_auto_100 = []
        for stock in ret:
            abs_corrs = np.correlate( map(lambda x: abs(x),stock), map(lambda x: abs(x),stock), mode = 'full' )
            abs_auto_100.append( abs_corrs[abs_corrs.size/2] )
        return abs_auto_100
    
    def sqrd_autocorr_values(self, ret):
        sqrd_auto_100 = []
        for stock in ret:
            sqrd_corrs = np.correlate( map(lambda x: x**2,stock), map(lambda x: x**2,stock), mode = 'full' )
            sqrd_auto_100.append( sqrd_corrs[sqrd_corrs.size/2] )
        return sqrd_auto_100
        
        
#===============================================================================================================#
#===============================================================================================================#
        
        
class Sim_stock_analysis(object):
    
    def __init__(self, matrix):
        self.matrix = matrix
    
    def jarque_bera(self, ret, axis=0):
        resids = np.asarray(ret)
        
        # Calculate residual skewness and kurtosis
        skew = stats.skew(resids, axis=axis)
        kurtosis = 3 + stats.kurtosis(resids, axis=axis)

        # Calculate the Jarque-Bera test for normality
        n = len(resids)
        jb = (n/6.0)*( skew**2 + ( (kurtosis-3)**2/4.0 ) )
        
        return jb
    
    def jb_100(self):
        return map(self.jarque_bera, self.matrix)
    
    def standard_autocorr_values(self):
        auto_100 = []
        for stock in self.matrix:
            autocorrs = np.correlate( stock, stock, mode = 'full' )
            auto_100.append( autocorrs[autocorrs.size/2] )
        return auto_100

    def abs_autocorr_values(self):
        abs_auto_100 = []
        for stock in self.matrix:
            abs_corrs = np.correlate( map(lambda x: abs(x),stock), map(lambda x: abs(x),stock), mode = 'full' )
            abs_auto_100.append( abs_corrs[abs_corrs.size/2] )
        return abs_auto_100
    
    def sqrd_autocorr_values(self):
        sqrd_auto_100 = []
        for stock in self.matrix:
            sqrd_corrs = np.correlate( map(lambda x: x**2,stock), map(lambda x: x**2,stock), mode = 'full' )
            sqrd_auto_100.append( sqrd_corrs[sqrd_corrs.size/2] )
        return sqrd_auto_100