#!/usr/bin/env python
# -*- coding = utf-8 -*-

import os
import sys
import re
import chardet

reload(sys)
sys.setdefaultencoding('utf-8')

class ParseSubtitle():
    def __init__(self, subtitle, savefile):
        self.subtitle = subtitle
        self.savefile1 = savefile
        self.savefile2 = os.path.splitext(savefile)[0] + '_en_cn' + os.path.splitext(savefile)[1]
        self.savefile3 = os.path.splitext(savefile)[0] + '_en' + os.path.splitext(savefile)[1]
        self.savefile4 = os.path.splitext(savefile)[0] + '_cn' + os.path.splitext(savefile)[1]

        mfile = open(subtitle, 'r')
        temp = mfile.read()

        self.encode = chardet.detect(temp)['encoding'].lower()

        print self.encode
        if self.encode != 'utf-8':
            # class inner function is called by inner function
            self.transferFileEncode(self.subtitle, self.encode, 'utf-8')

    def transferFileEncode(self, filePath, fromCode, toCode):
        rFile = open(filePath, 'r');
        lines = rFile.read()
        rFile.close()

        wFile = open(filePath, 'w')
        if fromCode == 'gb2312':
            lines = lines.decode('gbk')
        else:
            lines = lines.decode(fromCode)
        lines.encode(toCode)
        wFile.write(lines)
        wFile.close()

    def parseType(self):
        match = re.compile(".*\.([Aa][Ss][Ss]|[Ss][Rr][Tt])$").match(self.subtitle)
        print "%s %s" % (match.group(0), match.group(1))
        if match.group(1).lower() == "ass":
            self.genre = "parseASS"
        elif match.group(1).lower() == "srt":
            self.genre = "parseSRT"
        else:
            self.genre = None


    def parseSubtitle(self):
        def parseASS(self):
            with open(self.subtitle, 'r') as mFile:
                with open(self.savefile1, 'w') as sFile1:
                    with open(self.savefile2, 'w') as sFile2:
                        with open(self.savefile3, 'w') as sFile3:
                            with open(self.savefile4, 'w') as sFile4:
                                for line in mFile.readlines():
                                    # filter out the real subtitle line
                                    # what it needs to be included
                                    if re.compile(r'\\N').search(line) == None:
                                        continue
                                    # what it doesn't need to be included
                                    if re.search(r'{\\an|{\\fad', line):
                                        continue
                                    # split out the real subtitle message
                                    reGetMain = line.split(',', 9)
                                    if re.search(r'\\N', reGetMain[9]) == None:
                                        continue
                                    if len(reGetMain) >= 10 and reGetMain[9].strip() != '':
                                    # } replace N then use } split
                                        reGetMain = re.split(r'}', re.subn('N', '}', reGetMain[9], 1)[0])
                                        if re.search(r'{', reGetMain[0]):
                                            continue
                                        #print "%-60s %s\n" % (reGetMain[-1].strip(), ','.join(reGetMain[0].strip().split()).replace('\\', '', 1))
                                        sFile1.write("%-60s %s\n" % (reGetMain[-1].strip(), ','.join(reGetMain[0].strip().split()).replace('\\', '', 1)))
                                        sFile2.write("%s\n%s\n" % (reGetMain[-1].strip(), ','.join(reGetMain[0].strip().split()).replace('\\', '', 1)))
                                        sFile3.write("%s\n" % (reGetMain[-1].strip()))
                                        sFile4.write("%s\n" % (','.join(reGetMain[0].strip().split()).replace('\\', '', 1)))

        def parseSRT(self):
            with open(self.subtitle, 'r') as mFile:
                with open(self.savefile1, 'w') as sFile1:
                    with open(self.savefile2, 'w') as sFile2:
                        with open(self.savefile3, 'w') as sFile3:
                            with open(self.savefile4, 'w') as sFile4:
                                dataList = []
                                mList = []
                                for line in mFile.readlines():
                                    if re.compile(r'^[0-9]+$').match(line.strip()):
                                        if len(mList):
                                            dataList.append(mList)
                                            mList = []
                                    if line.strip():
                                        mList.append(line.strip())
                                        continue
                                if len(mList):
                                    dataList.append(mList)
                                    mList = []
                                for data in dataList:
                                    #print '%s' % data
                                    if len(data) != 4:
                                        continue
                                    if re.compile(r'{\\pos').search(data[2]):
                                        continue
                                    if re.compile(r'{\\an').search(data[2]):
                                        continue
                                    #print "%-60s %s" % (data[3], ','.join(data[2].split()))
                                    sFile1.write("%-60s %s\n" % (data[3], ','.join(data[2].split())))
                                    sFile2.write("%s\n%s\n" % (data[3], ','.join(data[2].split())))
                                    sFile3.write("%s\n" % (data[3]))
                                    sFile4.write("%s\n" % (','.join(data[2].split())))

        # function of function is called
        if self.genre == "parseASS":
            parseASS(self)
        elif self.genre == "parseSRT":
            parseSRT(self)
        else:
            print "%s can not be parsed" % self.subtitle

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: %s xxx.ass/xxx.srt savefile" % sys.argv[0]
        sys.exit()
    item = ParseSubtitle(sys.argv[1], sys.argv[2])
    item.parseType()
    item.parseSubtitle()
