from flask import Flask, url_for, request, session, redirect
from moves import MovesClient
import _keys

app = Flask(__name__)

Moves = MovesClient(_keys.client_id, _keys.client_secret)


@app.route("/")
def index():
    if 'token' not in session:
        oauth_return_url = url_for('oauth_return', _external=True)
        auth_url = Moves.build_oauth_url(oauth_return_url)
        return 'Authorize this application: <a href="%s">%s</a>' % \
            (auth_url, auth_url)
    return redirect(url_for('show_info'))


@app.route("/oauth_return")
def oauth_return():
    error = request.values.get('error', None)
    if error is not None:
        return error
    oauth_return_url = url_for('oauth_return', _external=True)
    code = request.args.get("code")
    token = Moves.get_oauth_token(code, redirect_uri=oauth_return_url)
    session['token'] = token
    return redirect(url_for('show_info'))


@app.route("/info")
def show_info():
    profile = Moves.user_profile(access_token=session['token'])
    print profile
    return "User info: %s" % str(profile)

app.secret_key = _keys.secret_key

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
