import json
import urllib
import requests


class MovesAPIError(Exception):
    """Raised if the Moves API returns an error."""
    pass


class MovesClient(object):
    """OAuth client for the Moves API"""

    def __init__(self, client_id=None, client_secret=None, access_token=None,
                 use_app=False):

        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.api_url = "https://api.moves-app.com/api/v1"
        self.auth_url = "moves://app/authorize" if use_app else \
            "https://api.moves-app.com/oauth/v1/authorize"
        self.token_url = "https://api.moves-app.com/oauth/v1/access_token"
        self.use_app = use_app

    def parse_response(self, response):
        """Parse JSON API responses."""

        response = json.loads(response)
        return response

    def build_oauth_url(self, redirect_uri=None, scope="activity location"):
        params = {
            'client_id': self.client_id,
            'scope': scope
        }

        if not self.use_app:
            params['response_type'] = 'code'

        if redirect_uri:
            params['redirect_uri'] = redirect_uri
        # Moves hates +s for spaces, so use %20 instead.
        encoded = urllib.urlencode(params).replace('+', '%20')
        return "%s?%s" % (self.auth_url, encoded)

    def get_oauth_token(self, code, **kwargs):

        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'grant_type': kwargs.get('grant_type', 'authorization_code')
        }

        if 'redirect_uri' in kwargs:
            params['redirect_uri'] = kwargs['redirect_uri']
        response = requests.post(self.token_url, params=params)
        response = json.loads(response.content)
        try:
            return response['access_token']
        except:
            error = "<%(error)s>: %(error_description)s" % response
            raise MovesAPIError(error)

    def api(self, path, method='GET', **kwargs):

        params = kwargs['params'] if 'params' in kwargs else {}
        data = kwargs['data'] if 'data' in kwargs else {}

        if not self.access_token and 'access_token' not in params:
            raise MovesAPIError("You must provide a valid access token.")

        url = "%s/%s" % (self.api_url, path)

        if 'access_token' in params:
            access_token = params['access_token']
            del(params['access_token'])
        else:
            access_token = self.access_token

        headers = {
            "Authorization": 'Bearer ' + access_token
        }

        resp = requests.request(method, url, data=data, params=params,
                                headers=headers)
        if str(resp.status_code)[0] not in ('2', '3'):
            raise MovesAPIError("Error returned via the API with status code (%s):" %
                                resp.status_code, resp.text)
        return resp

    def get(self, path, **params):
        return self.parse_response(self.api(path, params=params).text)

    def post(self, path, **params):
        return self.parse_response(self.api(path, data=params).text)

    def set_first_date(self):
        if not self.first_date:
            response = self.user_profile()
            self.first_date = response['profile']['firstDate']

    def __getattr__(self, name):
        path = name

        def closure(*args, **kwargs):
            base_path = path.replace('_', '/')
            if len(args) > 0:
                name = "%s/%s" % (base_path, '/'.join(args))
            else:
                name = base_path
            return self.parse_response(self.api(name, 'GET',
                                       params=kwargs).text)
        return closure
