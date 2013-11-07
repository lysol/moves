"""\
This implements a command line interpreter (CLI) for the moves API.

OAuth data is kept in a JSON file, for easy portability between different
programming languages.

Currently, the initialization of OAuth requires the user to copy a URL
into a web browser, then copy the URL of the resulting page back to this
script.
"""

copyright = """
Copyright (c) 2013 Sam Denton <samwyse@gmail.com>
All Rights Reserved.

Licensed under the Academic Free License (AFL 3.0)
http://opensource.org/licenses/afl-3.0
"""

from cmd import Cmd as _Cmd
from pprint import pprint as _pprint
import json as _json

try:
    from moves import MovesClient
except ImportError:
    import sys
    from os.path import join, normpath
    # Try looking in the parent of this script's directory.
    sys.path.insert(0, normpath(join(sys.path[0], '..')))
    from moves import MovesClient
    

def _parse_line(f):
    import itertools
    from functools import wraps
    def partition(pred, iterable,
                  filter=itertools.ifilter,
                  filterfalse=itertools.ifilterfalse,
                  tee=itertools.tee):
        'Use a predicate to partition entries into false entries and true entries'
        t1, t2 = tee(iterable)
        return filterfalse(pred, t1), filter(pred, t2)

    @wraps(f)
    def wrapper(self, line):
        args, kwds = partition(
            lambda s: '=' in s,
            line.split())
        kwds = dict(item.split('=') for item in kwds)
        return f(self, *args, **kwds)
    return wrapper

class MovesCmd(_Cmd):

    cache_file = 'moves_cli.json'

    def default(self, line):
        '''Echos the arguments and exits the interpreter.'''
        print `argv`

    def do_quit(self, line):
        '''Exits the interpreter.'''
        return True

    def do_copyright(self, line):
        '''Displays copyright and licensing information.'''
        print copyright

    def do_client_id(self, line):
        '''Displays or sets the value.'''
        if line:
            self.mc.client_id = line
        elif self.mc.client_id:
            print 'client_id =', self.mc.client_id
        else:
            print 'The client id is not set.'

    def do_client_secret(self, line):
        '''Displays or sets the value.'''
        if line:
            self.mc.client_secret = line
        elif self.mc.client_secret:
            print 'client_secret =', self.mc.client_secret
        else:
            print 'The client secret is not set.'

    def do_access_token(self, line):
        '''Displays or sets the value.'''
        from urlparse import urlparse, parse_qs
        mc = self.mc
        if line:
            parts = urlparse(line)
            code = parse_qs(parts.query)['code'][0]
            mc.access_token = mc.get_oauth_token(code)
            mc.access_token = line
        elif mc.access_token:
            print 'access_token =', mc.access_token
        else:
            print 'The access token is not set.'
            print 'Enter the URL below in a web browser and follow the instructions.'
            print ' ', mc.build_oauth_url()
            print 'Once the web browser redirects, copy the complete URL and'
            print 'use it to re-run this command.'

    def do_load(self, filename):
        '''Loads the API state from a JSON file.'''
        if not filename:
            filename = self.cache_file
        with open(filename, 'rb') as fp:
            self.mc.__dict__.update(_json.load(fp))

    def do_save(self, filename):
        '''Saves the API state into a JSON file.'''
        if not filename:
            filename = self.cache_file
        with open(filename, 'wb') as fp:
            _json.dump(self.mc.__dict__, fp)

    @_parse_line
    def do_get(self, *path, **params):
        '''Issues an HTTP GET request
Syntax:
\tget path... [key=value]...
'''
        _pprint(self.mc.get('/'.join(path), **params))

    @_parse_line
    def do_post(self, *path, **params):
        '''Issues an HTTP POST request
Syntax:
\tpost path... [key=value]...
'''
        _pprint(self.mc.post('/'.join(path), **params))

    def do_tokeninfo(self, line):
        '''Displays information about the access token.'''
        _pprint(self.mc.tokeninfo())

    def do_examples(self, line):
        '''Displays example commands.'''
        print '''\
These are some commands to try.
 get user profile
 get user summary daily pastDays=7
 get user activities daily pastDays=5
 get user places daily pastDays=3
 get user storyline daily pastDays=2
'''

    def onecmd(self, line):
        try:
            return _Cmd.onecmd(self, line)
        except Exception as error:
            print "%s: %s" % (type(error).__name__, error)

    def preloop(self):
        self.mc = MovesClient()

def main(argv):
    MovesCmd().cmdloop()

if __name__ == '__main__':
    import sys
    main(sys.argv)
    
