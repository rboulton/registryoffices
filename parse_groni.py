#!/usr/bin/env python

import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
import sys
import re
import urllib
import urllib2

try:
    import simplejson as json
except ImportError:
    import json

nameend_re = re.compile(',\s*$')
address_re = re.compile(',\s*')
postcode_re = re.compile('\.\s*$')

def parse(data):
    soup = BeautifulSoup.BeautifulSoup(data,
        convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
    data = []
    for tag in soup.findAll('strong'):
        name = tag.string
        tag = tag.parent
        name = nameend_re.sub('', name)
        tags = tag.findNextSiblings('p', limit=4)
        tag = [tag.string for tag in tags]
        address = address_re.split(tag[0])
        postcode = address[-1]
        address = ', '.join(address[:-1])
        postcode = postcode_re.sub('', postcode)
        telephone = tag[1]
        hours = tag[2]
        email = tag[3]

        data.append({
            'name': name,
            'address': address,
            'postcode': postcode,
            'telephone': telephone,
            'hours': hours,
            'email': email,
        })
    return data

def get():
    url = 'http://www.groni.gov.uk/index/district-registrars-offices.htm'
    rawdata = urllib2.urlopen(url).read().decode('latin1')
    return parse(rawdata)

if __name__ == '__main__':
    data = get()
    fd = open('groni.json', 'w')
    fd.write(json.dumps(data))
    fd.close()
