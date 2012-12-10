'''
Created on 24 Oct 2012

@author: Ash Booth
''' 

import datetime 
import math

class Quote(object):
    def __init__(self, time, buying, price, vol):
        self.buying = buying
        self.price = price
        self.vol = vol
        self.born = time

class AA(object):
    '''
    classdocs
    '''
    def __init__(self, date, time, buying, start, end, volume, start_eqlbm, startBB, startBA, mmax,
                 theta, limit , target, smithsAlpha, agg, params):
        '''
        Constructor
        
        params[0] - alpha
        params[1] - maxQuoteLife
        params[2] - eta
        params[3] - theta max 
        params[4] - theta min
        params[5] - dAggRel
        params[6] - dAggAbs
        params[7] - learn rate Agg
        params[8] - learn rate theta
        params[9] - gamma
        params[10] - smiths alpha N
        params[11] = time adaptive parameter phi
        
        '''
        self.date = date
        self.time = time
        self.start = start
        self.end = end
        self.total_time_sec = (datetime.datetime.combine(self.date,self.end)-datetime.datetime.combine(self.date,self.start)).seconds
        
        self.buying = buying
        self.notTraded = True
        self.trade = []
        self.sleepTime = 20
        
        self.eqlbm = start_eqlbm
        self.eqlbm_alpha = params[0]
        self.marketMax = mmax
        
        self.currentBid = startBB
        self.currentAsk = startBA
        self.submittedTrade = False
        self.myquote = None
        
        self.maxQuoteLife = datetime.timedelta(seconds=params[1])
        self.eta = params[2]
        self.currentTradeSize = None
        
        self.volume = volume
        self.lastTrades = []
        self.nLastTrades = params[10]
        
        self.theta = theta
        self.thetaMax = params[3]
        self.thetaMin = params[4]
        self.limit = limit
        self.aggressiveness = agg
        
        self.target = target
        self.dAggAbs = params[6]
        self.dAggRel = params[5]
        self.learnRateAgg = params[7]
        self.learnRateTheta = params[8]
        self.smithsAlpha = smithsAlpha
        self.smithsAlphaMin = 0.099
        self.smithsAlphaMax = 0.101
        self.gamma = params[9]
        
        self.phi = params[11]
        
        self.maxNewtonItter = 10
        self.maxNewtonError = 0.0001


    def updateEq(self, price):
        self.eqlbm = self.eqlbm_alpha * price + (1 - self.eqlbm_alpha) * self.eqlbm
        
    def newton4Buying(self):
        theta_est = self.theta
        rightHside = ((self.theta * (self.limit - self.eqlbm)) / float(math.exp(self.theta) - 1));
        i = 0
        while i <= self.maxNewtonItter:
            eX = math.exp(theta_est)
            eXminOne = eX - 1
            fofX = (((theta_est * self.eqlbm) / float(eXminOne)) - rightHside)
            if abs(fofX) <= self.maxNewtonError:
                break
            dfofX = ((self.eqlbm / eXminOne) - ((eX * self.eqlbm * theta_est) / float(eXminOne * eXminOne)))
            theta_est = (theta_est - (fofX / float(dfofX)));
            i += 1
        if theta_est == 0.0: theta_est += 0.000001
        return theta_est
    
    def newton4Selling(self):
        theta_est = self.theta
        rightHside = ((self.theta * (self.eqlbm - self.limit)) / float(math.exp(self.theta) - 1))
        i = 0
        while i <= self.maxNewtonItter:
            eX = math.exp(theta_est)
            eXminOne = eX - 1
            fofX = (((theta_est * (self.marketMax - self.eqlbm)) / float(eXminOne)) - rightHside)
            if abs(fofX) <= self.maxNewtonError:
                break
            dfofX = (((self.marketMax - self.eqlbm) / eXminOne) - ((eX * (self.marketMax - self.eqlbm) * theta_est) / float(eXminOne * eXminOne)))
            theta_est = (theta_est - (fofX / float(dfofX)))
            i += 1
        if theta_est == 0.0: theta_est += 0.000001
        return theta_est
        
    def updateTarget(self):
        if self.buying:
            if self.limit < self.eqlbm:
                # Extra-marginal buyer
                if self.aggressiveness >= 0: target = self.limit
                else: target = self.limit * (1 - (math.exp(-self.aggressiveness * self.theta) - 1) / float(math.exp(self.theta) - 1))
                self.target = target
            else:
                # Intra-marginal buyer
                if self.aggressiveness >= 0: target = (self.eqlbm + (self.limit - self.eqlbm) * ((math.exp(self.aggressiveness * self.theta) - 1) / float(math.exp(self.theta) - 1)))
                else:
                    theta_est = self.newton4Buying()
                    target = self.eqlbm * (1 - (math.exp(-self.aggressiveness * theta_est) - 1) / float(math.exp(theta_est) - 1))
                self.target = target
        else:
            if self.limit > self.eqlbm:
                # Extra-marginal seller
                if self.aggressiveness >= 0: target = self.limit
                else: target = self.limit + (self.marketMax - self.limit) * ((math.exp(-self.aggressiveness * self.theta) - 1) / float(math.exp(self.theta) - 1))
                self.target = target
            else:
                # Intra-marginal seller
                if self.aggressiveness >= 0: target = self.limit + (self.eqlbm - self.limit) * (1 - (math.exp(self.aggressiveness * self.theta) - 1) / float(math.exp(self.theta) - 1))
                else:
                    theta_est = self.newton4Selling() 
                    target = self.eqlbm + (self.marketMax - self.eqlbm) * ((math.exp(-self.aggressiveness * theta_est) - 1) / (math.exp(theta_est) - 1))
                self.target = target
    
    def calcRshout(self, target):
        # target must be:
        #    - highest bid if last was bid
        #    - lowest ask if last was ask
        #    - trade price if last was trade
        if self.buying:
            # Are we extramarginal?
            if self.eqlbm >= self.limit:
                r_shout = 0.0
            else:  # Intra-marginal
                if target > self.eqlbm:
                    if target > self.limit: target = self.limit
                    r_shout = math.log((((target - self.eqlbm) * (math.exp(self.theta) - 1)) / (self.limit - self.eqlbm)) + 1) / self.theta
                else:  # other formula for intra buyer
                    r_shout = math.log((1 - (target / self.eqlbm)) * (math.exp(self.newton4Buying()) - 1) + 1) / -self.newton4Buying()
        else:  # Selling
            # Are we extra-marginal?
            if self.limit >= self.eqlbm:
                r_shout = 0.0
            else:  # Intra-marginal
                if target > self.eqlbm:
                    r_shout = math.log(((target - self.eqlbm) * (math.exp(self.newton4Selling()) - 1)) / (self.marketMax - self.eqlbm) + 1) / -self.newton4Selling()
                else:  # other intra seller formula
                    if target < self.limit: target = self.limit
                    r_shout = math.log((1 - (target - self.limit) / (self.eqlbm - self.limit)) * (math.exp(self.theta) - 1) + 1) / self.theta
        return r_shout
    
    def updateAgg(self, up, target):
        if up:
            delta = (1 + self.dAggRel) * self.calcRshout(target) + self.dAggAbs
        else:
            delta = (1 - self.dAggRel) * self.calcRshout(target) - self.dAggAbs
        vol_adapt_component = self.aggressiveness + self.learnRateAgg * (delta - self.aggressiveness)
        seconds_elapsed=(datetime.datetime.combine(self.date,self.time)-datetime.datetime.combine(self.date,self.start)).seconds
        time_component = (math.exp(self.phi * ( seconds_elapsed/float(self.total_time_sec) ) ) - 1) / (math.exp(self.phi)-1.0)
        new_agg = vol_adapt_component+(1-vol_adapt_component)*time_component
        if new_agg > 1.0: new_agg = 1.0
        elif new_agg < 0.0: new_agg = 0.000001
        self.aggressiveness = new_agg
    
    def updateSalpha(self, price):
        self.lastTrades.append(price)
        if not (len(self.lastTrades) <= self.nLastTrades): self.lastTrades.pop(0)
        self.smithsAlpha = math.sqrt(sum(((p - self.eqlbm) ** 2) for p in self.lastTrades) * (1 / float(len(self.lastTrades)))) / self.eqlbm
        if self.smithsAlpha < self.smithsAlphaMin: self.smithsAlphaMin = self.smithsAlpha
        if self.smithsAlpha > self.smithsAlphaMax: self.smithsAlphaMax = self.smithsAlpha
    
    def updateTheta(self):
        alphaBar = (self.smithsAlpha - self.smithsAlphaMin) / (self.smithsAlphaMax - self.smithsAlphaMin)
        desiredTheta = (self.thetaMax - self.thetaMin) * (1 - (alphaBar * math.exp(self.gamma * (alphaBar - 1)))) + self.thetaMin
        theta = self.theta + self.learnRateTheta * (desiredTheta - self.theta)
        if theta == 0: theta += 0.0000001
        self.theta = theta
        
    def submitQuote(self):
        if self.buying:
            price = (self.currentBid + (self.target - self.currentBid) * self.eta)
            self.myquote = Quote(self.time, True, price, self.volume)
            self.submittedTrade = True
        else: 
            price = (self.currentAsk - (self.currentAsk - self.target) * self.eta)
            self.myquote = Quote(self.time, False, price, self.volume)

            self.submittedTrade = True
                    
    def checkForClearing(self, price,time):
        if self.buying and (price <= self.myquote.price):
            self.trade = [datetime.datetime.combine(self.date, time),price]
            self.notTraded = False
        elif (not self.buying) and (price >= self.myquote.price):
            self.trade = [datetime.datetime.combine(self.date, time),price]
            self.notTraded = False
            
    def getTradeResults(self):
            return self.trade
        
    def newInfo(self, time, price, trade, bid):
        self.time = time
        if self.sleepTime > 0:
            self.sleepTime -= 1
        if trade:
            self.updateEq(price)
            self.updateSalpha(price)
            self.updateTheta()
        else:
            if bid: self.currentBid = price
            else: self.currentAsk = price

        if self.buying:
            if trade:
                if self.target >= price: 
                    self.updateAgg(False, price)
                else: self.updateAgg(True, price)
            else: 
                if bid and (self.target <= price): self.updateAgg(True, self.currentBid)
        else:  # selling
            if trade:
                if self.target <= price:  self.updateAgg(False, price)
                else: self.updateAgg(True, price)
            else:
                if (not bid) and (self.target >= price): self.updateAgg(True, self.currentAsk)
        self.updateTarget()
        # Do I still need to trade?
        if self.notTraded:
            # If I've submitted a quote let's see if it's expired or if it clears
            if self.submittedTrade:
                if time > (datetime.datetime.combine(self.date, self.myquote.born) + self.maxQuoteLife).time():
                    # cancel old and submit new quote
                    self.submitQuote()
                # Will it clear?
                if trade:
                    self.checkForClearing(price,time)
            # If wait time is over and I am yet to submit a quote - submit one
            elif (self.sleepTime <= 0):
                self.submitQuote()
