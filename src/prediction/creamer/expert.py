'''
Created on Dec 5, 2012

@author: Ash Booth
'''

class Expert(object):
    '''
    classdocs
    '''


    def __init__(self, module, time, next_in, first):
        '''
        Constructor
        '''
        self.module = module
        self.born_at = time
        self.next_ariving_at = time+next_in
        self.first = first
        self.cummulative_return = 0.0
        self.initial_weight = None
        self.weight = None
        
        