from parameters import *

class Predictor(object):
    def __init__(self):
        self.experts = []
        
    def writeSpecification(self):
        import os
        spec = open('{}/spec.spec'.format(os.getcwd()), 'w')
        spec.write('exampleTerminator=;\nattributeTerminator=,\nmaxBadExa=5\n')
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
        spec.write('FASTKn{}\t\tnumber\n'.format(FASTKn2))
        spec.write('FASTDn{}\t\tnumber\n'.format(FASTKn1))
        spec.write('FASTDn{}\t\tnumber\n'.format(FASTKn2))
        spec.write('FASTDn{}\t\tnumber\n'.format(FASTKn2))
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

    def createClassifier(self, filename):
        import os
        import rpy2
        from rpy2.robjects.numpy2ri import numpy2ri
        import rpy2.robjects as ro
        ro.conversion.py2ri = numpy2ri
        #rpy2.robjects.numpy2ri.activate()
        from rpy2.robjects import r
        
        # Run R script that does all statistics and creates an xts for complete date range
        r('source("{}/oneStockXTS.r")'.format(os.getcwd()))
        r('setwd("{}")'.format(os.getcwd()))
        
#        # DONT FORGET THE LAG!
#        startDatabase = STARTDATE - training_window - lag_date
#        endDatabase = ENDDATE
#        r.assign('remoteTICKER', ticker.split()[0])
#        r.assign('remoteSTART', startDatabase.strftime('%Y%m%d'))
#        r.assign('remoteEND', endDatabase.strftime('%Y%m%d'))
#        r('DB<-createDatabase(remoteTICKER,remoteSTART,remoteEND)')
#        
#        # Need to get a vector of datetimes of trading days
#        theUTCdates = r('index(DB)')
#        tradingDays = []  # to be populated with all of the dates that we wish to trade on
#        # iterate through r timestamps; once we hit the STARTDATE, start appending 
#        # datetime objects of the dates to the tradingDay list
#        for date in theUTCdates:
#            if date >= time.mktime(STARTDATE.timetuple()):
#                tradingDays.append(datetime.datetime.fromtimestamp(date))