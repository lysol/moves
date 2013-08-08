"""\
This implements a command line interpreter (CLI) for the moves API.

OAuth data is kept in a JSON file, for easy portability between different
programming languages.

Currently, the initialization of OAuth requires the user to copy a URL
into a web browser, then copy the URL of the resulting page back to this
script.
"""

from cmd import Cmd as _Cmd
from pprint import pprint as _pprint
import itertools as _itertools
import json as _json

try:
    from moves import MovesClient
except ImportError:
    import sys
    sys.path.insert(0, '..')
    from moves import MovesClient
    
##    class MovesClient(object):
##        def __init__(self, **kwds):
##            self.__dict__.update(kwds)

def _partition(pred, iterable,
              # Optimized by replacing global lookups with local variables
              # defined as default values.
              filter=_itertools.ifilter,
              filterfalse=_itertools.ifilterfalse,
              tee=_itertools.tee):
    'Use a predicate to partition entries into false entries and true entries'
    # partition(is_odd, range(10)) --> 0 2 4 6 8   and  1 3 5 7 9
    t1, t2 = tee(iterable)
    return filterfalse(pred, t1), filter(pred, t2)

def _parse_line(f):
    from functools import wraps
    @wraps(f)
    def wrapper(self, line):
        args, kwds = _partition(
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

    def do_exit(self, line):
        '''Exits the interpreter.'''
        return True

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
        '''get path [key=value]...'''
        _pprint(self.mc.get('/'.join(path), **params))

    @_parse_line
    def do_post(self, *path, **params):
        '''post path [key=value]...'''
        _pprint(self.mc.post('/'.join(path), **params))

    def do_tokeninfo(self, line):
        '''Displays information about the access token.'''
        _pprint(self.mc.tokeninfo())

##_pprint(mc.user_profile())
##_pprint(mc.user_summary_daily(pastDays=7))
##_pprint(mc.user_activities_daily(pastDays=7))
##_pprint(mc.user_places_daily(pastDays=7))
##_pprint(mc.user_storyline_daily(pastDays=7))

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
    
