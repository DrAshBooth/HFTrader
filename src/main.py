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
    import random
    
    TEST = False
    CHEAT = True    # For testing data logging of exceptionally good results (rare otherwise!)

    ##################################################
    ################## Actual Runs ###################
    ##################################################
    
    
    
    start_test = datetime.date(2011, 01, 01)
    end_test = datetime.date(2012, 01, 01)
    ticker = 'AAPL'
    
    data_handler = dc.DataContainer(['creamer','ash'])
    
    the_predictor = cm.Predictor(start_test, end_test, ticker, nef=5, max_experts=48, )
    days_that_trade = the_predictor.getTradingDates()
    
    creamer_ptflo = mpf.MyPortfolio(1000000)
    creamer_ptflo.add_stock(ticker)
    
    ash_ptflo = mpf.MyPortfolio(1000000)
    ash_ptflo.add_stock(ticker)
    p_val= 1000000
#    ###########TEST###########
#    random.seed(4)
#    crem = 0.0
#    crem_cum = [crem]
#    crem_ret = [0]
#    ash=0.0
#    ash_cum = [ash]
#    ash_ret=[0]
#    bah=0.0
#    bah_cum = [bah]
#    bah_ret=[0]
#    ##########################
    
    for count, the_date in enumerate(days_that_trade):
        
#        ###########TEST###########
#        base = random.gauss(0.06,0.35)*0.55
#        crem += base
#        crem_cum.append(crem)
#        crem_ret.append(base)
#        diff = random.gauss(0.004,0.05)
#        ash+= (base+diff)
#        ash_cum.append(ash)
#        ash_ret.append(diff)
#        base2 = random.gauss(-0.05,0.35)*0.55
#        bah+=base2
#        bah_cum.append(bah)
#        bah_ret.append(base2)
#        ##########################
        
        if count+3>len(days_that_trade): break
        tomo = days_that_trade[count+1]
        day_after = days_that_trade[count+2]
        pred, next_close, close_after = the_predictor.makePrediction(the_date, tomo, day_after, False)
        
        if pred!=0.0:
            pred=pred*-1
            pred, go_long, correct = data_handler.update_predictions_data(pred, next_close, close_after, CHEAT)
            ##### Trade #####
            # Creamer
            ret = (close_after-next_close)/next_close
            day_return = pred*(ret)-(pred-the_predictor.previeous_pred)*0.0002
            data_handler.update_car('creamer', the_date, day_return)
            
            # Me {AAPL : [num_shares, current_share_value] }
            if pred>0 and ash_ptflo.stocks[ticker][0]<0:
                size=-ash_ptflo.stocks[ticker][0]
            elif pred<0 and ash_ptflo.stocks[ticker][0]>0:
                size = -ash_ptflo.stocks[ticker][0]
            else:
                size = math.floor((ash_ptflo.cash*pred)/next_close)
            prev_val, curr_val = ash_ptflo.update_portfolio(-1*size*next_close, [['AAPL',size,next_close]]) #try close after
            day_return = (prev_val-curr_val)/prev_val
            data_handler.update_car('ash', the_date, day_return)
            
        
        else:
            data_handler.num_holds+=1

            # Creamer
            ret = (close_after-next_close)/next_close
            day_return = 0.0*(ret)-(0.0-the_predictor.previeous_pred)*0.0002
            data_handler.update_car('creamer', the_date, day_return)
            # ash
            prev_val, curr_val = ash_ptflo.update_portfolio(0, [['AAPL',0,next_close]]) #try close after
            day_return = (prev_val-curr_val)/prev_val
            data_handler.update_car('ash', the_date, day_return)
        
        data_handler.add_price_data(False, the_date, close_after)
        
    a, l, s = data_handler.percentage_correct()
    print "Correct predictions:\n\t- Short = {}\n\t- Long = {}\n\t- All = {}".format(s, l, a)
    
    the_dates = [x[0] for x in data_handler.cars['creamer']]
    crem_cars = [a[1] for a in data_handler.cars['creamer']]
    ash_cars = [a[1] for a in data_handler.cars['ash']]

    pylab.figure()
    pylab.subplot(121)
    pylab.plot_date(the_dates,crem_cars,'k-')
    pylab.subplot(122)
    pylab.plot_date(the_dates,ash_cars,'r-')
    pylab.show()
    
#    # sharps
#    bah_return = pylab.array(bah_ret)
#    bah_sharp =  bah_return.mean()/bah_return.std()
#    crem_return = pylab.array(crem_ret)
#    crem_sharp =  crem_return.mean()/crem_return.std()
#    ash_return = pylab.array(ash_ret)
#    ash_sharp =  ash_return.mean()/ash_return.std()
#    
#    print "Sharp Ratios:\nB&H\t{}\nSimple\t{}\nNew\t{}".format(abs(bah_sharp)*10,crem_sharp*10,ash_sharp*10)
#    
#    import matplotlib.cm as cm
#    pylab.figure()
#    pylab.plot_date(days_that_trade,bah_cum[:-1],'-',label="Buy and Hold",linewidth=1.5, color=cm.gray(2/3.,1))
#    pylab.plot_date(days_that_trade,crem_cum[:-1],'-',label="Simple Execution",linewidth=1.5, color=cm.gray(1.3/3.,1))
#    pylab.plot_date(days_that_trade,ash_cum[:-1],'-',label="Intelligent Execution",linewidth=1.5, color=cm.gray(0.6/3.,1))
#    pylab.legend(loc='upper left')
#    pylab.xlabel("Date", fontsize=18)
#    pylab.ylabel("Cumulative Abnormal Return (%)", fontsize=18)
#    pylab.show()
    
    

            
    
    
    
    
    