'''
Created on Dec 10, 2012

@author: Ash Booth
'''

import random
import numpy

class DataContainer(object):
    '''
    Holds data about:
    - prediction accuracies
    - asset prices
    - transaction prices
    
    prices should be a tuple of price and date
    
    Currently only designed for a single asset
    
    '''


    def __init__(self,strats):
        self.num_short_predictions = 0
        self.num_long_predictions = 0
        self.num_predictions = 0
        self.num_holds = 0
        self.correct_predictions = 0
        self.correct_long_predictions = 0
        self.correct_short_predictions = 0
        
        self.open_prices = []
        self.close_prices = []
        self.open_trade_prices = {}
        self.close_trade_prices = {}
        self.balances = {}
        for strat in strats:
            self.open_trade_prices[strat] = []
            self.close_trade_prices[strat] = []
            self.balances[strat] = []
        
    def update_predictions_data(self, pred, the_open, the_close, cheat):
        going_long=False
        correct=False
        should_go_long = (the_close>the_open)
        self.num_predictions+=1
        if pred>0.0: 
            going_long=True
            self.num_long_predictions+=1
            if going_long==should_go_long:
                self.correct_predictions+=1
                self.correct_long_predictions+=1
                correct=True
            elif cheat and random.random()<0.2:
                going_long=should_go_long
                self.num_long_predictions-=1
                self.num_short_predictions+=1
                self.correct_short_predictions+=1
                self.correct_predictions+=1
                pred*=-1
                correct=True  
        else:
            self.num_short_predictions+=1
            if going_long==should_go_long:
                self.correct_short_predictions+=1
                self.correct_predictions+=1
                correct=True
            elif cheat and random.random()<0.2:
                going_long=should_go_long
                self.num_short_predictions-=1
                self.num_long_predictions+=1
                self.correct_predictions+=1
                self.correct_long_predictions+=1
                pred*=-1
                correct=True
        if going_long: going_long=1
        else: going_long=-1
        return pred, going_long, correct
        
    def add_price_data(self, the_open, the_date, price):
        if the_open: self.open_prices.append((the_date, price))
        else: self.close_prices.append((the_date, price))
        
    def add_trade_data(self, strat, the_date, at_open, buy, price, vol):
        if at_open: self.open_trade_prices[strat].append([the_date, buy, price, vol])
        else: self.close_trade_prices[strat].append([the_date, buy, price, vol])
        
    def add_balances_data(self,strat, the_date, balance):
        self.balances[strat].append([the_date,balance])
        
    def percentage_correct(self):
        all_preds = (self.correct_predictions/float(self.num_predictions))*100
        went_long = (self.correct_long_predictions/float(self.num_long_predictions))*100
        went_short = (self.correct_short_predictions/float(self.num_short_predictions))*100
        return all_preds, went_long, went_short
    
    def get_returns(self,strat):
        balances = [x[1] for x in self.balances[strat]]
        returns = [0]
        for i in range(1,len(balances)):
            returns.append( (balances[i]-balances[i-1])/float(balances[i-1]))
        return returns
    
    def get_annualised_return(self,strat):
        balances_with_dates = [x for x in self.balances[strat]]
        current_return = (balances_with_dates[-1][1]-balances_with_dates[0][1])/balances_with_dates[0][1]
        num_days = (balances_with_dates[-1][0]-balances_with_dates[0][0]).days
        annualised_return = (1+current_return)**(365.25/float(num_days))-1
        return annualised_return
    
    def get_sharp_ratio(self, strat):
        returns = numpy.array(self.get_returns(strat))
        return returns.mean()/returns.std()
    
        