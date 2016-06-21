#!/usr/bin/env python
#-*- coding = utf-8 -*-

import os
import re
import time
import sys

class GetGitLog():
    def __init__(self):
        pass

    def getLog(self):
        self.fullLogFile = os.popen('git log')
	
    def parseSaveLog(self):
        self.logList = []

        y = 0
        flag = 0
        tempList = []
        for line in self.fullLogFile.readlines():
            #add index and commit HEAD
            temp = re.match(r'^commit\s((\d?\w?)+)$', line)
            if temp != None:
                tempList.append(str(y+1))
                tempList.append(temp.group(1)[0:7])
                flag = 0
                continue
            #use the flag to filter out the first commit you want
            if flag == 1:
                continue
            #add author
            temp = re.match(r'^Author:\s(.*)\s<.*$', line)
            if temp != None:
                tempList.append(temp.group(1))
                continue
            #add date and time
            temp = re.match(r'^Date:\s+(.*)\s*\+', line)
            if temp != None:
                tempList.append(time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(temp.group(1).strip(),'%a %b %d %H:%M:%S %Y')))
            #pass \s* line
            temp = re.match(r'^\s*$', line)
            if temp != None:
                continue
            #add commit
            temp = re.match(r'^\s{4}\s*(.*)\s*', line)
            if temp != None:
                tempList.append(temp.group(1))
                self.logList.append(tempList)
                y += 1
                flag = 1
                tempList = []
                
    def printStatus(self):
        print 'index   content\n'
        for x in self.logList:
            print '%5s %15s %s %s' % (x[0], x[2], x[3], x[4]),
            print
	
    def checkGitDir(self):
        if len(self.logList):
            return True
        else:
            print
            print '#####################################################'
            print 'Check current directroy, can not find git repository!'
            print '#####################################################'
            print 
            return None

    def printSelectMenu(self):
        os.system('clear')
        self.printStatus()
        while True:
            print '######################'
            print '#q  : quit           #'
            print '#u  : update menu    #'
            print '#n  : git diff n     #'
            print '#n n: git diff n n   #'
            print '######################'
            choice = raw_input('Please select input :')
            if choice == 'q':
                print 'Exit!!'
                break
            elif choice == 'u':
                os.system('clear')
                self.printStatus()
                continue
            else:
                temp = re.match(r'^\s*([0-9]+)\s+([0-9]+)\s*$', choice)
                if temp != None:
                    num1 = self.parseInput(temp.group(1))
                    num2 = self.parseInput(temp.group(2))
                    if num1 != None and num2 != None:
                        os.system('git diff %s %s' % (num1, num2))
                    else:
                        print '%s or %s is over the border' % (temp.group(1), temp.group(2))
                    raw_input("Do anything to return:")
                else:
                    temp = re.match(r'^\s*(\d+)\s*$', choice)
                    if temp != None:
                        num1 = self.parseInput(temp.group(1))
                        num2 = self.parseInput(str(int(temp.group(1)) + 1))
                        if num1 != None and num2 != None:
                            os.system('git diff %s %s' % (num1, num2))
                        else:
                            print '%s is over the border' % (temp.group(1))
                        raw_input("Do anything to return:")
                    else:
                        print 'Input is irregular!!'
                        raw_input("Do anything to return:")

    def parseInput(self, num):
        for x in self.logList:
            if x[0] == num:
                return x[1]
            else:
                continue
        return None

if __name__ == "__main__":
    operator = GetGitLog()
    operator.getLog()
    operator.parseSaveLog()
    if operator.checkGitDir() == None:
        sys.exit()
    operator.printSelectMenu()
