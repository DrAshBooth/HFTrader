from parameters import *
from expert import *

class Predictor(object):
    def __init__(self, nef, max_experts=25, c=1):
        self.t=0
        self.c=c
        self.experts = []
        self.new_exp_freq = nef
        self.writeSpecification()
        
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

    def createClassifier(self, time, start_training, end_training, file_name, verbose):
        import os
        import rpy2
        from rpy2.robjects.numpy2ri import numpy2ri
        import rpy2.robjects as ro
        ro.conversion.py2ri = numpy2ri
        #rpy2.robjects.numpy2ri.activate()
        from rpy2.robjects import r
        import subprocess
        
        # Run R script that does all statistics and creates an xts for complete date range
        r('source("{}/oneStockXTS.r")'.format(os.getcwd()))
        r('setwd("{}")'.format(os.getcwd()))
        
        # DONT FORGET THE LAG!
        r.assign('remote_filename', file_name)
        r.assign('remoteSTART', start_training.strftime('%Y%m%d'))
        r.assign('remoteEND', end_training.strftime('%Y%m%d'))
        r('DB<-createDatabase(remote_filename,remoteSTART,remoteEND)')
        
        # write training file 
        # write test data file
        
        # Run bash script to invoke learner and generate classifier
        if verbose: print("Creating classifier using Jboost with runADTree.sh bash script..\n\n")
        command_line = '{}/runADTree.sh '.format(os.getcwd()) + os.getcwd() + ' ' + file_name
        process = subprocess.Popen([command_line], shell=True)
        retcode = process.wait()
        
        # import classifier from file made on the fly
        if verbose: print("Importing classifier...\n")
        test_file = file_name + '.test'
        spec_file = 'spec.spec'
        classifier_name = '{}predict'.format(file_name)
        m = __import__(classifier_name, globals(), locals(), ['ADTree'])
        
        # Add new expert to list of experts
        self.experts.append(Expert(getattr(m, 'ATree'), time, self.new_exp_freq, (not self.experts)))

        # To use a classifier, create an object as below
        # classifier = self.experts[x].module(test_file, spec_file) 

    def reweightExperts(self, time):
        for expert in self.experts:
            if expert.first:
                expert.weight = math.exp((self.c*expert.cummulative_return)/math.sqrt(float(time)))
            elif time-expert.born_at==0:
                weight_sum = 0
                for e in self.experts: weight_sum+= e.weight
                expert.initial_weight = weight_sum/float(len(self.experts))
                expert.weight=expert.initial_weight
            else:
                ramp = min((time-expert.born_at)/float(self.new_exp_freq))
                weight_factor = math.exp((self.c*expert.cummulative_return)/math.sqrt(float(time-expert.born_at)))
                expert.weight = expert.initial_weight*ramp*weight_factor
                
    def getExpertsPrediction(self, filename):
        long_sum = 0.0
        total_sum = 0.0
        test_file = filename + '.test'
        spec_file = 'spec.spec'
        for expert in self.experts:
            classifier = expert.module(test_file, spec_file)
            score = classifier.get_scores()[0][0]
            if score>0: long_sum+=expert.weight
            total_sum += expert.weight
        fraction_long = long_sum/float(total_sum)
        fraction_short = 1-fraction_long
        return fraction_long-fraction_short
                
    def makePrediction(self):
        self.t+=1
        # create classifier
        # reweight experts
        # risk management