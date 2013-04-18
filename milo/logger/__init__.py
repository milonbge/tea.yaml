#!/usr/bin/env python

"""
Logging convenience stuff.
"""

import logging
import os
import sys
from datetime import datetime

def get_logger(name='some script'):

    """ 
    return a logger that prints to the screen if it's
    interactive and a file if not
    """

    #timestamp for filename 
    timestamp = datetime.now().strftime('%Y-%m-%d')

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    #custom formatter
    formatter = logging.Formatter(
        '%(asctime)s %(name)s %(levelname)s %(filename)s '
        '%(funcName)s line: %(lineno)s: %(msg)s'
    )
    handler = logging.FileHandler('/tmp/scripts_{0}.log'.format(timestamp))
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    #print to stdout if it's interactive, but file-only if not
    if sys.stdin.isatty():
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger
