#!/usr/bin/env python

import geoloc
import parse_groni
import time
import json

def get():
    results = []
    for c, result in enumerate(parse_groni.get()):
	coord = geoloc.get(result['address'], result['postcode'])
	result['longlat'] = coord
        results.append(result)
    	print c, result
	time.sleep(1)
    return results

if __name__ == '__main__':
    data = get()
    fd = open('regoff.json', 'w')
    fd.write(json.dumps(data))
    fd.close()
