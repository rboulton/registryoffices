#!/usr/bin/env python

import xappy
try:
    import simplejson as json
except ImportError:
    import json

def build(indexpath, jsonpath):
    conn = xappy.IndexerConnection(indexpath)
    conn.add_field_action('location', xappy.FieldActions.GEOLOCATION)
    conn.add_field_action('data', xappy.FieldActions.STORE_CONTENT)
    data = json.loads(open(jsonpath).read())
    for item in data:
        doc = xappy.UnprocessedDocument()
        doc.id = item['name']
        doc.append('location', item['longlat'][1] + ' ' + item['longlat'][0])
        doc.append('data', json.dumps(item))
        conn.replace(doc)
    conn.flush()

if __name__ == '__main__':
    build('regoff.db', 'regoff.json')
