#!/usr/bin/env python

"""
Print the output of cProfile.

Sort options from here:
http://docs.python.org/2/library/profile.html#module-pstats

    Valid Arg   Meaning
    'calls' call count
    'cumulative'    cumulative time
    'cumtime'   cumulative time
    'file'  file name
    'filename'  file name
    'module'    file name
    'ncalls'    call count
    'pcalls'    primitive call count
    'line'  line number
    'name'  function name
    'nfl'   name/file/line
    'stdname'   standard name
    'time'  internal time
    'tottime'   internal time

"""

import sys
import pstats


try:
    sort_by = sys.argv[2]
except IndexError:
    sort_by = 'cumulative'

stats = pstats.Stats(sys.argv[1])

try:
    stats.sort_stats(sort_by).print_stats(.5)
except IOError:
    #avoid errors when piping output to 'head'
    pass
