from flask import Flask, url_for, request, session, redirect
from moves import MovesClient
from datetime import datetime, timedelta
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


@app.route('/logout')
def logout():
    if 'token' in session:
        del(session['token'])
    return redirect(url_for('index'))


@app.route("/info")
def show_info():
    profile = Moves.user_profile(access_token=session['token'])
    response = 'User ID: %s<br />First day using Moves: %s' % \
        (profile['userId'], profile['profile']['firstDate'])
    return response + "<br /><a href=\"%s\">Info for today</a>" % url_for('today') + \
        "<br /><a href=\"%s\">Logout</a>" % url_for('logout')


@app.route("/today")
def today():
    today = datetime.now().strftime('%Y%m%d')
    info = Moves.user_summary_daily(today, access_token=session['token'])
    res = ''
    for activity in info[0]['summary']:
        if activity['activity'] == 'wlk':
            res += 'Walking: %d steps<br />' % activity['steps']
        elif activity['activity'] == 'run':
            res += 'Running: %d steps<br />' % activity['steps']
        elif activity['activity'] == 'cyc':
            res += 'Cycling: %dm' % activity['distance']
    return res


@app.route("/expanded-summary")
def expanded_summary():
    today = datetime.now().strftime('%Y%m%d')
    info = Moves.user_summary_daily(today, access_token=session['token'])
    res = ''
    for activity in info[0]['summary']:
        res = activities_block(activity, res)
        if activity['activity'] == 'wlk':
            res += 'Walking: %d steps<br />' % activity['steps']
            res += 'Walking: %d calories<br />' % activity['calories']
            res += 'Walking: %d distance<br />' % activity['distance']
            res += 'Walking: %d duration<br /><br />' % activity['duration']
        elif activity['activity'] == 'run':
            res += 'Running: %d steps<br />' % activity['steps']
            res += 'Running: %d calories<br />' % activity['calories']
            res += 'Running: %d distance<br />' % activity['distance']
            res += 'Running: %d duration<br /><br />' % activity['duration']
        elif activity['activity'] == 'cyc':
            res += 'Cycling: %dm<br />' % activity['distance']
            res += 'Cycling: %d calories<br />' % activity['calories']
            res += 'Cycling: %d distance<br />' % activity['distance']
            res += 'Cycling: %d duration<br />' % activity['duration']
    return res


@app.route("/activities")
def activities():
    today = datetime.now().strftime('%Y%m%d')
    info = Moves.user_activities_daily(today, access_token=session['token'])
    res = ''
    for segment in info[0]['segments']:
        if segment['type'] == 'move':
            res += 'Move<br />'
            res = segment_start_end(segment, res)
            for activity in segment['activities']:
                res += 'Activity %s<br />' % activity['activity']
                res = activity_start_end(activity, res)
                res += 'Duration: %d<br />' % activity['duration']
                res += 'Distance: %dm<br />' % activity['distance']
            res += '<br />'
        elif segment['type'] == 'place':
            res += 'Place<br />'
            res = segment_start_end(segment, res)
            for activity in segment['activities']:
                res += 'Activity %s<br />' % activity['activity']
                res = activity_start_end(activity, res)
                res += 'Duration: %d<br />' % activity['duration']
                res += 'Distance: %dm<br />' % activity['distance']
            res += '<br />'
    return res


@app.route("/places")
def places():
    today = datetime.now().strftime('%Y%m%d')
    info = Moves.user_places_daily(today, access_token=session['token'])
    res = ''
    for segment in info[0]['segments']:
        res = place(segment, res)
    return res


@app.route("/storyline")
def storyline():
    today = datetime.now().strftime('%Y%m%d')
    info = Moves.user_storyline_daily(today, trackPoints={'true'}, access_token=session['token'])
    res = ''
    for segment in info[0]['segments']:
        if segment['type'] == 'place':
            res = place(segment, res)
        elif segment['type'] == 'move':
            res = move(segment, res)
        res += '<hr>'
    return res


def segment_start_end(segment, res):
    res += 'Start Time: %s<br />' % segment['startTime']
    res += 'End Time: %s<br />' % segment['endTime']
    return res


def activity_start_end(activity, res):
    res += 'Start Time: %s<br />' % activity['startTime']
    res += 'End Time: %s<br />' % activity['endTime']
    return res


def place_block(segment, res):
    res += 'ID: %d<br />' % segment['place']['id']
    res += 'Name: %s<br />' % segment['place']['name']
    res += 'Type: %s<br />' % segment['place']['type']
    if segment['place']['type'] == 'foursquare':
        res += 'Foursquare ID: %s<br />' % segment['place']['foursquareId']
    res += 'Location<br />'
    res += 'Latitude: %f<br />' % segment['place']['location']['lat']
    res += 'Longitude: %f<br />' % segment['place']['location']['lon']
    return res


def trackPoint(track_point, res):
    res += 'Latitude: %f<br />' % track_point['lat']
    res += 'Longitude: %f<br />' % track_point['lon']
    res += 'Time: %s<br />' % track_point['time']
    return res


def activities_block(activity, res):
    res += 'Activity: %s<br />' % activity['activity']
    res = activity_start_end(activity, res)
    res += 'Duration: %d<br />' % activity['duration']
    res += 'Distance: %dm<br />' % activity['distance']
    if activity['activity'] == 'wlk' or activity['activity'] == 'run':
        res += 'Steps: %d<br />' % activity['steps']
    if activity['activity'] != 'trp':
        res += 'Calories: %d<br />' % activity['calories']
    if 'trackPoints' in activity:
        for track_point in activity['trackPoints']:
            res = trackPoint(track_point, res)
    return res


def place(segment, res):
    res += 'Place<br />'
    res = segment_start_end(segment, res)
    res = place_block(segment, res)
    if 'activities' in segment:
        for activity in segment['activities']:
            res = activities_block(activity, res)
    res += '<br />'
    return res


def move(segment, res):
    res += 'Move<br />'
    res = segment_start_end(segment, res)
    for activity in segment['activities']:
        res = activities_block(activity, res)
    res += '<br />'
    return res

app.secret_key = _keys.secret_key

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
