#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Nianhua,Wei(willian.wnh@gmail.com)

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

print tree










