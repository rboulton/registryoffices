#!/usr/bin/env python

import wsgiwapi
import search

@wsgiwapi.jsonreturning
@wsgiwapi.allow_GETHEAD
def find_registry(request):
    loc = request.GET['location']
    res = search.search('regoff.db', loc[0])
    return res

def main():
    app = wsgiwapi.make_application({
        'registry/find': find_registry,
    })

    server = wsgiwapi.make_server(app, ('0.0.0.0', 8080))
    try:
	server.start()
    except KeyboardInterrupt:
	server.stop()

if __name__ == '__main__':
    main()
