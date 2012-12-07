'''
Created on Dec 3, 2012

@author: Ash Booth
'''

if __name__ == '__main__':
    # with current setup, must make prediction every day!!!!!
    
    import datetime
    import prediction.creamer as cm
    import math
    
    start_test = datetime.date(2011, 01, 01)
    end_test = datetime.date(2012, 01, 01)
    
    the_predictor = cm.Predictor(start_test, end_test, 'AAPL', nef=5, max_experts=48, )
    days_that_trade = the_predictor.getTradingDates()
    
    predictions = []
    actuals = []
    for the_date in days_that_trade:
        pred, act = the_predictor.makePrediction(the_date, False)
        predictions.append(pred)
        actuals.append(act)
    
    correct = 0
    pred_sum=0
    total_preds = 0
    for i, pre in enumerate(predictions):
        if pre!=0.0:
            if pre>0.0: go_long=True
            else: go_long = False
            if go_long==actuals[i]: correct+=1
            total_preds+=1
    
        
    print "{}% correct predictions".format(int((correct/float(total_preds))*100))

    
    # DEBUG
    
    
    