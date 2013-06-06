moves
=====

Requirements
------------

* [Requests](http://docs.python-requests.org/en/latest/)

Installation
------------

Install via pip:

    pip install moves

Usage
-----

See `examples/oauth.py` for some basic examples.

You can request API endpoints like so:

    moves.api('/user/profile', 'GET', params={'access_token': access_token})

Or

    moves.get('/user/profile', params={'access_token': access_token})

Or just

    moves.user_profile(access_token=access_token)

For endpoints that require RESTful parameters in the URL, such as `/user/summary/daily/<YYYYMMDD>`

    moves.user_summary_daily('20130605', access_token=access_token)

All responses are decoded JSON objects.

Consult the [API documentation](https://dev.moves-app.com/docs/api) for the methods supported.

Disclaimer
----------

This library uses data from Moves but is not endorsed or certified by Moves. Moves is a trademark of ProtoGeo Oy.
