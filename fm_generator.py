#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Nianhua,Wei(veinian@163.com)

'''
read database schema from xml file, and dump it to sqlqlchemy models.py
'''

from __future__ import print_function
import xml.etree.ElementTree as ET
import sys
import os
import re

# TODO: sqlalchemy datatype map to sql datatype

mysql_to_sqlalchemy =  {
    'BOOL': 'Bollean',
    'BOOLEAN': 'Boolean',
    'SMALLINT': 'SmallInteger',
    'INTEGER': 'Integer',
    'BIGINT': 'BigInteger',
    'ENUM': 'Enum',
    'DECIMAL': 'Numeric',
    'FLOAT': 'Float',
    'DATE': 'Date',
    'DATETIME': 'Datetime',
    'TIMESTAMP': 'Datetime',
    'VARCHAR': 'String',
    'CHAR': 'String',
    'TEXT': 'Text',
}

def fm_maker(xmlfile):
    tree = ET.parse(xmlfile)

    for elem in tree.iter(tag='table'):
#       print(elem.attrib['name'])
        new_table = MakeTables(elem.attrib['name'])
        (row_type, row_default, row_size) = ('', '', '')
        for sub_elem in elem.iter(tag='row'):
#            print(sub_elem.get('name'), end=" ")
            row_name = sub_elem.attrib['name']
            for child in sub_elem.iter(tag='datatype'):
#                print(child.text, end=" ")
                row_type = child.text

            for child in sub_elem.iter(tag='default'):
#                print(child.text)
                row_default = child.text
            new_table.add_row(row_name, row_type, row_default, 0)

        new_table.dump()

class MakeTables(object):
    '''
    convert xml table tree to python dic
    '''

    # DATATYPE:
    '''
    {
         table_name:  [
             row_name: {
                  type: INTEGER(VARCHAR),
                  default: xxx,
                  primary: true/false,
                  auto_incremetn: true/false,
             },
             row_name: {
                  type: INTEGER(VARCHAR),
                  default: xxx,
                  primary: true/false,
                  auto_incremetn: true/false,
             },
         ]
    }

    '''

    def __init__(self, table_name):
        self.table = {}
        self.tname = table_name

    def add_row(self, row_name, row_type, default, primary=False, auto_inc=False):
        self.table[row_name] = {}
        self.table[row_name]['type'] = row_type
        self.table[row_name]['default'] = default
        self.table[row_name]['primary'] = primary
        self.table[row_name]['auto_increment'] = auto_inc

    def make_table(self):
        print("class {0}(db.Model):".format(self.tname.title()))
        print()

    def make_init_func(self):
        # fetch the cloumn name and join them my ','
        rows = ','.join(self.table.keys())
        print("    def __init__(self, {0}):".format(rows))
        for row in self.table.keys():
            print("        self.{0} = {1}".format(row, row))

        print()

    def make_row(self):
        for (row_name, items) in self.table.items():
            s_type = re.match(r'^([a-zA-Z]+)', items['type'])
            try:
                p_type = items['type'].replace(s_type.group(), mysql_to_sqlalchemy[s_type.group()])
            except Exception as err:
                p_type = items['type']
            finally:
                print("    {0} = db.Column(db.{1})".format(row_name, p_type))

        print()

    def make_repr_func(self):
        print("    def __repr__():")
        print("        pass")
        print()

    def dump(self):
        self.make_table()
        self.make_row()
        self.make_init_func()
        self.make_repr_func()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        xml_file = sys.argv[1]
    else:
        print("usage: {0} db.xml".format(sys.argv[0]))
        sys.exit(1)

    if not os.path.isfile(xml_file):
        print("{0} not exists".format(xml_file))
        sys.exit(2)

    fm_maker(xml_file)



