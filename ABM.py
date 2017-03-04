"""
Agent Based Model:
    Agent Class
    Market Simulation- outputs a series of financial returns
        
@author: nadeem
"""


import random
import pandas as pd
import numpy as np


class Agent(object):
    
    def __init__(self, lookback):
        self.lookback = lookback
        
        #generates a set of random strategies
        self.history = [self.strategy() for j in range(4)]
        
        #initialises each strategy with a score
        self.score = [[strat,0] for strat in self.history]
        
        
    #randomly generates a trading decision
    def random_trade(self):
        if random.random() < 0.5:
            return 1
        else:
            return 0
    
    #generates a random strategy
    def strategy(self):
        #generating all the possible combinations for a given number of days
        ls = [ [ int(c) for c in ('{0:0'+ str( self.lookback ) +'b}').format(num) ] for num in range(2**self.lookback) ]
        
        #assigns a random trade decision for each combination
        return {tuple(comb):self.random_trade() for comb in ls}
        




#number of agents should be odd

def simulation(memory_size, no_of_agents, interval_size):    
    #initializing a specific number of traders
    traders = [Agent(memory_size) for i in range(no_of_agents)]
    
    #The matrix which stores all the trade decisions for each trader at each time step
    market = np.zeros([len(traders), interval_size])
    
    #---------------------------------------------------------------------------------------------------------------#
    
    ##generating random trades for each trader for the first *memory_size* days    
    for day in range(memory_size):
        for agent in traders:
            market[traders.index(agent), day] = agent.random_trade()
    
    #finding minority trade for first *memory_size* days with random trade decisions
    minority = [1 if np.count_nonzero(market[:,day]) <= (len(traders)/2) else 0 for day in range(memory_size)]
    
    #---------------------------------------------------------------------------------------------------------------#

    #randomly selecting strategy to use for first decision    
    for agent in traders:
        first_strat = random.choice(agent.history)[ tuple(minority[:memory_size]) ]
        market[traders.index(agent), memory_size] = first_strat
        
    #updating minority after first decision
    if np.count_nonzero(market[:,memory_size]) <= (len(traders)/2):
        minority.append(1)
    else:
        minority.append(0)
    
    #---------------------------------------------------------------------------------------------------------------#
    
    #start day of non random simulation
    day = memory_size + 1
    while (day < interval_size):

        #looping through each agent
        for agent in traders:
            
            #================================#
                    #update scoring#
            #================================#
            for strat in agent.history:
                if strat[ tuple(minority[day-(memory_size + 1): day-1]) ] == minority[day - 1]:
                    for elem in agent.score:
                        if elem[0] == strat:
                            elem[1] += 1
                    
            #================================#        
                    #use best strategy#
            #================================#
            #sorts strategy by their score in descending order
            ranked = sorted(agent.score, key=lambda x:x[1], reverse=True)
            
            #selecting all the joint highest ranked
            best_strats = [r[0] for r in ranked if r[1] == ranked[0][1]]
            
            #================================#
        
    #looking back *memory_size* time steps of the minority list and choosing a random strategy from the set of best strategies
            trade_strat = random.choice(best_strats)[ tuple(minority[day-memory_size: day]) ]

            #implementing each traders decision by adding to table
            market[traders.index(agent), day] = trade_strat
            
        #finding minorty for the timestep
        if np.count_nonzero(market[:,day]) <= (len(traders)/2):
            minority.append(1)
        else:
            minority.append(0)
        
        #incrementing the day
        day += 1
            
    '''Change all 0 values to -1 in the market matrix and then sum all the columns to get attendance values.
        Then divide attendance values by a lambda value representing liquidity in the market, to get a series of returns'''
    
    market[market == 0] = -1
    
    return np.sum(market, axis = 0) / 10**5
	
	
	
	
#running the simulation 100 times to get an idea of simulation output
def monte_carlo_simulation(memory_size, no_of_agents, interval_size):
        return [simulation(memory_size=memory_size, no_of_agents=no_of_agents, interval_size=interval_size) \
                 for i in range(100)]