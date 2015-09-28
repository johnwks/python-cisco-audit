#!/usr/bin/env python

import sys
import getopt
from ciscoconfparse import CiscoConfParse
import re


def usage() :
    print 'Usage:\n\t', sys.argv[0], '-c audit-config-file device-config-file\n'

cfgfile = None

try :
    opts, args = getopt.getopt(sys.argv[1:], 'c:')
except getopt.GetoptError :
    usage()
    sys.exit(2)

for opt, arg in opts :
    if opt in ('-c') :
        cfgfile = arg
    else :
        usage()
        sys.exit(2)

if (cfgfile == None) or (len(args) != 1) :
    usage()
    sys.exit(2)

infile = args[0]

try :
    cf = open(cfgfile, 'r')
except IOError :
    print 'error opening audit-config-file'
    sys.exit(2)

try :
    inf = open(infile, 'r')
except IOError :
    print 'error opening device-config-file'
    sys.exit(2)
inf.close()

parse = CiscoConfParse(infile)

line = cf.readline()

while line :
    line = line.rstrip('\r\n')
    if re.search(r'^#', line) :
        pass
    elif re.match(r'^\s*$', line) :
        pass
    elif re.search(r'^\[', line) :
        chunkName = re.sub(r'[\[\]]', '', line)
        line = cf.readline()
        line = line.rstrip('\r\n')
        linespec = line
        line = cf.readline()
        line = line.rstrip('\r\n')
        req = []
        while line :
            if re.search(r'^#', line) :
                pass
            elif re.match(r'^\s*$', line) :
                pass
            else :
                req.append(line);
            line = cf.readline()
            line = line.rstrip('\r\n')
        diffs = parse.sync_diff(req, linespec)
        print '!!! Auditing', chunkName
        for i in diffs :
            print i
    else :
        pass

    line = cf.readline()

cf.close()
