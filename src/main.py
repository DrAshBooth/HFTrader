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
    
    ash_ptflo = mpf.MyPortfolio(1000000)
    
    for the_date in days_that_trade:
        pred, the_close = the_predictor.makePrediction(the_date, False)
        
        if pred:
            ##### Trade #####
            # Creamer
            ret = (the_close-data_handler.close_prices[-1][1])/data_handler.close_prices[-1][1]
            day_return = pred*(ret)-(pred-the_predictor.prediction)*0.0002
            data_handler.update_car('creamer', the_date, day_return)
            
            # Me
            # Trade previous day...
            # if short stock:
                # size = short postition
            # else size = pred*cash
        
        else:
            # No trading, just wait until close and update value of assets that we're holding
            yday_val, today_val = creamer_ptflo.update_portfolio(0, [['AAPL',0,the_close]])
            day_return = (today_val-yday_val)/yday_val
            data_handler.update_car('creamer', the_date, day_return)
        
        data_handler.add_price_data(False, the_date, the_close)
        
#
#        pred, the_close, next_close = the_predictor.makePrediction(the_date, False)
#        if pred:
#            pred, go_long, correct = data_handler.update_predictions_data(pred, the_close, next_close, CHEAT)
#            data_handler.add_price_data(False, the_date, the_close)
#            
#            # Work out Creamer's return
#            tomo_ret = (next_close-the_close)/the_close
#            creamer_return = pred*tomo_ret-((pred-the_predictor.previeous_pred)*0.002)
#            data_handler.update_car('creamer', the_date, creamer_return) # maybe tomorrows date?
#            
#            
##            amt_inv = 0.2*creamer_ptflo.cash
##            vol_to_trade =  math.floor(amt_inv/the_open)
##            amt_inv = vol_to_trade*the_open
##            creamer_ptflo.cash-=amt_inv
##
##            data_handler.add_trade_data('creamer', the_date, True, pred>0, the_open, vol_to_trade)
##            data_handler.add_trade_data('creamer', the_date, False, pred<0, the_close, vol_to_trade)
##            
##            # update assets in portfolio (not really necess with creamer)
##            asset_return = (the_close-the_open)/the_open
##            creamer_ptflo.cash+= amt_inv*(1+go_long*asset_return)
##            data_handler.add_balances_data('creamer', the_date, creamer_ptflo.cash)
#
#        else:
#            data_handler.num_holds+=1
#    
    a, l, s = data_handler.percentage_correct()
    print "Correct predictions:\n\t- Short = {}\n\t- Long = {}\n\t- All = {}".format(s, l, a)
    
    the_dates = [x[0] for x in data_handler.cars['creamer']]
    the_cars = [x[1] for x in data_handler.cars['creamer']]

    pylab.plot_date(the_dates,the_cars,'k-')
    pylab.show()

#    pylab.figure()
#    pylab.subplot(121)
#    pylab.plot_date(the_dates, the_cars, '-k')
#    pylab.subplot(122)
#    pylab.plot_date(the_dates, data_handler.get_returns('creamer'),'k-')
#    pylab.show()
    
    

            
    
    
    
    
    