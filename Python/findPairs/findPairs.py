#!/usr/bin/env python
#-*- coding = utf-8 -*-

import sys
import os
import re

pairSetC        = {
    re.compile(r'^\s*#ifn?def\s+(\S+\s*)+$') : ( re.compile(r'^\s*#endif\s*(\s*//.*)?$'), r'endif'),
    re.compile(r'^\s*#if\s+(\S+\s*)+$')      : ( re.compile(r'^\s*#endif\s*(\s*//.*)?$'), r'endif')
                  }
pairSetMakefile = {
    re.compile(r'^\s*ifn?def\s+(\S+\s*)+$') : ( re.compile(r'^\s*endif\s*(\s*#.*)?$'), r'endif'),
    re.compile(r'^\s*ifn?eq\s+(\S+\s*)+$')  : ( re.compile(r'^\s*endif\s*(\s*#.*)?$'), r'endif'),
    re.compile(r'^\s*define\s+(\S+\s*)+$')  : ( re.compile(r'^\s*endef\s*(\s*#.*)?$'), r'define'),
                  }
pairSetShell    = {
    re.compile(r'^\s*(.*;)*\s*do(\s.*)?\s*$') : ( re.compile(r'^\s*(.*;)*\s*done\s*;?(\s.*)?$'), r'do'),
    re.compile(r'^\s*;?\s*case\s.+$')         : ( re.compile(r'^\s*;?\s*esac\s*$')             , r'case'),
    re.compile(r'^\s*;?\s*if\s.*$')           : ( re.compile('^\s*;?\s*fi\s*;?\s*$')           , r'if')
                  }

class FindPair():
    def __init__(self, fileName):
        self.fileName = fileName

    def identifyFile(self):
        if os.path.isfile(self.fileName):
            if re.compile(r'.+\.sh$').match(self.fileName):
                self.fileType = pairSetShell
            elif re.compile(r'^[Mm]akefile$').match(self.fileName) or re.compile(r'^MAKEFILE$').match(self.fileName) or re.compile(r'.+\.mk$').match(self.fileName):
                self.fileType = pairSetMakefile
            elif re.compile(r'.+\.(c|cc|cpp)').match(self.fileName):
                self.fileType = pairSetC
        else:
            print '%s is not a file' % self.fileName
            return None

    def findErrorPair(self):

        with open(self.fileName) as mFile:
            stack = []
            lineNum = 0
            nLineContent = []
            for line in mFile.readlines():
                lineNum += 1
                for key in self.fileType.keys():
                    if key.match(line):
                        stack.append(key)
                        nLineContent.append(str(lineNum) + ': ' + line)
                        print 'key   ' + str(lineNum) + ': ' + line
                        break
                    if self.fileType[key][0].match(line):
                        if len(stack) != 0 and self.fileType[stack[len(stack) - 1]][1] == self.fileType[key][1]:
                            stack.pop()
                            nLineContent.pop()
                            print 'value %d: %s' % (lineNum, line)
                            break
                        else:
                            print 'Error at:'
                            print 'Near here! %d: %s' % (lineNum, line)
                            return
            if len(stack) == 0:
                print 'No error pair was found!'
            else:
                for content in nLineContent:
                    print 'Error at:' 
                    print 'Near here! %s' % (content)



if __name__ == "__main__":
    if len(sys.argv) == 2:
        finder = FindPair(sys.argv[1])
        finder.identifyFile()
        finder.findErrorPair()
    else:
        print "Usage:"
        print "%s xxxx" % sys.argv[0]
