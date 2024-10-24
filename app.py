from flask import Flask, redirect, url_for, session, request, jsonify
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for Flask session

# Replace with your own Spotify App credentials
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'
REDIRECT_URI = 'http://localhost:5000/callback'  # Change this if hosting online
SCOPE = 'user-library-modify user-follow-modify user-follow-read'

@app.route('/')
def index():
    return '''
    <h1>Presave All Future Releases!</h1>
    <button onclick="window.location.href='/login'">Click to Presave</button>
    '''

@app.route('/login')
def login():
    sp_oauth = SpotifyOAuth(client_id=CLIENT_ID,
                            client_secret=CLIENT_SECRET,
                            redirect_uri=REDIRECT_URI,
                            scope=SCOPE)
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    sp_oauth = SpotifyOAuth(client_id=CLIENT_ID,
                            client_secret=CLIENT_SECRET,
                            redirect_uri=REDIRECT_URI,
                            scope=SCOPE)

    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info

    return redirect(url_for('presave'))

@app.route('/presave')
def presave():
    token_info = session.get('token_info', None)
    if not token_info:
        return redirect('/')

    sp = spotipy.Spotify(auth=token_info['access_token'])

    artist_id = 'your_artist_id'  # Replace with the artist's Spotify ID
    sp.user_follow_artists([artist_id])

    # Here, you could periodically save new releases as before.
    # For simplicity, let's just display a success message.
    return '''
    <h1>Success!</h1>
    <p>You are now following the artist. Future releases will be saved to your library.</p>
    '''

if __name__ == '__main__':
    app.run(debug=True)
