#!/usr/bin/env python2.7
import sys
import lispy

if len(sys.argv) > 1:
    filename = str(sys.argv[1])
    lispy.load(filename)
else:
    lispy.repl()
