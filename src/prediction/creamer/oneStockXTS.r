# Created on 15 Aug 2012
#
# @author: Ash Booth
#
# This creates an xts object for a given stock that contains the following 
# technical indicators and trading rules ready for the machine learning layer
#
#
# Indicators:
# - ema1    - ema2    - ema3    - sma1    - sma2    - sma3
# - bbl1    - bbh1    - bbl2    - bbh2    - bbl3    - bbh3
# - mom1    - mom2    - mom3    - acc1    - acc2    - acc3
# - roc1    - roc2    - roc3    - macd1   - macd2   - macd3
# - macds1  - macds2  - macds3  - rsi1    - rsi2    - rsi3
# - fastk1  - fastk2  - fastk3  - fastd1  - fastd2  - fastd3
# - slowk1  - slowk2  - slowk3  - slowd1  - slowd2  - slowd3
# - will    - mfi     - chv     - gkv     - adl     - obv
# - cho     - pvi     - nvi
#
# Ratios
# - ema2close     - close2bbh1    - close2bbh2    - close2bbh3
# - close2bbl1    - close2bbl2    - close2bbl3    - emamom1
# - emamom2       - emamom3       - mom2emamom1   - mom2emamom2
# - mom2emamom3   - macd2macds1   - macd2macds2   - macd2macds3
# - slowk2slowd1  - slowk2slowd2  - slowk2slowd3  - fastk2fastd1
# - fastk2fastd2  - fastk2fastd3  - pvi2smapvi    - nvi2smanvi
#
# Trading Rules
# - bolTR1    - bolTR2    - bolTR3    - momTR1    - momTR2
# - momTR3    - accTR1    - accTR2    - accTR3    - rosTR1
# - rocTR2    - rocTR3    - macdTR1   - macdTR2   - macdTR3
# - rsiTR1    - rsiTR2    - rsiTR3    - fastTR1   - fastTR2
# - fastTR3   - slowTR1   - slowTR2   - slowTR3   - willTR
# - mfiTR     - pviTR     - nviTR

library(fTrading)
library(TTR)
library(fGarch)

LONGLAG<-61

### newCode
#createNewDatabase <-function(filename) {
#
#  # Creae dataframe from csv
#  all_data<-read.csv("20120621AAPL US Equityopen.csv",header=F)
#  
#  # Pull out the trades
#  trade_data <- all_data[all_data[2]=='TRADE',]
#  
#  ## function for converting to string of times to time objects 
#  trade_data$V1 <- as.POSIXct(trade_data$V1, "%Y-%m-%d %H:%M:%S")
  
#  # Move to XTS
#  trade_XTS<- xts(trade_data[,-1], order.by=trade_data[,1])
  
#  # create a vector of times at 10 sec intervals
#  x<-as.POSIXct('2012-06-21 14:00:00', "%Y-%m-%d %H:%M:%S") + 10*c(1:5)
#}


createDatabase <- function(ticker,START,END) {
  assetData<-getYahooData(ticker,START,END,freq="daily",adjust=TRUE)
  
  # Calculate EMAs
  remoteEMAn1<-10
  remoteEMAn2<-16
  remoteEMAn3<-22
  remoteEMA1<-emaTA(assetData$Close,remoteEMAn1)
  remoteEMA2<-emaTA(assetData$Close,remoteEMAn2)
  remoteEMA3<-emaTA(assetData$Close,remoteEMAn3)
  
  # Calculate SMAs
  remoteSMAn1 <- 10
  remoteSMAn2 <- 16
  remoteSMAn3 <- 22
  remoteSMA1<-SMA(assetData$Close,remoteSMAn1)
  remoteSMA2<-SMA(assetData$Close,remoteSMAn2)
  remoteSMA3<-SMA(assetData$Close,remoteSMAn3)
  
  # Calculate Bollinger bands
  remoteBoln1 <- 20
  remoteBoln2 <- 26
  remoteBoln3 <- 32
  remoteBB1<-BBands(assetData$Close,n=remoteBoln1)
  remoteBB2<-BBands(assetData$Close,n=remoteBoln2)
  remoteBB3<-BBands(assetData$Close,n=remoteBoln3)
  ### remoteBB[,1] is the down
  ### remoteBB[,2] is the mvAv
  ### remoteBB[,3] is the up
  ### remoteBB[,4] is the %B calculation
  remoteBBL1 <-remoteBB1[,1]
  remoteBBH1 <-remoteBB1[,3]
  remoteBBL2 <-remoteBB2[,1]
  remoteBBH2 <-remoteBB2[,3]
  remoteBBL3 <-remoteBB3[,1]
  remoteBBH3 <-remoteBB3[,3]
  
  # Calculate Momentum
  remoteMOMn1 <- 12
  remoteMOMn2 <- 18
  remoteMOMn3 <- 24
  remoteMOM1<-momentum(assetData$Close,n=remoteMOMn1)
  remoteMOM2<-momentum(assetData$Close,n=remoteMOMn2)
  remoteMOM3<-momentum(assetData$Close,n=remoteMOMn3)
  
  # Calculate acceleration
  remoteACC1<-diff(remoteMOM1)
  remoteACC2<-diff(remoteMOM2)
  remoteACC3<-diff(remoteMOM3)
  
  
  #Calculate Rate of Change
  remoteROCn1 <- 10
  remoteROCn2 <- 16
  remoteROCn3 <- 22
  remoteROC1<-ROC(assetData$Close, n=remoteROCn1)
  remoteROC2<-ROC(assetData$Close, n=remoteROCn2)
  remoteROC3<-ROC(assetData$Close, n=remoteROCn3)    
  
  # Calculate MACD and signal
  remoteMACDs <- 12
  remoteMACDf1 <- 18
  remoteMACDf2 <- 24
  remoteMACDf3 <- 30
  remoteMACDn <- 9
  remoteMACDDS1<-MACD(assetData$Close,nSlow=remoteMACDf1,nFast=remoteMACDs, nSig=remoteMACDn)
  remoteMACDDS2<-MACD(assetData$Close,nSlow=remoteMACDf2,nFast=remoteMACDs, nSig=remoteMACDn)
  remoteMACDDS3<-MACD(assetData$Close,nSlow=remoteMACDf3,nFast=remoteMACDs, nSig=remoteMACDn)
  remoteMACD1 <-remoteMACDDS1$macd
  remoteMACD2 <-remoteMACDDS2$macd
  remoteMACD3 <-remoteMACDDS3$macd
  remoteMACDS1 <-remoteMACDDS1$signal
  remoteMACDS2 <-remoteMACDDS2$signal
  remoteMACDS3 <-remoteMACDDS3$signal
  
  # Calculate Relative Strength Index
  remoteRSIn1 <- 8
  remoteRSIn2 <- 14
  remoteRSIn3 <- 20
  remoteRSI1<-RSI(assetData$Close,n=remoteRSIn1)
  remoteRSI2<-RSI(assetData$Close,n=remoteRSIn2)
  remoteRSI3<-RSI(assetData$Close,n=remoteRSIn3)
  
  # Calculate Fast K
  remoteFASTKn1 <- 12 
  remoteFASTKn2 <- 18
  remoteFASTKn3 <- 24
  remoteFASTK1<-fpkTA(assetData$Close,assetData$High,assetData$Low,remoteFASTKn1)
  remoteFASTK2<-fpkTA(assetData$Close,assetData$High,assetData$Low,remoteFASTKn2)
  remoteFASTK3<-fpkTA(assetData$Close,assetData$High,assetData$Low,remoteFASTKn3)
  
  # Calculate Fast D
  # Need to figure out which lag is which by plotting
  remoteFASTDn <- 3
  remoteFASTD1<-SMA(remoteFASTK1,remoteFASTDn)
  remoteFASTD2<-SMA(remoteFASTK2,remoteFASTDn)
  remoteFASTD3<-SMA(remoteFASTK3,remoteFASTDn)
  
  # Calculate slow K
  remoteSLOWK1<-SMA(remoteFASTD1,remoteFASTDn)
  remoteSLOWK2<-SMA(remoteFASTD2,remoteFASTDn)
  remoteSLOWK3<-SMA(remoteFASTD3,remoteFASTDn)
  
  
  # Calculate slow D
  remoteSLOWD1<-SMA(remoteSLOWK1,remoteFASTDn)
  remoteSLOWD2<-SMA(remoteSLOWK2,remoteFASTDn)
  remoteSLOWD3<-SMA(remoteSLOWK3,remoteFASTDn)
  
  # Calculate Williams %R
  remoteWILL<-WPR(assetData[,c("High","Low","Close")], n=14)
  
  # Calculate Money Flow Index
  remoteMFI<-MFI(assetData[,c("High","Low","Close")], assetData$Volume, n=14)
  
  # Calculate Chaikin Volatility
  remoteCHVn = 10
  remoteCHV<-chaikinVolatility(assetData[,c("High","Low")],n=remoteCHVn)
  
  # Calculate Garman Klauss Volatility
  remoteGKV<-volatility(assetData[,c("Open","High","Low","Close")], calc="garman")
  
  # Estimate next period with GARCH
  # my intraday returns
  #     logDiff<-log(assetData$Close/assetData$Open)
  #     remoteGRCHR<-rep(NA,length(logDiff))
  #     remoteGRCHV<-rep(NA,length(logDiff))
  #     remoteGRCHS<-rep(NA,length(logDiff))
  #     counter<-1
  #     for(i in remoteGRCHR) {
  #       if(counter>60) {
  #         spec = garchSpec()
  #         fit <- fGarch::garchFit(~ arma(2,1)+garch(1,1), data=logDiff[c(1:counter)], trace=FALSE)
  #         prediction<-predict(fit, n.ahead=2)
  #         
  #         i<-prediction$meanForecast[1]
  #         remoteGRCHV[counter]<-prediction$standardDeviation[1]
  #         remoteGRCHS[counter]<-(prediction$meanForecast[1]/prediction$standardDeviation[1])
  #       }
  #       counter<-counter+1
  #     }
  #     
  # Calculate accumulation/distribution line
  remoteADL<-chaikinAD(assetData[,c("High","Low","Close")],assetData[,"Volume"])
  
  # Calculate On Balance Volume
  remoteOBV<-OBV(assetData[,"Close"],assetData[,"Volume"])
  
  # Calculate Chaikin Oscillator
  remoteCHOs <- 3
  remoteCHOf <- 10
  remoteCHOall<-MACD(remoteADL,nSlow=remoteCHOf,nFast=remoteCHOs)
  remoteCHO<-remoteCHOall$macd
  
  # Positive and Negative Volume indexes
  remotePVI<-rep(1,length(assetData$Close))
  remoteNVI<-rep(1,length(assetData$Close))
  counter<-1
  for(i in remotePVI) {
    if(counter>1) {
      if(as.numeric(assetData$Volume[counter]) > as.numeric(assetData$Volume[counter-1])) {
        remotePVI[counter]<-(remotePVI[counter-1] + (((as.numeric(assetData$Close[counter]) - as.numeric(assetData$Close[counter-1])) / as.numeric(assetData$Close[counter-1]))*remotePVI[counter-1]))
        remoteNVI[counter]<-remoteNVI[counter-1]
      } else if(as.numeric(assetData$Volume[counter]) < as.numeric(assetData$Volume[counter-1])) {
        remotePVI[counter]<-remotePVI[counter-1]
        remoteNVI[counter]<-(remoteNVI[counter-1] + (((as.numeric(assetData$Close[counter]) - as.numeric(assetData$Close[counter-1])) / as.numeric(assetData$Close[counter-1]))*remoteNVI[counter-1]))
      } else {
        remotePVI[counter]<-remotePVI[counter-1]
        remoteNVI<-remoteNVI[counter-1]
      } 
    }
    counter<-counter+1
  }
  
  ####################################
  ############## RATIOS ##############
  ####################################
  
  # ema/close
  ema2close<-(remoteEMA1/assetData$Close)
  
  # close/bbh
  close2bbh1<-(assetData$Close/remoteBBH1)
  close2bbh2<-(assetData$Close/remoteBBH2)
  close2bbh3<-(assetData$Close/remoteBBH3)
  
  # close/bbl
  close2bbl1<-(assetData$Close/remoteBBL1)
  close2bbl2<-(assetData$Close/remoteBBL2)
  close2bbl3<-(assetData$Close/remoteBBL3)
  
  # mom/ema(mom)
  emamom1<-EMA(remoteMOM1,n=10)
  emamom2<-EMA(remoteMOM2,n=10)
  emamom3<-EMA(remoteMOM3,n=10)
  mom2emamom1<-(remoteMOM1/emamom1)
  mom2emamom2<-(remoteMOM2/emamom2)
  mom2emamom3<-(remoteMOM3/emamom3)
  
  # macd/macds
  macd2macds1<-(remoteMACD1/remoteMACDS1)
  macd2macds2<-(remoteMACD2/remoteMACDS2)
  macd2macds3<-(remoteMACD3/remoteMACDS3)
  
  # slowk/slowd
  slowk2slowd1<-(remoteSLOWK1/remoteSLOWD1)
  slowk2slowd2<-(remoteSLOWK2/remoteSLOWD2)
  slowk2slowd3<-(remoteSLOWK3/remoteSLOWD3)
  
  # fastk/fastd
  fastk2fastd1<-(remoteFASTK1/remoteFASTD1)
  fastk2fastd2<-(remoteFASTK2/remoteFASTD2)
  fastk2fastd3<-(remoteFASTK3/remoteFASTD3)
  
  # nvi/smanvi
  smanvi<-SMA(remoteNVI,n=10)
  nvi2smanvi<-(remoteNVI/smanvi)
  
  # pvi/smapvi
  smapvi<-SMA(remotePVI,n=10)
  pvi2smapvi<-(remotePVI/smapvi)
  
  ####################################
  ############## RULES ###############
  ####################################
  
  # Bolinger trading rules
  bolTR1 <- rep(NA,length(remoteBBL1))
  counter <- 1
  for(i in bolTR1) {
    if(counter>35){
      if((as.numeric(assetData$Close[counter-1])>=as.numeric(remoteBBL1[counter])) && (as.numeric(assetData$Close[counter])<as.numeric(remoteBBH1[counter]))){
        bolTR1[counter]<-"buy"
      } else if((as.numeric(assetData$Close[counter-1])<=as.numeric(remoteBBL1[counter])) && (as.numeric(assetData$Close[counter])>as.numeric(remoteBBH1[counter]))) {
        bolTR1[counter]<-"sell"
      } else {
        bolTR1[counter]<-"hold"
      }
    }
    counter <- counter+1
  }
  
  bolTR2 <- rep(NA,length(remoteBBL2))
  counter <- 1
  for(i in bolTR2) {
    if(counter>35){
      if((as.numeric(assetData$Close[counter-1])>=as.numeric(remoteBBL2[counter])) && (as.numeric(assetData$Close[counter])<as.numeric(remoteBBH2[counter]))){
        bolTR2[counter]<-"buy"
      } else if((as.numeric(assetData$Close[counter-1])<=as.numeric(remoteBBL2[counter])) && (as.numeric(assetData$Close[counter])>as.numeric(remoteBBH2[counter]))) {
        bolTR2[counter]<-"sell"
      } else {
        bolTR2[counter]<-"hold"
      }
    }
    counter <- counter+1
  }
  
  bolTR3 <- rep(NA,length(remoteBBL3))
  counter <- 1
  for(i in bolTR3) {
    if(counter>35){
      if((as.numeric(assetData$Close[counter-1])>=as.numeric(remoteBBL3[counter])) && (as.numeric(assetData$Close[counter])<as.numeric(remoteBBH3[counter]))){
        bolTR3[counter]<-"buy"
      } else if((as.numeric(assetData$Close[counter-1])<=as.numeric(remoteBBL3[counter])) && (as.numeric(assetData$Close[counter])>as.numeric(remoteBBH3[counter]))) {
        bolTR3[counter]<-"sell"
      } else {
        bolTR3[counter]<-"hold"
      }
    }
    counter <- counter+1
  }
  
  # Momentum trading rule
  momTR1 <- rep(NA,length(remoteMOM1))
  counter <- 1
  for(i in momTR1) {
    if(counter>35){
      if((as.numeric(remoteMOM1[counter-1])<=as.numeric(emamom1[counter])) && (as.numeric(remoteMOM1[counter])>as.numeric(emamom1[counter]))){
        momTR1[counter]<-"buy"
      } else if((as.numeric(remoteMOM1[counter-1])>=as.numeric(emamom1[counter])) && (as.numeric(remoteMOM1[counter])<as.numeric(emamom1[counter]))) {
        momTR1[counter]<-"sell"
      } else {
        momTR1[counter]<-"hold"
      }
    }
    counter <- counter+1
  }
  
  momTR2 <- rep(NA,length(remoteMOM2))
  counter <- 1
  for(i in momTR2) {
    if(counter>35){
      if((as.numeric(remoteMOM2[counter-1])<=as.numeric(emamom2[counter])) && (as.numeric(remoteMOM2[counter])>as.numeric(emamom2[counter]))){
        momTR2[counter]<-"buy"
      } else if((as.numeric(remoteMOM2[counter-1])>=as.numeric(emamom2[counter])) && (as.numeric(remoteMOM2[counter])<as.numeric(emamom2[counter]))) {
        momTR2[counter]<-"sell"
      } else {
        momTR2[counter]<-"hold"
      }
    }
    counter <- counter+1
  }
  
  momTR3 <- rep(NA,length(remoteMOM3))
  counter <- 1
  for(i in momTR3) {
    if(counter>35){
      if((as.numeric(remoteMOM3[counter-1])<=as.numeric(emamom3[counter])) && (as.numeric(remoteMOM3[counter])>as.numeric(emamom3[counter]))){
        momTR3[counter]<-"buy"
      } else if((as.numeric(remoteMOM3[counter-1])>=as.numeric(emamom3[counter])) && (as.numeric(remoteMOM3[counter])<as.numeric(emamom3[counter]))) {
        momTR3[counter]<-"sell"
      } else {
        momTR3[counter]<-"hold"
      }
    }
    counter <- counter+1
  }
  
  # Acceleration trading rule
  accTR1 <- rep(NA,length(remoteACC1))
  counter <- 1
  for(i in accTR1) {
    if(counter>30){
      if((as.numeric(remoteACC1[counter-1])+1<=0) && (as.numeric(remoteACC1[counter])+1>0)){
        accTR1[counter]<-"buy"
      } else if((as.numeric(remoteACC1[counter-1])+1>=0) && (as.numeric(remoteACC1[counter])+1<0)) {
        accTR1[counter]<-"sell"
      } else {
        accTR1[counter]<-"hold"
      }
    }
    counter <- counter+1
  }
  
  accTR2 <- rep(NA,length(remoteACC2))
  counter <- 1
  for(i in accTR2) {
    if(counter>30){
      if((as.numeric(remoteACC2[counter-1])+1<=0) && (as.numeric(remoteACC2[counter])+1>0)){
        accTR2[counter]<-"buy"
      } else if((as.numeric(remoteACC2[counter-1])+1>=0) && (as.numeric(remoteACC2[counter])+1<0)) {
        accTR2[counter]<-"sell"
      } else {
        accTR2[counter]<-"hold"
      }
    }
    counter <- counter+1
  }
  
  accTR3 <- rep(NA,length(remoteACC3))
  counter <- 1
  for(i in accTR3) {
    if(counter>30){
      if((as.numeric(remoteACC3[counter-1])+1<=0) && (as.numeric(remoteACC3[counter])+1>0)){
        accTR3[counter]<-"buy"
      } else if((as.numeric(remoteACC3[counter-1])+1>=0) && (as.numeric(remoteACC3[counter])+1<0)) {
        accTR3[counter]<-"sell"
      } else {
        accTR3[counter]<-"hold"
      }
    }
    counter <- counter+1
  }
  
  # ROC trading rule
  rocTR1 <- rep(NA,length(remoteROC1))
  counter <- 1
  for(i in rocTR1) {
    if(counter>32){
      if((as.numeric(remoteROC1[counter-1])<=0) && (as.numeric(remoteROC1[counter])>0)){
        rocTR1[counter]<-"buy"
      } else if((as.numeric(remoteROC1[counter-1])>=0) && (as.numeric(remoteROC1[counter])<0)) {
        rocTR1[counter]<-"sell"
      } else {
        rocTR1[counter]<-"hold"
      }
    }
    counter <- counter+1
  }
  
  rocTR2 <- rep(NA,length(remoteROC2))
  counter <- 1
  for(i in rocTR2) {
    if(counter>32){
      if((as.numeric(remoteROC2[counter-1])<=0) && (as.numeric(remoteROC2[counter])>0)){
        rocTR2[counter]<-"buy"
      } else if((as.numeric(remoteROC2[counter-1])>=0) && (as.numeric(remoteROC2[counter])<0)) {
        rocTR2[counter]<-"sell"
      } else {
        rocTR2[counter]<-"hold"
      }
    }
    counter <- counter+1
  }
  
  rocTR3 <- rep(NA,length(remoteROC3))
  counter <- 1
  for(i in rocTR3) {
    if(counter>32){
      if((as.numeric(remoteROC3[counter-1])<=0) && (as.numeric(remoteROC3[counter])>0)){
        rocTR3[counter]<-"buy"
      } else if((as.numeric(remoteROC3[counter-1])>=0) && (as.numeric(remoteROC3[counter])<0)) {
        rocTR3[counter]<-"sell"
      } else {
        rocTR3[counter]<-"hold"
      }
    }
    counter <- counter+1
  }
  
  # macd trading rules
  macdTR1 <- rep(NA,length(remoteMACD1))
  counter <- 1
  for(i in macdTR1) {
    if(counter>40){
      if((as.numeric(remoteMACD1[counter-1])<=as.numeric(remoteMACDS1[counter])) && (as.numeric(remoteMACD1[counter])>as.numeric(remoteMACDS1[counter]))){
        macdTR1[counter]<-"buy"
      } else if((as.numeric(remoteMACD1[counter-1])>=as.numeric(remoteMACDS1[counter])) && (as.numeric(remoteMACD1[counter])<as.numeric(remoteMACDS1[counter]))){
        macdTR1[counter]<-"sell"
      } else {
        macdTR1[counter]<-"hold"
      }
    }
    counter <- counter+1
  }
  
  macdTR2 <- rep(NA,length(remoteMACD2))
  counter <- 1
  for(i in macdTR2) {
    if(counter>40){
      if((as.numeric(remoteMACD2[counter-1])<=as.numeric(remoteMACDS2[counter])) && (as.numeric(remoteMACD2[counter])>as.numeric(remoteMACDS2[counter]))){
        macdTR2[counter]<-"buy"
      } else if((as.numeric(remoteMACD2[counter-1])>=as.numeric(remoteMACDS2[counter])) && (as.numeric(remoteMACD2[counter])<as.numeric(remoteMACDS2[counter]))) {
        macdTR2[counter]<-"sell"
      } else {
        macdTR2[counter]<-"hold"
      }
    }
    counter <- counter+1
  }
  
  macdTR3 <- rep(NA,length(remoteMACD3))
  counter <- 1
  for(i in macdTR3) {
    if(counter>40){
      if((as.numeric(remoteMACD3[counter-1])<=as.numeric(remoteMACDS3[counter])) && (as.numeric(remoteMACD3[counter])>as.numeric(remoteMACDS3[counter]))){
        macdTR3[counter]<-"buy"
      } else if((as.numeric(remoteMACD3[counter-1])>=as.numeric(remoteMACDS3[counter])) && (as.numeric(remoteMACD3[counter])<as.numeric(remoteMACDS3[counter]))) {
        macdTR3[counter]<-"sell"
      } else {
        macdTR3[counter]<-"hold"
      }
    }
    counter <- counter+1
  }
  
  # RSI trading rule
  rsiTR1 <- rep(NA,length(remoteRSI1))
  counter <- 1
  for(i in rsiTR1) {
    if(counter>30){
      if((as.numeric(remoteRSI1[counter-1])>=30) && (as.numeric(remoteRSI1[counter])<70)){
        rsiTR1[counter]<-"buy"
      } else if((as.numeric(remoteRSI1[counter-1])<=30) && (as.numeric(remoteRSI1[counter])>70)) {
        rsiTR1[counter]<-"sell"
      } else {
        rsiTR1[counter]<-"hold"
      }
    }
    counter <- counter+1
  }
  
  rsiTR2 <- rep(NA,length(remoteRSI2))
  counter <- 1
  for(i in rsiTR2) {
    if(counter>30){
      if((as.numeric(remoteRSI2[counter-1])>=30) && (as.numeric(remoteRSI2[counter])<70)){
        rsiTR2[counter]<-"buy"
      } else if((as.numeric(remoteRSI2[counter-1])<=30) && (as.numeric(remoteRSI2[counter])>70)) {
        rsiTR2[counter]<-"sell"
      } else {
        rsiTR2[counter]<-"hold"
      }
    }
    counter <- counter+1
  }
  
  rsiTR3 <- rep(NA,length(remoteRSI3))
  counter <- 1
  for(i in rsiTR3) {
    if(counter>30){
      if((as.numeric(remoteRSI3[counter-1])>=30) && (as.numeric(remoteRSI3[counter]) < 70)){
        rsiTR3[counter]<-"buy"
      } else if((as.numeric(remoteRSI3[counter-1]) <= 30) && (as.numeric(remoteRSI3[counter])>70)) {
        rsiTR3[counter]<-"sell"
      } else {
        rsiTR3[counter]<-"hold"
      }
    }
    counter <- counter+1
  }
  
  # Fast stochastic trading rule
  fastTR1 <- rep(NA,length(remoteFASTK1))
  counter <- 1
  for(i in fastTR1) {
    if(counter>10){
      if((as.numeric(remoteFASTK1[counter-1])<=as.numeric(remoteFASTD1[counter])) && (as.numeric(remoteFASTK1[counter])>as.numeric(remoteFASTD1[counter]))){
        fastTR1[counter]<-"buy"
      } else if((as.numeric(remoteFASTK1[counter-1])>=as.numeric(remoteFASTD1[counter])) && (as.numeric(remoteFASTK1[counter])<as.numeric(remoteFASTD1[counter]))) {
        fastTR1[counter]<-"sell"
      } else {
        fastTR1[counter]<-"hold"
      }
    }
    counter <- counter+1
  }
  
  fastTR2 <- rep(NA,length(remoteFASTK2))
  counter <- 1
  for(i in fastTR2) {
    if(counter>10){
      if((as.numeric(remoteFASTK2[counter-1])<=as.numeric(remoteFASTD2[counter])) && (as.numeric(remoteFASTK2[counter])>as.numeric(remoteFASTD2[counter]))){
        fastTR2[counter]<-"buy"
      } else if((as.numeric(remoteFASTK2[counter-1])>=as.numeric(remoteFASTD2[counter])) && (as.numeric(remoteFASTK2[counter])<as.numeric(remoteFASTD2[counter]))) {
        fastTR2[counter]<-"sell"
      } else {
        fastTR2[counter]<-"hold"
      }
    }
    counter <- counter+1
  }
  
  fastTR3 <- rep(NA,length(remoteFASTK3))
  counter <- 1
  for(i in fastTR3) {
    if(counter>10){
      if((as.numeric(remoteFASTK3[counter-1])<=as.numeric(remoteFASTD3[counter])) && (as.numeric(remoteFASTK3[counter])>as.numeric(remoteFASTD3[counter]))){
        fastTR3[counter]<-"buy"
      } else if((as.numeric(remoteFASTK3[counter-1])>=as.numeric(remoteFASTD3[counter])) && (as.numeric(remoteFASTK3[counter])<as.numeric(remoteFASTD3[counter]))) {
        fastTR3[counter]<-"sell"
      } else {
        fastTR3[counter]<-"hold"
      }
    }
    counter <- counter+1
  }
  
  # slow stochastic trading rules
  slowTR1 <- rep(NA,length(remoteSLOWK1))
  counter <- 1
  for(i in slowTR1) {
    if(counter>10){
      if((as.numeric(remoteSLOWK1[counter-1])<=as.numeric(remoteSLOWD1[counter])) && (as.numeric(remoteSLOWK1[counter])>as.numeric(remoteSLOWD1[counter]))){
        slowTR1[counter]<-"buy"
      } else if((as.numeric(remoteSLOWK1[counter-1])>=as.numeric(remoteSLOWD1[counter])) && (as.numeric(remoteSLOWK1[counter])<as.numeric(remoteSLOWD1[counter]))) {
        slowTR1[counter]<-"sell"
      } else {
        slowTR1[counter]<-"hold"
      }
    }
    counter <- counter+1
  }
  
  slowTR2 <- rep(NA,length(remoteSLOWK2))
  counter <- 1
  for(i in slowTR2) {
    if(counter>10){
      if((as.numeric(remoteSLOWK2[counter-1])<=as.numeric(remoteSLOWD2[counter])) && (as.numeric(remoteSLOWK2[counter])>as.numeric(remoteSLOWD2[counter]))){
        slowTR2[counter]<-"buy"
      } else if((as.numeric(remoteSLOWK2[counter-1])>=as.numeric(remoteSLOWD2[counter])) && (as.numeric(remoteSLOWK2[counter])<as.numeric(remoteSLOWD2[counter]))) {
        slowTR2[counter]<-"sell"
      } else {
        slowTR2[counter]<-"hold"
      }
    }
    counter <- counter+1
  }
  
  slowTR3 <- rep(NA,length(remoteSLOWK3))
  counter <- 1
  for(i in slowTR3) {
    if(counter>10){
      if((as.numeric(remoteSLOWK3[counter-1])<=as.numeric(remoteSLOWD3[counter])) && (as.numeric(remoteSLOWK3[counter])>as.numeric(remoteSLOWD3[counter]))){
        slowTR3[counter]<-"buy"
      } else if((as.numeric(remoteSLOWK3[counter-1])>=as.numeric(remoteSLOWD3[counter])) && (as.numeric(remoteSLOWK3[counter])<as.numeric(remoteSLOWD3[counter]))) {
        slowTR3[counter]<-"sell"
      } else {
        slowTR3[counter]<-"hold"
      }
    }
    counter <- counter+1
  }
  
  # Williams trading rule
  willTR <- rep(NA,length(remoteWILL))
  counter <- 1
  for(i in willTR) {
    if(counter>15){
      if((as.numeric(remoteWILL[counter-1])>= -20) && (as.numeric(remoteWILL[counter])< -80)){
        willTR[counter]<-"buy"
      } else if((as.numeric(remoteWILL[counter-1])<= -20) && (as.numeric(remoteWILL[counter]) > -80)) {
        willTR[counter]<-"sell"
      } else {
        willTR[counter]<-"hold"
      }
    }
    counter <- counter+1
  }
  
  # MFI Trading rule
  mfiTR <- rep(NA,length(remoteMFI))
  counter <- 1
  for(i in mfiTR) {
    if(counter>15){
      if((as.numeric(remoteMFI[counter-1])>=30) && (as.numeric(remoteMFI[counter])<70)){
        mfiTR[counter]<-"buy"
      } else if((as.numeric(remoteMFI[counter-1])<=30) && (as.numeric(remoteMFI[counter])>70)) {
        mfiTR[counter]<-"sell"
      } else {
        mfiTR[counter]<-"hold"
      }
    }
    counter <- counter+1
  }
  
  # PVI and NVI Trading rules
  pviTR <- rep(NA,length(remotePVI))
  counter <- 1
  for(i in pviTR) {
    if(counter>15){
      if((as.numeric(remotePVI[counter-1])<=as.numeric(smapvi[counter])) && (as.numeric(remotePVI[counter])>as.numeric(smapvi[counter]))){
        pviTR[counter]<-"buy"
      } else if((as.numeric(remotePVI[counter-1])>=as.numeric(smapvi[counter])) && (as.numeric(remotePVI[counter])<as.numeric(smapvi[counter]))){
        pviTR[counter]<-"sell"
      } else {
        pviTR[counter]<-"hold"
      }
    }
    counter <- counter+1
  }
  
  nviTR <- rep(NA,length(remoteNVI))
  counter <- 1
  for(i in nviTR) {
    if(counter>15){
      if((as.numeric(remoteNVI[counter-1])<=as.numeric(smanvi[counter])) && (as.numeric(remoteNVI[counter])>as.numeric(smanvi[counter]))){
        nviTR[counter]<-"buy"
      } else {
        nviTR[counter]<-"hold"
      }
    }
    counter <- counter+1
  }
  
  # Hack off spin up stuff from the begining
  remoteEMA1=remoteEMA1[-c(1:LONGLAG)]
  remoteEMA2=remoteEMA2[-c(1:LONGLAG)]
  remoteEMA3=remoteEMA3[-c(1:LONGLAG)]
  remoteSMA1=remoteSMA1[-c(1:LONGLAG)]
  remoteSMA2=remoteSMA2[-c(1:LONGLAG)]
  remoteSMA3=remoteSMA3[-c(1:LONGLAG)]
  remoteBBL1=remoteBBL1[-c(1:LONGLAG)]
  remoteBBH1=remoteBBH1[-c(1:LONGLAG)]
  remoteBBL2=remoteBBL2[-c(1:LONGLAG)]
  remoteBBH2=remoteBBH2[-c(1:LONGLAG)]
  remoteBBL3=remoteBBL3[-c(1:LONGLAG)]
  remoteBBH3=remoteBBH3[-c(1:LONGLAG)]
  remoteMOM1=remoteMOM1[-c(1:LONGLAG)]
  remoteMOM2=remoteMOM2[-c(1:LONGLAG)]
  remoteMOM3=remoteMOM3[-c(1:LONGLAG)]
  remoteACC1=remoteACC1[-c(1:LONGLAG)]
  remoteACC2=remoteACC2[-c(1:LONGLAG)]
  remoteACC3=remoteACC3[-c(1:LONGLAG)]
  remoteROC1=remoteROC1[-c(1:LONGLAG)]
  remoteROC2=remoteROC2[-c(1:LONGLAG)]
  remoteROC3=remoteROC3[-c(1:LONGLAG)]
  remoteMACD1=remoteMACD1[-c(1:LONGLAG)]
  remoteMACD2=remoteMACD2[-c(1:LONGLAG)]
  remoteMACD3=remoteMACD3[-c(1:LONGLAG)]
  remoteMACDS1=remoteMACDS1[-c(1:LONGLAG)]
  remoteMACDS2=remoteMACDS2[-c(1:LONGLAG)]
  remoteMACDS3=remoteMACDS3[-c(1:LONGLAG)]
  remoteRSI1=remoteRSI1[-c(1:LONGLAG)]
  remoteRSI2=remoteRSI2[-c(1:LONGLAG)]
  remoteRSI3=remoteRSI3[-c(1:LONGLAG)]
  remoteFASTK1=remoteFASTK1[-c(1:LONGLAG)]
  remoteFASTK2=remoteFASTK2[-c(1:LONGLAG)]
  remoteFASTK3=remoteFASTK3[-c(1:LONGLAG)]
  remoteFASTD1=remoteFASTD1[-c(1:LONGLAG)]
  remoteFASTD2=remoteFASTD2[-c(1:LONGLAG)]
  remoteFASTD3=remoteFASTD3[-c(1:LONGLAG)]
  remoteSLOWK1=remoteSLOWK1[-c(1:LONGLAG)]
  remoteSLOWK2=remoteSLOWK2[-c(1:LONGLAG)]
  remoteSLOWK3=remoteSLOWK3[-c(1:LONGLAG)]
  remoteSLOWD1=remoteSLOWD1[-c(1:LONGLAG)]
  remoteSLOWD2=remoteSLOWD2[-c(1:LONGLAG)]
  remoteSLOWD3=remoteSLOWD3[-c(1:LONGLAG)]
  remoteWILL=remoteWILL[-c(1:LONGLAG)]
  remoteMFI=remoteMFI[-c(1:LONGLAG)]
  remoteCHV=remoteCHV[-c(1:LONGLAG)]
  remoteGKV=remoteGKV[-c(1:LONGLAG)]
  #     remoteGRCHR=remoteGRCHR[-c(1:LONGLAG)]
  #     remoteGRCHV=rempteGRCHV[-c(1:LONGLAG)]
  #     remoteGRCHS=remoteGRCHS[-c(1:LONGLAG)]
  remoteADL=remoteADL[-c(1:LONGLAG)]
  remoteOBV=remoteOBV[-c(1:LONGLAG)]
  remoteCHO=remoteCHO[-c(1:LONGLAG)]
  remotePVI=remotePVI[-c(1:LONGLAG)]
  remoteNVI=remoteNVI[-c(1:LONGLAG)]
  
  ema2close=ema2close[-c(1:LONGLAG)]
  close2bbh1=close2bbh1[-c(1:LONGLAG)]
  close2bbh2=close2bbh2[-c(1:LONGLAG)]
  close2bbh3=close2bbh3[-c(1:LONGLAG)]
  close2bbl1=close2bbl1[-c(1:LONGLAG)]
  close2bbl2=close2bbl2[-c(1:LONGLAG)]
  close2bbl3=close2bbl3[-c(1:LONGLAG)]
  emamom1=emamom1[-c(1:LONGLAG)]
  emamom2=emamom2[-c(1:LONGLAG)]
  emamom3=emamom3[-c(1:LONGLAG)]
  mom2emamom1=mom2emamom1[-c(1:LONGLAG)]
  mom2emamom2=mom2emamom2[-c(1:LONGLAG)]
  mom2emamom3=mom2emamom3[-c(1:LONGLAG)]
  macd2macds1=macd2macds1[-c(1:LONGLAG)]
  macd2macds2=macd2macds2[-c(1:LONGLAG)]
  macd2macds3=macd2macds3[-c(1:LONGLAG)]
  slowk2slowd1=slowk2slowd1[-c(1:LONGLAG)]
  slowk2slowd2=slowk2slowd2[-c(1:LONGLAG)]
  slowk2slowd3=slowk2slowd3[-c(1:LONGLAG)]
  fastk2fastd1=fastk2fastd1[-c(1:LONGLAG)]
  fastk2fastd2=fastk2fastd2[-c(1:LONGLAG)]
  fastk2fastd3=fastk2fastd3[-c(1:LONGLAG)]
  pvi2smapvi=pvi2smapvi[-c(1:LONGLAG)]
  nvi2smanvi=nvi2smanvi[-c(1:LONGLAG)]
  
  bolTR1=bolTR1[-c(1:LONGLAG)]
  bolTR2=bolTR2[-c(1:LONGLAG)]
  bolTR3=bolTR3[-c(1:LONGLAG)]
  momTR1=momTR1[-c(1:LONGLAG)]
  momTR2=momTR2[-c(1:LONGLAG)]
  momTR3=momTR3[-c(1:LONGLAG)]
  accTR1=accTR1[-c(1:LONGLAG)]
  accTR2=accTR2[-c(1:LONGLAG)]
  accTR3=accTR3[-c(1:LONGLAG)]
  rosTR1=rocTR1[-c(1:LONGLAG)]
  rocTR2=rocTR2[-c(1:LONGLAG)]
  rocTR3=rocTR3[-c(1:LONGLAG)]
  macdTR1=macdTR1[-c(1:LONGLAG)]
  macdTR2=macdTR2[-c(1:LONGLAG)]
  macdTR3=macdTR3[-c(1:LONGLAG)]
  rsiTR1=rsiTR1[-c(1:LONGLAG)]
  rsiTR2=rsiTR2[-c(1:LONGLAG)]
  rsiTR3=rsiTR3[-c(1:LONGLAG)]
  fastTR1=fastTR1[-c(1:LONGLAG)]
  fastTR2=fastTR2[-c(1:LONGLAG)]
  fastTR3=fastTR3[-c(1:LONGLAG)]
  slowTR1=slowTR1[-c(1:LONGLAG)]
  slowTR2=slowTR2[-c(1:LONGLAG)]
  slowTR3=slowTR3[-c(1:LONGLAG)]
  willTR=willTR[-c(1:LONGLAG)]
  mfiTR=mfiTR[-c(1:LONGLAG)]
  pviTR=pviTR[-c(1:LONGLAG)]
  nviTR=nviTR[-c(1:LONGLAG)]
  
  choppedOpen<-assetData$Open[-c(1:LONGLAG)]
  choppedClose<-assetData$Close[-c(1:LONGLAG)]
  remoteDates<-index(assetData)[-c(1:LONGLAG)]
  tickerList<-rep(ticker,length(remoteDates))
  
  # create the target column
  target <- rep(NA,length(choppedOpen))
  counter <- 1
  for(i in choppedClose) {
    if(counter<length(choppedClose)) {
      if(i<=choppedClose[counter+1]) {
        target[counter]<- 1
      }
      else target[counter]<- -1
    }
    counter <- counter+1
  }
  
  len<-c((length(remoteEMA1)-1):length(remoteEMA1))
  
  training<-data.frame(remoteDates[c(2:(length(remoteDates)-1))],choppedOpen[c(2:(length(choppedOpen)-1))],
                       choppedClose[c(2:(length(choppedOpen)-1))],remoteEMA1[-len],remoteEMA2[-len],
                       remoteEMA3[-len],remoteSMA1[-len],remoteSMA2[-len],remoteSMA3[-len],remoteBBL1[-len],
                       remoteBBH1[-len],remoteBBL2[-len],remoteBBH2[-len],remoteBBL3[-len],remoteBBH3[-len],
                       remoteMOM1[-len],remoteMOM2[-len],remoteMOM3[-len],remoteACC1[-len],remoteACC2[-len],
                       remoteACC3[-len],remoteROC1[-len],remoteROC2[-len],remoteROC3[-len],remoteMACD1[-len],
                       remoteMACD2[-len],remoteMACD3[-len],remoteMACDS1[-len],remoteMACDS2[-len],
                       remoteMACDS3[-len],remoteRSI1[-len],remoteRSI2[-len],remoteRSI3[-len],
                       remoteFASTK1[-len],remoteFASTK2[-len],remoteFASTK3[-len],remoteFASTD1[-len],
                       remoteFASTD2[-len],remoteFASTD3[-len],remoteSLOWK1[-len],remoteSLOWK2[-len],
                       remoteSLOWK3[-len],remoteSLOWD1[-len],remoteSLOWD2[-len],remoteSLOWD3[-len],
                       remoteWILL[-len],remoteMFI[-len],remoteCHV[-len],remoteGKV[-len],remoteADL[-len],
                       remoteOBV[-len],remoteCHO[-len],remotePVI[-len],remoteNVI[-len],
                       ema2close[-len],close2bbh1[-len],close2bbh2[-len],
                       close2bbh3[-len],close2bbl1[-len],close2bbl2[-len],close2bbl3[-len],emamom1[-len],
                       emamom2[-len],emamom3[-len],mom2emamom1[-len],mom2emamom2[-len],mom2emamom3[-len], 
                       macd2macds1[-len],macd2macds2[-len],macd2macds3[-len],slowk2slowd1[-len],
                       slowk2slowd2[-len],slowk2slowd3[-len],fastk2fastd1[-len],fastk2fastd2[-len],
                       fastk2fastd3[-len],pvi2smapvi[-len],nvi2smanvi[-len],bolTR1[-len],bolTR2[-len],
                       bolTR3[-len],momTR1[-len],momTR2[-len],momTR3[-len],accTR1[-len],accTR2[-len],
                       accTR3[-len],rosTR1[-len],rocTR2[-len],rocTR3[-len],macdTR1[-len],macdTR2[-len],
                       macdTR3[-len],rsiTR1[-len],rsiTR2[-len],rsiTR3[-len],fastTR1[-len],fastTR2[-len],
                       fastTR3[-len],slowTR1[-len],slowTR2[-len],slowTR3[-len],willTR[-len],mfiTR[-len],
                       pviTR[-len],nviTR[-len],tickerList[-len],target[c(2:(length(remoteDates)-1))])
  
  colnames(training) <- c("date", "open","close", "ema1", "ema2", "ema3", "sma1","sma2","sma3","bbl1",
                          "bbh1","bbl2","bbh2","bbl3","bbh3","mom1","mom2","mom3","acc1","acc2","acc3",
                          "roc1","roc2","roc3","macd1","macd2","macd3","macds1","macds2","macds3","rsi1",
                          "rsi2","rsi3","fastk1","fastk2","fastk3","fastd1","fastd2","fastd3","slowk1",
                          "slowk2","slowk3","slowd1","slowd2","slowd3","will","mfi","chv","gkv","adl",
                          "obv","cho","pvi","nvi","ema2close","close2bbh1",
                          "close2bbh2","close2bbh3","close2bbl1","close2bbl2","close2bbl3","emamom1",
                          "emamom2","emamom3","mom2emamom1","mom2emamom2","mom2emamom3","macd2macds1",
                          "macd2macds2","macd2macds3","slowk2slowd1","slowk2slowd2","slowk2slowd3",
                          "fastk2fastd1","fastk2fastd2","fastk2fastd3","pvi2smapvi","nvi2smanvi",
                          "bolTR1","bolTR2","bolTR3","momTR1","momTR2","momTR3","accTR1","accTR2","accTR3",
                          "rocTR1","rocTR2","rocTR3","macdTR1","macdTR2","macdTR3","rsiTR1","rsiTR2",
                          "rsiTR3","fastTR1","fastTR2","fastTR3","slowTR1","slowTR2","slowTR3","willTR",
                          "mfiTR","pviTR","nviTR","ticker","target")
  
  # convert the datafram to an xts and then return it
  trainingXTS<- xts(training[,-1], order.by=training[,1])
  
#   # For bug check print to csv and inspect the table
#   varFilename=paste(START,END,ticker)
#   write.table(training, file=paste(varFilename, "csv", sep="."),quote=FALSE,sep=',',eol=';\n',
#               row.names=FALSE,col.names=TRUE)
  
  return(trainingXTS)
}
a<-0
