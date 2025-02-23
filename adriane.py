import spotipy  # Spotipy library for Spotify API interaction | Install "pip install spotipy"
from spotipy.oauth2 import SpotifyOAuth  # Authentication handler for Spotify API
from flask import Flask, render_template, request  # Flask framework for web app | Install "pip install flask"

app = Flask(__name__)  # Initialize Flask application

# Authenticate with Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="19e677300cf04bbd94797a96016c1911",
    client_secret="fad9fd7323f84e2498a18597f35e44d6",
    redirect_uri="http://localhost:8888/callback",
    scope="user-top-read"
))

# Function to fetch user's top tracks within a given time range
def get_top_tracks(time_range, limit=10):
    results = sp.current_user_top_tracks(time_range=time_range, limit=limit)
    return [{
        "name": item['name'],
        "artists": ', '.join(artist['name'] for artist in item['artists']),
        "spotify_url": item['external_urls']['spotify'],
        "image_url": item['album']['images'][0]['url'] if item['album']['images'] else None  # Get album image
    } for item in results['items']]


# Function to fetch user's Spotify display name
def get_user_name():
    return sp.current_user()['display_name']

# Route to handle home page and track retrieval
@app.route('/', methods=['GET', 'POST'])
def adrianefrontend():
    time_ranges = {'short_term': '1 Month', 'medium_term': '6 Months', 'long_term': '1 Year'}
    selected_range = request.form.get("time_range", "short_term")
    return render_template("adrianefrontend.html",
                           top_tracks=get_top_tracks(selected_range),
                           time_ranges=time_ranges,
                           selected_range=selected_range,
                           user_name=get_user_name())

if __name__ == "__main__":
    app.run(debug=True)  # Run Flask app in debug mode
