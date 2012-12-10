from parameters import *
from expert import *

import os
import rpy2
import subprocess
import datetime
import math
import time

from rpy2.robjects.numpy2ri import numpy2ri
import rpy2.robjects as ro
ro.conversion.py2ri = numpy2ri
#rpy2.robjects.numpy2ri.activate()
from rpy2.robjects import r

class Predictor(object):
    def __init__(self, start, end, ticker, nef=5, max_experts=48, c=1):
        self.date= start-datetime.timedelta(days=1)
        self.trading_days_seen=1
        self.start_trading_after=50
        self.c=c
        self.experts = []
        self.new_exp_freq = nef
        self.max_experts = max_experts
        self.start = start
        self.end = end
        self.training_periods = [50,100,150,200]
        self.lag = 100
        self.ticker = ticker
        self.threshold = 0.2
        self.__writeSpecification()
        self.__createRDB()
        
    def __createRDB(self):
        # Run R script that does all statistics and creates an xts for complete date range
        r('source("/Users/user/git/HFTrader/src/prediction/creamer/oneStockXTS.r")')
        r('setwd("/Users/user/git/HFTrader/src/prediction/creamer")')
        startDatabase = self.start - datetime.timedelta(days=(max(self.training_periods) + self.lag+20))
        endDatabase = self.end+datetime.timedelta(days=20)
        r.assign('remoteTICKER', self.ticker)
        r.assign('remoteSTART', startDatabase.strftime('%Y%m%d'))
        r.assign('remoteEND', endDatabase.strftime('%Y%m%d'))
        r('DB<-createDatabase(remoteTICKER,remoteSTART,remoteEND)')
        
    def __writeSpecification(self):
        spec = open('{}/prediction/creamer/spec.spec'.format(os.getcwd()), 'w')
        spec.write('exampleTerminator=;\nattributeTerminator=,\nmaxBadExa=5\n')
        spec.write('Open\t\t\tnumber\n')
        spec.write('EMAn{}\t\t\tnumber\n'.format(EMAn1))
        spec.write('EMAn{}\t\t\tnumber\n'.format(EMAn2))
        spec.write('EMAn{}\t\t\tnumber\n'.format(EMAn3))
        spec.write('SMAn{}\t\t\tnumber\n'.format(SMAn1))
        spec.write('SMAn{}\t\t\tnumber\n'.format(SMAn2))
        spec.write('SMAn{}\t\t\tnumber\n'.format(SMAn3))
        spec.write('BOL_LOWn{}\t\tnumber\n'.format(BOLn1))
        spec.write('BOL_HGHn{}\t\tnumber\n'.format(BOLn1))
        spec.write('BOL_LOWn{}\t\tnumber\n'.format(BOLn2))
        spec.write('BOL_HGHn{}\t\tnumber\n'.format(BOLn2))
        spec.write('BOL_LOWn{}\t\tnumber\n'.format(BOLn3))
        spec.write('BOL_HGHn{}\t\tnumber\n'.format(BOLn3))
        spec.write('MOMn{}\t\t\tnumber\n'.format(MOMn1))
        spec.write('MOMn{}\t\t\tnumber\n'.format(MOMn2))
        spec.write('MOMn{}\t\t\tnumber\n'.format(MOMn3))
        spec.write('ACCn{}\t\t\tnumber\n'.format(MOMn1))
        spec.write('ACCn{}\t\t\tnumber\n'.format(MOMn2))
        spec.write('ACCn{}\t\t\tnumber\n'.format(MOMn3))
        spec.write('ROCn{}\t\t\tnumber\n'.format(ROCn1))
        spec.write('ROCn{}\t\t\tnumber\n'.format(ROCn2))
        spec.write('ROCn{}\t\t\tnumber\n'.format(ROCn3))
        spec.write('MACDf{}\t\tnumber\n'.format(MACDf1))
        spec.write('MACDf{}\t\tnumber\n'.format(MACDf2))
        spec.write('MACDf{}\t\tnumber\n'.format(MACDf3))
        spec.write('MACDSIGf{}\t\tnumber\n'.format(MACDf1))
        spec.write('MACDSIGf{}\t\tnumber\n'.format(MACDf2))
        spec.write('MACDSIGf{}\t\tnumber\n'.format(MACDf3))
        spec.write('RSIn{}\t\t\tnumber\n'.format(RSIn1))
        spec.write('RSIn{}\t\t\tnumber\n'.format(RSIn2))
        spec.write('RSIn{}\t\t\tnumber\n'.format(RSIn3))
        spec.write('FASTKn{}\t\tnumber\n'.format(FASTKn1))
        spec.write('FASTKn{}\t\tnumber\n'.format(FASTKn2))
        spec.write('FASTKn{}\t\tnumber\n'.format(FASTKn3))
        spec.write('FASTDn{}\t\tnumber\n'.format(FASTKn1))
        spec.write('FASTDn{}\t\tnumber\n'.format(FASTKn2))
        spec.write('FASTDn{}\t\tnumber\n'.format(FASTKn3))
        spec.write('SLOWKn{}\t\tnumber\n'.format(FASTKn1))
        spec.write('SLOWKn{}\t\tnumber\n'.format(FASTKn2))
        spec.write('SLOWKn{}\t\tnumber\n'.format(FASTKn3))
        spec.write('SLOWDn{}\t\tnumber\n'.format(FASTKn1))
        spec.write('SLOWDn{}\t\tnumber\n'.format(FASTKn2))
        spec.write('SLOWDn{}\t\tnumber\n'.format(FASTKn3))
        spec.write('WILL\t\tnumber\n')
        spec.write('MFI\t\tnumber\n')
        spec.write('CHVn{}\t\t\tnumber\n'.format(CHVn))
        spec.write('GKV\t\tnumber\n')
        spec.write('ADL\t\t\t\tnumber\n')
        spec.write('OBV\t\t\t\tnumber\n')
        spec.write('CHOs{s},f{f}\t\tnumber\n'.format(s=CHOs, f=CHOf))
        spec.write('PVI\t\tnumber\n')
        spec.write('NVI\t\tnumber\n')
        spec.write('ema2close\t\tnumber\n')
        spec.write('close2bbh1\t\tnumber\n')
        spec.write('close2bbh2\t\tnumber\n')
        spec.write('close2bbh3\t\tnumber\n')
        spec.write('close2bbl1\t\tnumber\n')
        spec.write('close2bbl2\t\tnumber\n')
        spec.write('close2bbl3\t\tnumber\n')
        spec.write('emamom1\t\tnumber\n')
        spec.write('emamom2\t\tnumber\n')
        spec.write('emamom3\t\tnumber\n')
        spec.write('mom2emamom1\t\tnumber\n')
        spec.write('mom2emamom2\t\tnumber\n')
        spec.write('mom2emamom3\t\tnumber\n')
        spec.write('macd2macds1\t\tnumber\n')
        spec.write('macd2macds2\t\tnumber\n')
        spec.write('macd2macds3\t\tnumber\n')
        spec.write('slowk2slowd1\t\tnumber\n')
        spec.write('slowk2slowd2\t\tnumber\n')
        spec.write('slowk2slowd3\t\tnumber\n')
        spec.write('fastk2fastd1\t\tnumber\n')
        spec.write('fastk2fastd2\t\tnumber\n')
        spec.write('fastk2fastd3\t\tnumber\n')
        spec.write('pvi2smapvi\t\tnumber\n')
        spec.write('nvi2smanvi\t\tnumber\n')
        spec.write('bolTR1\t\t(buy, sell, hold)\n')
        spec.write('bolTR2\t\t(buy, sell, hold)\n')
        spec.write('bolTR3\t\t(buy, sell, hold)\n')
        spec.write('momTR1\t\t(buy, sell, hold)\n')
        spec.write('momTR2\t\t(buy, sell, hold)\n')
        spec.write('momTR3\t\t(buy, sell, hold)\n')
        spec.write('accTR1\t\t(buy, sell, hold)\n')
        spec.write('accTR2\t\t(buy, sell, hold)\n')
        spec.write('accTR3\t\t(buy, sell, hold)\n')
        spec.write('rocTR1\t\t(buy, sell, hold)\n')
        spec.write('rocTR2\t\t(buy, sell, hold)\n')
        spec.write('rocTR3\t\t(buy, sell, hold)\n')
        spec.write('macdTR1\t\t(buy, sell, hold)\n')
        spec.write('macdTR2\t\t(buy, sell, hold)\n')
        spec.write('macdTR3\t\t(buy, sell, hold)\n')
        spec.write('rsiTR1\t\t(buy, sell, hold)\n')
        spec.write('rsiTR2\t\t(buy, sell, hold)\n')
        spec.write('rsiTR3\t\t(buy, sell, hold)\n')
        spec.write('fastTR1\t\t(buy, sell, hold)\n')
        spec.write('fastTR2\t\t(buy, sell, hold)\n')
        spec.write('fastTR3\t\t(buy, sell, hold)\n')
        spec.write('slowTR1\t\t(buy, sell, hold)\n')
        spec.write('slowTR2\t\t(buy, sell, hold)\n')
        spec.write('slowTR3\t\t(buy, sell, hold)\n')
        spec.write('willTR\t\t(buy, sell, hold)\n')
        spec.write('mfiTR\t\t(buy, sell, hold)\n')
        spec.write('pviTR\t\t(buy, sell, hold)\n')
        spec.write('nviTR\t\t(buy, sell, hold)\n')
        spec.write('labels\t\t\t(-1,1)')

        spec.close()

    def getTradingDates(self):
        the_UTC_dates = r('index(DB)')
        trading_dates = []  # to be populated with all of the dates that we wish to trade on
        # iterate through r time-stamps; once we hit the STARTDATE, start appending 
        # datetime objects of the dates to the tradingDay list
        for date in the_UTC_dates:
            if date >= time.mktime(self.start.timetuple()):
                trading_dates.append(datetime.datetime.fromtimestamp(date))
        return trading_dates

    def createClassifiers(self, verbose):
        test_date=self.date
        for window in self.training_periods:
            training_start = test_date - datetime.timedelta(days = int(1.7*window))
            day_before = test_date - datetime.timedelta(days=1)
            filename = training_start.strftime('%Y%m%d') + test_date.strftime('%Y%m%d') + self.ticker
            
            # Generate features:
            # (make CSV from the R database [mustn't forget to drop the close column]) 
            if verbose:
                print('Generating feature csvs from R xts..\n')
                print('Current window = {}\n\n'.format(filename))
            r.assign('windowStart', training_start.strftime('%Y-%m-%d'))
            r.assign('windowEnd', day_before.strftime('%Y-%m-%d'))
            r.assign('testDate', test_date.strftime('%Y-%m-%d'))
            r('windowDB<-DB[paste(windowStart,windowEnd,sep="/")]')
            r('windowDB<-subset(windowDB, select = -c(close,ticker) )')
            r('testDB<-DB[testDate]')
            r('testDB<-subset(testDB, select = -c(close,ticker) )')
            r.assign('remoteFilename', filename)
            r('write.table(windowDB, file=paste(remoteFilename, "train", sep="."),quote=FALSE,sep=",",eol=";\n",row.names=FALSE,col.names=FALSE)')
            r('write.table(testDB, file=paste(remoteFilename, "test", sep="."),quote=FALSE,sep=",",eol=";\n",row.names=FALSE,col.names=FALSE)')
        
            # Run bash script to invoke learner and generate classifier
            if verbose: print("Creating classifier using Jboost with runADTree.sh bash script..\n\n")
            command_line = '{}/runADTree.sh '.format(os.getcwd()) + os.getcwd() + ' ' + filename
            process = subprocess.Popen([command_line], shell=True)
            retcode = process.wait()
            
            # import classifier from file made on the fly
            if verbose: print("Importing classifier...\n")
            test_file = filename + '.test'
            spec_file = 'spec.spec'
            classifier_name = '{}predict'.format(filename)
            m = __import__(classifier_name, globals(), locals(), ['ADTree'])
            
            # Add new expert to list of experts
            self.experts.append(Expert(getattr(m, 'ATree'), self.trading_days_seen, self.new_exp_freq, (len(self.experts)<=len(self.training_periods))))
            # remove oldest expert
            if len(self.experts)>=self.max_experts: self.experts.pop(0)
            
            # delete all files generated above
            os.remove(filename + '.info')
            os.remove(filename + '.log')
            os.remove(filename + '.output.tree')
            os.remove(filename + '.train')
            os.remove(filename + '.test')
            os.remove(filename + '.test.boosting.info')
            os.remove(filename + '.train.boosting.info')
            os.remove(filename + 'predict.py')
            os.remove(filename + 'predict.pyc')

    def reweightExperts(self):
        the_time = self.trading_days_seen
        for i, expert in enumerate(self.experts):
            if expert.first:
                expert.weight = math.exp((self.c*expert.cummulative_return)/math.sqrt(the_time))
            elif the_time-expert.born_at==0:
                weight_sum = 0
                for e in range(i): 
                    weight_sum+= self.experts[e].weight
                expert.initial_weight = weight_sum/float(len(self.experts[:i]))
                expert.weight=expert.initial_weight
            else:
                ramp = min((the_time-expert.born_at)/float(self.new_exp_freq),1.0)
                weight_factor = math.exp((self.c*expert.cummulative_return)/math.sqrt(float(the_time-expert.born_at)))
                expert.weight = expert.initial_weight*ramp*weight_factor
                
    def getExpertsPrediction(self, verbose):
        long_sum = 0.0
        total_sum = 0.0
        test_file = 'experts.test'
        spec_file = 'spec.spec'
        
        # Create "test set" from r DB
        if verbose: print "Generating test-set file... \n"
        test_date=self.date
        r.assign('testDate', test_date.strftime('%Y-%m-%d'))
        r('testDB<-DB[testDate]')
        the_open = float(r('testDB$open')[0])
        the_close = float(r('testDB$close')[0])
        r('testDB<-subset(testDB, select = -c(close,ticker) )')
        r.assign('remoteFilename', test_file)
        r('write.table(testDB, file=remoteFilename,quote=FALSE,sep=",",eol=";\n",row.names=FALSE,col.names=FALSE)')
        for expert in self.experts:
            classifier = expert.module(test_file, spec_file)
            score = classifier.get_scores()[0][0]
            expert.prediction = score
            if score>0: long_sum+=expert.weight
            total_sum += expert.weight
        fraction_long = long_sum/float(total_sum)
        fraction_short = 1-fraction_long
        # Delete test file
        os.remove(test_file)
        # next close
        tomorrow = test_date+datetime.timedelta(days=1)
        r.assign('remoteTomorrow',tomorrow)
        next_close = float(r('DB[remoteTomorrow]$close')[0])
        return fraction_long-fraction_short, the_open, the_close, next_close
    
    def riskManagement(self,prediction):
        if abs(prediction)<self.threshold: return None
        else: return prediction
    
    def reviewExperts(self, the_close, next_close):
        # need to work out return for all experts and add to cumulative return
        abs_return = (next_close-the_close)/float(the_close)
        if (next_close-the_close)>0.0: go_long=True
        else: go_long=False
        for exp in self.experts:
            if go_long:
                if exp.prediction>0.0: exp.cummulative_return+=abs_return
                else: exp.cummulative_return-=abs_return
            else:
                if exp.prediction<0.0: exp.cummulative_return+=abs_return
                else: exp.cummulative_return-=abs_return
                
    def makePrediction(self,date,verbose):
        self.date=date
        if self.trading_days_seen%self.new_exp_freq==1:
            self.createClassifiers(verbose)
        self.reweightExperts()
        prediction, the_open, the_close, next_close = self.getExpertsPrediction(verbose)
        prediction = self.riskManagement(prediction)
        self.reviewExperts(the_close, next_close)
        self.trading_days_seen+=1
        return prediction, the_open, the_close
        