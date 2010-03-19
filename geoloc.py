#!/usr/bin/env python

import urllib
import urllib2
import simplejson
import private_passwords

def fetch(url, params):
    url += '?' + urllib.urlencode(params)
    result = urllib2.urlopen(url).read()
    json = simplejson.loads(result)
    return json
                 
def get_loc(location):
    """Get the (longitude, latitude) for a postcode.

    """
    url = "http://maps.google.com/maps/geo"
    if not location.lower().endswith('uk'):
        location += ', UK'
    params = {
        'q': location,
        'output': 'json',
        'sensor': 'false',
        'key': private_passwords.GOOGLE_MAPS_KEY,
    }
    location = fetch(url, params)
    status = location["Status"]["code"]
    if status != 200:
        return None, None
    try:
        country_code = location["Placemark"][0]["AddressDetails"]["Country"]["CountryNameCode"]
        if country_code != "GB":
	    return None, None
    except KeyError:
        pass
    longitude, latitude, height = location["Placemark"][0]["Point"]["coordinates"]
    if longitude is None:
        return None, None
    return str(longitude), str(latitude)   

def get(loc1, loc2=None):
    loc = get_loc(loc1)
    if loc[0] is None:
        if loc2 is not None:
            loc = get_loc(loc2)
    return loc

if __name__ == '__main__':
    print get('cb224qn')
    print get('58 Kingsway, Duxford')
