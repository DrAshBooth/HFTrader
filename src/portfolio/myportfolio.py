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
        
        self.total_value = cash
        self.update_value()
        
    def add_stock(self,ticker):
        self.stocks[ticker] = [0,0]
        
    def update_portfolio(self, cash_change, new_stocks=[]):
        '''
        Takes a list of stock infos and updates the portfolio quantities and values.
        The list is in the form
        stocks = [ ['AAPL', num_traded, close_price], ['MSFT', num_traded, close_price]...]
        '''
        if new_stocks:
            for stk in new_stocks:
                self.stocks[stk[0]][0]+=stk[1]  # adjust stock quantity
                self.stocks[stk[0]][1]=stk[2]   # update stock price
        self.cash+=cash_change
        prev_val=self.total_value
        new_val = self.update_value()
        return prev_val, new_val
        
                
    def update_value(self):
        total_val = self.cash
        if self.stocks:
            for stk in self.stocks:
                total_val+=(self.stocks[stk][0]*self.stocks[stk][1])
        self.total_value = total_val
        new_val = self.total_value
        return new_val
        
##################################################
################# Example Usage ##################
##################################################

#my_ptflo = MyPortfolio(100)
#print my_ptflo.total_value
#my_ptflo.add_stock('AAPL')
#my_ptflo.update_portfolio(-80, [['AAPL',10,11.0]])
#print my_ptflo.total_value
#my_ptflo.update_portfolio(0, [['AAPL',0,12.0]])
#print my_ptflo.total_value