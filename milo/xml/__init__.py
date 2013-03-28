#!/home/ivmedia/pyenv/ivmedia/bin/python

"""
Read XML text and return a list of dictionaries.
"""

import sys
import json
from xml.dom import minidom

__all__ = ('parse',)

def parse(xml, element_name):

    """
    Given an XML string and an element name, iterate
    through all children with that element name and 
    return a dictionary of that element's childred.

    Arguments:

        xml: string of XML
        element_name: XML element name containing items of interest

    Returns:
        list of dictionaries

    """

    tree = minidom.parseString(xml)

    items = []

    for rec in tree.getElementsByTagName(element_name):

        item = {}

        for child in rec.childNodes:
            try:
                item[child.nodeName] = child.firstChild.data
            except AttributeError:
                #skip children with no kids of their own
                pass

        items.append(item)

    return items

