#!/usr/bin/env python

import sys
import csv
import re

try:
    import simplejson as json
except ImportError:
    import json

mapping = {
    'Title': 'name',
    'Address1': 'address',
    'Address2': 'address',
    'Address3': 'address',
    'Postcode': 'postcode',
    'URL': 'url',
}

name_re = re.compile(' - Register Office')

def get():
    file = 'sourcedata/GRO Offices Data.csv'
    fd = open(file)
    result = []
    cols = None
    for row in csv.reader(fd.readlines()):
        if cols is None:
            cols = row
            continue
        data = {}
        for col, val in zip(cols, row):
            col = mapping.get(col, col)
            val = name_re.sub('', val)
            if col in data:
                data[col] += ', ' + val
            else:
                data[col] = val
        result.append(data)
    return result

if __name__ == '__main__':
    data = get()
    fd = open('groenwales.json', 'w')
    fd.write(json.dumps(data))
    fd.close()
