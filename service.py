#!/usr/bin/env python

import wsgiwapi
import search

@wsgiwapi.jsonreturning
@wsgiwapi.allow_GETHEAD
@wsgiwapi.param("loc", 1, 1, None, None,
                "The location to search for registry offices near.")
def find_registry(request):
    loc = request.GET['loc']
    res = search.search('regoff.db', loc[0])
    return res

def main():
    app = wsgiwapi.make_application({
        'registries': find_registry,
    }, autodoc='doc')

    server = wsgiwapi.make_server(app, ('0.0.0.0', 10010))
    try:
	server.start()
    except KeyboardInterrupt:
	server.stop()

if __name__ == '__main__':
    main()
