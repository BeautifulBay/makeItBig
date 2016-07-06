#!/usr/bin/env python
#-*- coding = utf-8 -*-

import sys
import os
import re
from collections import OrderedDict

class PareseDts():
    def __init__(self, path):
        self.result = []
        self.data = OrderedDict()
        self.count = 0
        self.separator = '\t'
        self.originalPath = path
        self.path = os.path.split(path)[0]
        if len(self.path) != 0:
            self.path += '/'

    def getInclude(self, path):
        self.count += 1
        tempResult = []
        tempSeparator = ""
        try:
            with open(path) as dtsFile:
                for data in dtsFile.readlines():
                    temp = re.match(r'\s*#include\s*\"\s*(\S*\.dtsi?)\s*\"', data)
                    if temp != None:
                        for i in range(0, self.count, 1):
                            tempSeparator = tempSeparator + self.separator
                        self.data[self.path + temp.group(1)] = tempSeparator
                        tempSeparator = ""
                        self.getInclude(self.path + temp.group(1))
                    else:
                        temp = re.match(r'\s*/\s*include\s*/\s*\"\s*(\S*\.dtsi?)\s*\"', data)
                        if temp != None:
                            for i in range(0, self.count, 1):
                                tempSeparator = tempSeparator + self.separator
                            self.data[self.path + temp.group(1)] = tempSeparator
                            tempSeparator = ""
                            self.getInclude(self.path + temp.group(1))
        except IOError:
            for i in range(0, self.count - 1, 1):
                tempSeparator = tempSeparator + self.separator
            self.data.popitem()
            self.data['%s #No such a file' % path] = tempSeparator
        self.count -= 1
    
    def printInclude(self):
        print self.originalPath
        for key in self.data.keys():
                print key
        print 
    
    def printData(self):
        print self.originalPath
        for key in self.data.keys():
            print self.data[key], key
        print 

if __name__ == "__main__":
    if len(sys.argv) == 2:
        if not os.path.isfile(sys.argv[1]):
            print 
            print "%s doesn't exist!" % sys.argv[1]
            print 
            sys.exit()
        operator = PareseDts(sys.argv[1])
        operator.getInclude(sys.argv[1])
        #operator.printInclude()
        operator.printData()
    else:
        print '#Error#'
        print 'Usage:'
        print sys.argv[0], 'xxx.dts[i]'
