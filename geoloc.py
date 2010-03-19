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
                 
def get(location):
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
    country_code = location["Placemark"][0]["AddressDetails"]["Country"]["CountryNameCode"]
    if country_code != "GB":
	return None, None
    longitude, latitude, height = location["Placemark"][0]["Point"]["coordinates"]
    return str(longitude), str(latitude)   

if __name__ == '__main__':
    print get_geolocation('cb224qn')
    print get_geolocation('58 Kingsway, Duxford')
