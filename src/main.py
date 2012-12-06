'''
Created on Dec 3, 2012

@author: Ash Booth
'''

if __name__ == '__main__':
    # with current setup, must make prediction every day!!!!!
    
    import datetime
    import prediction.creamer as cm
    
    start_test = datetime.date(2011, 01, 01)
    end_test = datetime.date(2011, 02, 01)
    
    the_predictor = cm.Predictor(start_test, end_test, 'AAPL', nef=5, max_experts=48, )
    days_that_trade = the_predictor.getTradingDates()
    
    for the_date in days_that_trade:
        the_predictor.makePrediction(the_date, False)
        
    print [x.cummulativeReturn for x in the_predictor.experts]
    
    
    # DEBUG
    
    
    