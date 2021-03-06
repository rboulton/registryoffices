#!/usr/bin/env python

import geoloc
import parse_groni
import parse_groenwales
try:
    import simplejson as json
except ImportError:
    import json

def parseall():
    for item in parse_groni.get():
        yield item
    for item in parse_groenwales.get():
        yield item

def get():
    results = []
    for c, result in enumerate(parseall()):
	coord = geoloc.get(result['address'], result['postcode'])
	result['longlat'] = coord
        results.append(result)
    	print c, result
    return results

if __name__ == '__main__':
    data = get()
    fd = open('regoff.json', 'w')
    fd.write(json.dumps(data, indent=True))
    fd.close()
