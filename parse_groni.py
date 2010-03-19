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
email_re = re.compile('email:\s*')
tel_re = re.compile('Tel:\s*([0-9 /]+)')
fax_re = re.compile('Fax:\s*([0-9 /]+)')

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
        vals = {}

        vals['name'] = name
        address = address_re.split(tag[0])
        postcodebits = postcode_re.sub('', address[-1]).split()
        address = address[:-1]
        if len(postcodebits) > 2:
            address.append(' '.join(postcodebits[:-2]))
            postcodebits = postcodebits[-2:]
        vals['postcode'] = ' '.join(postcodebits)
        vals['address'] = ', '.join(address)
        telephone = tag[1]
        tel_mo = tel_re.search(telephone)
        if tel_mo:
            vals['tel'] = tel_mo.group(1).strip()
        fax_mo = fax_re.search(telephone)
        if fax_mo:
            vals['fax'] = fax_mo.group(1).strip()
        vals['hours'] = tag[2]
        vals['email'] = email_re.sub('', tag[3])

        data.append(vals)
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
