#!/usr/bin/env python

import xappy
import json
import geoloc

def search(indexpath, loc1, loc2=None):
    loc = geoloc.get(loc1, loc2)
    if loc[0] is None:
        return None
    loc = loc[1] + " " + loc[0]
    conn = xappy.SearchConnection(indexpath)
    results = []
    for result in conn.query_distance('location', loc).search(0, 10):
        data = json.loads(result.data['data'][0])
        dm = float(result.get_distance('location', loc)) / 1609.344
        data['dist_miles'] = "%.1f" % dm
        results.append(data)
    return results

if __name__ == '__main__':
    print search('regoff.db', "BT23")
