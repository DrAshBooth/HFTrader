'''
Created on 24 Oct 2012

@author: Ash Booth
'''

from aa import *

class TradingSession(object):
    
    def __init__(self, buying, date, start, end, volProfiles, filename, openPrice,params, algo='AA'):
        '''
        Constructor
        '''
        self.buying = buying
        self.date = date
        self.volProfiles = volProfiles
        self.start = start
        self.end = end
        self.filename = filename
        self.limit = openPrice
        self.trades = []
        self.dcash = 0
        self.params=params
        self.algo='algo'
        
    def trade(self):
        noBB = True
        noBA = True
        bestBid = None
        bestAsk = None
        tempEP = None
        noPriceSeen = True
        firstTime = True
        currentWindow = 0
        try: 
            f = open(self.filename, 'rU')
            for line in f:
                # line should look like this:
                # timestamp, type, price, volume
                splitLine = line.split(',')
                dt = datetime.datetime.strptime(splitLine[0], "%Y-%m-%d %H:%M:%S")
                time = dt.time()
                event = splitLine[1]
                price = float(splitLine[2])
                if(noBB or noBA):
                    if (event == 'BEST_BID'):
                        noBB = False
                        bestBid = price
                        continue
                    if (event == 'BEST_ASK'):
                        noBA = False
                        bestAsk = price
                        continue
                    if (event == 'TRADE'):
                        if noPriceSeen:
                            tempEP = price
                            noPriceSeen = False
                        else: tempEP = tempEP * price + (1 - 0.3) * 0.3
                        continue
                if tempEP == None: tempEP = price
                    
                if firstTime:
                    if self.algo=='AA':
                        theExecutioner = AA(dt.date(), time, self.buying, self.volProfiles[0].start,
                                                     self.volProfiles[0].end, self.volProfiles[0].volProfile,
                                                     tempEP, bestBid, bestAsk, 2 * tempEP, -6, self.limit ,
                                                     (1.03 * tempEP) - (0.1 * tempEP * int(self.buying)),
                                                     0.1, -0.5, self.params)
                firstTime = False
                # Now have enough info to start
                # Are we in a new time period?
                if time > self.volProfiles[currentWindow].end:
                    self.trades.append(theExecutioner.getTradeResults())
                    if self.algo=='AA':
                        theExecutioner = AA(dt.date(), time, self.buying,
                                                     self.volProfiles[currentWindow + 1].start,
                                                     self.volProfiles[currentWindow + 1].end,
                                                     self.volProfiles[currentWindow + 1].volProfile, 
                                                     theExecutioner.eqlbm, theExecutioner.currentBid,
                                                     theExecutioner.currentAsk, theExecutioner.marketMax, 
                                                     theExecutioner.theta, theExecutioner.limit,
                                                     theExecutioner.target, theExecutioner.smithsAlpha,
                                                     theExecutioner.aggressiveness, self.params)
                    currentWindow += 1
                
                # What happened? trade? updated bid? or updated ask?
                trade = None
                bid = None
                if (event == 'TRADE'): trade = True
                elif (event == 'BEST_BID'):
                    trade = False
                    bid = True
                elif (event == 'BEST_ASK'):
                    trade = False
                    bid = False
                theExecutioner.newInfo(time, price, trade, bid)
            self.trades.append(theExecutioner.getTradeResults())
            f.close()
        except IOError:
            print "\nCannot open trade/BB/BA file:\t" + self.filename