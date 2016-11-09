#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Nianhua,Wei(veinian@163.com)

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

class MakeTables(object):
    '''
    convert xml table tree to python dic
    '''

    # DATATYPE:
    '''
    {
         table_name:  [
             (row_name, row_type, ...),
             (row_name, row_type, ...),
             (row_name, row_type, ...),
         ]
    }

    '''

    def __init__(self, table_name):
        self.table = []
        self.tname = table_name

    def add_row(self, row_name, row_type):
        self.tname.push([row_name, row_type])

    def make_table(self):
        print "class {0}(db.Model):".format(self.tname.title())

    def make_init_func(self):
        # fetch the cloumn name and join them my ','
        rows = ','.join(map(lambda x: x[0], self.table))
        print "    def __init__(self, {0}):".format(rows)
        for row in self.tname:
            print "        self.{0} = {0}"

    def make_row(self):
        for row in self.table:
            db_type = row[1]
            db_name = row[0]
            db_type_len = row[1] # if row has size
            print "    {0} = db.Column({1}({2}))".format(db_name, db_type, db_type_len)

    def make_repr_func(self):
        print "    def __repr__():"
        print "        pass"

    def dump(self):
        self.make_table()
        self.make_row()
        self.make_init_func()
        self.make_repr_func()

