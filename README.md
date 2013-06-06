moves
=====

This is a Python client library for the [Moves App](http://www.moves-app.com/).

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

License
-------

(The MIT License)

Copyright (c) 2013 Derek Arnold <derek@derekarnold.net>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the 'Software'), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
