'''
Created on Dec 3, 2012

@author: Ash Booth
'''
import numpy
 

#TICKERS = ["ADBE US Equity"]
#TICKERS = ["AAPL US Equity", "GOOG US Equity", "ADBE US Equity", "COST US Equity", "DELL US Equity", "VOD US Equity", "YHOO US Equity", "TXN US Equity"]
#TICKERS = numpy.array(TICKERS)

#BUY = 1
#SELL = -1
#HOLD = 0

EMAn1 = 10
EMAn2 = 16
EMAn3 = 22
SMAn1 = 10
SMAn2 = 16
SMAn3 = 22
BOLn1 = 20
BOLn2 = 26
BOLn3 = 32
MOMn1 = 12
MOMn2 = 18
MOMn3 = 24
ROCn1 = 10
ROCn2 = 16
ROCn3 = 22
MACDs = 12
MACDf1 = 18
MACDf2 = 24
MACDf3 = 30
MACDn = 9
RSIn1 = 8
RSIn2 = 14
RSIn3 = 20
FASTKn1 = 12 
FASTKn2 = 18
FASTKn3 = 24
FASTDn = 3
CHVn = 10
CHOs = 3
CHOf = 10

def copy_file(path):
    '''copy_file(string)

    Import the needed functions.
    Assert that the path is a file.
    Return all file data.'''
    from os.path import basename, isfile
    assert isfile(path)
    return (basename(path), file(path, 'rb', 0).read())

def paste_file(file_object, path):
    '''paste_file(tuple, string)

    Import needed functions.
    Assert that the path is a directory.
    Create all file data.'''
    from os.path import isdir, join
    assert isdir(path)
    file(join(path, file_object[0]), 'wb', 0).write(file_object[1])
