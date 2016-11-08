#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Nianhua,Wei(willian.wnh@gmail.com)

'''
read database schema from xml file, and dump it to sqlqlchemy models.py
'''

import xml.etree.ElementTree as ET
import sys
import os

if len(sys.argv) == 2:
    xml_file = sys.argv[1]
else:
    print "usage: {0} db.xml".format(sys.argv[0])
    sys.exit(1)

if not os.path.isfile(xml_file):
    print "{0} not exists".format(xml_file)
    sys.exit(2)

tree = ET.parse(xml_file)

for elem in tree.iter(tag='table'):
    for sub_elem in elem.iter(tag='row'):
        print sub_elem.get('name')
        for child in sub_elem.iter(tag='datatype'):
            if 'INT' in child.text:
                print "INTEGER"
            else:
                print child.text

        for child in sub_elem.iter(tag='default'):
            print "default value: {0}".format(child.text)

class MakeModels(object):
    '''
    class generate python flask models file
    '''

    def __init__(self):
        pass

    def make_init_func(self):
        pass

    def add_elem(self):
        pass

    def dump(self):
        pass

    def make_repr_func(self):
        pass






# TODO: parse tree data, convert it to python code










