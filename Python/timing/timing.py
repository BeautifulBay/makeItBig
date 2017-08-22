#!/usr/bin/env python
#-*- coding=utf-8 -*-

import sys
import os
import re

class lcdTiming():
    def __init__(self, mFile, kFile, uFile):
        self.mFile = mFile
        self.kFile = kFile
        self.uFile = uFile
        self.data = []

    def parseTimingFile(self):
        with open(self.mFile) as timingFile:
            for data in timingFile.readlines():
                data = data.strip();
                if data == '':
                    continue
                else:
                    if len(data) == 1:
                        data = '0' + data
                    self.data.append(data)
            self.data.append('00')

    def toKernel(self):
        print 'Kernel timing file:'
        print '[' + self.data[0],
        self.kData = '[' + self.data[0] + ' '
        for temp in self.data[1:-1]:
            self.kData = self.kData + temp + ' '
            print temp,
        self.kData = self.kData + self.data[-1] + '];'
        print self.data[-1] + ']'
        print

    def toBootloader(self):
        print 'Bootloader timing file:'
        self.uData = ''
        for temp in self.data[:-1]:
            self.uData = self.uData + '0x' + temp + ', '
            print '0x' + temp + ',',
        self.uData = self.uData + '0x' + self.data[-1]
        print '0x' + self.data[-1]
        print

    def modifyKernel(self):
        #print self.kFile
        #print self.kData
        #print
        #Function one
        #command = 'sed -i \'s/^\(\s*qcom,mdss-dsi-panel-timings\s*=\s*\).*$/\\1%s/ \' %s' % (self.kData, self.kFile)
        #os.popen(command)
        #Function two
        wkernelFile = open(self.kFile + 'temp', 'w')
        with open(self.kFile, 'r') as rkernelFile:
            for line in rkernelFile:
                message = re.compile('\s*qcom,mdss-dsi-panel-timings\s*=\s*(.*)').match(line)
                if message:
                    wkernelFile.writelines(line.replace(message.group(1), self.kData))
                    print 'From\n%s\nchange to\n%s\n' % (message.group(1), self.kData)
                    wkernelFile.flush()
                    continue
                wkernelFile.writelines(line)
                wkernelFile.flush()
        wkernelFile.close()
        os.rename(self.kFile + 'temp', self.kFile)

    def modifyBootloader(self):
        #print self.uFile
        #print self.uData
        #print
        #Function one
        #command = 'sed -i \'/.*_timings\[.*/{N;s/\(.*_timings\[.*\)\\n\(\s*\).*/\\1\\n\\2%s/}\' %s' % (self.uData, self.uFile)
        #os.popen(command)
        #Function two
        flag = 0
        wubootloaderFile = open(self.uFile + 'temp', 'w')
        with open(self.uFile, 'r') as ubootloaderFile:
            for line in ubootloaderFile:
                if re.compile('.*_timings\[.*').match(line):
                    data = next(ubootloaderFile)
                    print 'From\n%s\nchange to\n%s\n' % (data.strip(), self.uData.strip())
                    flag = 1
                wubootloaderFile.writelines(line)
                if flag == 1:
                    wubootloaderFile.writelines(data.replace(data.strip(), self.uData))
                    flag = 0
                wubootloaderFile.flush()
        wubootloaderFile.close()
        os.rename(self.uFile + 'temp', self.uFile)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        kFile = None
        uFile = None
    elif len(sys.argv) == 3:
        kFile = sys.argv[2]
        uFile = None
    elif len(sys.argv) >= 4:
        kFile = sys.argv[2]
        uFile = sys.argv[3]
    else:
        print '\033[31mUsage: lcdTiming timingFile kernelFile bootloaderFile\033[0m'
        print '\033[31mYou need three files\033[0m'
        sys.exit()
    
    if not os.path.isfile(sys.argv[1]):
        print '\033[31mCan not find %s\033[0m' % sys.argv[1]
        sys.exit()
    operator = lcdTiming(sys.argv[1], kFile, uFile)
    operator.parseTimingFile()
    operator.toKernel()
    if kFile != None:
        if not re.compile('^.*\.dtsi$').match(kFile):
            print '\033[31m%s is not a xxx.dtsi file for kernel\033[0m' % kFile
        if not os.path.isfile(kFile):
            print '\033[31mCan not find %s\033[0m' % kFile
        else:
            operator.modifyKernel()
    operator.toBootloader()
    if uFile != None:
        if not re.compile('^.*\.h$').match(uFile):
            print '\033[31m%s is not a xxx.h file for bootloader\033[0m' % uFile
        if not os.path.isfile(uFile):
            print '\033[31mCan not find %s\033[0m' % uFile
        else:
            operator.modifyBootloader()

