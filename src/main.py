'''
Created on Dec 3, 2012

@author: Ash Booth
'''

if __name__ == '__main__':
    # with current setup, must make prediction every day!!!!!
    
    import datetime
    import prediction.creamer as cm
    import portfolio.myportfolio as mpf
    import datacontainer as dc
    import math
    import pylab
    
    TEST = False
    CHEAT = True    # For testing data logging of exceptionally good results (rare otherwise!)

    ##################################################
    ################## Actual Runs ###################
    ##################################################
    
    start_test = datetime.date(2011, 01, 01)
    end_test = datetime.date(2011, 02, 01)
    ticker = 'AAPL'
    
    data_handler = dc.DataContainer(['creamer','ash'])
    
    the_predictor = cm.Predictor(start_test, end_test, ticker, nef=5, max_experts=48, )
    days_that_trade = the_predictor.getTradingDates()
    
    creamer_ptflo = mpf.MyPortfolio(1000000)
    creamer_ptflo.add_stock(ticker)
    data_handler.add_balances_data('creamer', (days_that_trade[0]-datetime.timedelta(days=1)), 1000000)
    
    ash_ptflo = mpf.MyPortfolio(1000000)
    
    for the_date in days_that_trade:
        pred, the_open, the_close = the_predictor.makePrediction(the_date, False)
        if pred:
            pred, go_long, correct = data_handler.update_predictions_data(pred, the_open, the_close, CHEAT)
            data_handler.add_price_data(True, the_date, the_open)
            data_handler.add_price_data(False, the_date, the_close)
            
            # Creamer - trades at open and close
            amt_inv = 0.2*creamer_ptflo.cash
            vol_to_trade =  math.floor(amt_inv/the_open)
            amt_inv = vol_to_trade*the_open
            creamer_ptflo.cash-=amt_inv

            data_handler.add_trade_data('creamer', the_date, True, pred>0, the_open, vol_to_trade)
            data_handler.add_trade_data('creamer', the_date, False, pred<0, the_close, vol_to_trade)
            
            # update assets in portfolio (not really necess with creamer)
            asset_return = (the_close-the_open)/the_open
            creamer_ptflo.cash+= amt_inv*(1+go_long*asset_return)
            data_handler.add_balances_data('creamer', the_date, creamer_ptflo.cash)

        else:
            data_handler.num_holds+=1
    
    a, l, s = data_handler.percentage_correct()
    print "Correct predictions:\n\t- Short = {}\n\t- Long = {}\n\t- All = {}".format(s, l, a)
    
    the_dates = [x[0] for x in data_handler.balances['creamer']]
    the_balances = [x[1] for x in data_handler.balances['creamer']]

    print "Annualised return = {}\n".format(data_handler.get_annualised_return('creamer'))
    print "Sharp ratio = {}".format(data_handler.get_sharp_ratio('creamer'))

    pylab.figure()
    pylab.subplot(121)
    pylab.plot_date(the_dates, the_balances, '-k')
    pylab.subplot(122)
    pylab.plot_date(the_dates, data_handler.get_returns('creamer'),'k-')
    pylab.show()
    
    

            
    
    
    
    
    