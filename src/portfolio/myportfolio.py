'''
Created on Dec 10, 2012

@author: Ash Booth
'''

class MyPortfolio(object):
    '''
    Describes the current state of a portfolio including cash balance and various asset balances
    
    The dictionaries are intended to map a ticker to a list of attributes in the following form:
    
    {AAPL : [num_shares, current_share_value] }
    
    '''

    def __init__(self,cash):
        '''
        Constructor
        '''
        self.cash = cash
        self.stocks = {}
        self.furures = {}
        self.fx = {}
        self.bonds = {}
        self.options = {}
        self.complex = {}
        
    def add_stock(self,ticker):
        self.stocks[ticker] = [0,0]
        