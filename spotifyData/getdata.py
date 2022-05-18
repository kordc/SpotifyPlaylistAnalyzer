import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from urllib.parse import quote
import string
import sys

def searchPlaylist(possibleName):
    possibleName = quote(possibleName)
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    results = sp.search(q='playlist:' + possibleName, type='playlist')

class Track:
    def __init__(self, output: dict) -> None:
        self.id = output['id']
        self.name = output['name']
        self.albumID = output['album']['id']
        self.albumName = output['album']['name']
        self.artistName = output['artists'][0]['name']
        self.artistID = output['artists'][0]['id']
        self.isExplicit = output['explicit']
        self.spotifyPlay = output['external_urls']['spotify']
        self.preview = output['preview_url']
        self.popularity = float(output['popularity'])
        self.features = {}
        self.analysis = {}


class Playlist:
    def __init__(self, output: dict) -> None:
        self.id = output['id']
        self.link =  output['external_urls']['spotify']
        self.imgUrl = output['images'][0]['url']
        self.name = output['name']
        self.tracks = []


class DatasetCreator:
    def __init__(self) -> None:
        self.sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
        self.country_codes = ['AD', 'AR', 'AU', 'AT', 'BE', 'BO', 'BR', 'BG', 'CA', 'CL', 'CO', 'CR', 'CY', 'CZ', 'DK', 'DO', 'EC', 'SV', 'EE', 'FI', 'FR', 'DE', 'GR', 'GT', 'HN', 'HK', 'HU', 'IS', 'ID',
                         'IE', 'IT', 'JP', 'LV', 'LI', 'LT', 'LU', 'MY', 'MT', 'MX', 'MC', 'NL', 'NZ', 'NI', 'NO', 'PA', 'PY', 'PE', 'PH', 'PL', 'PT', 'SG', 'ES', 'SK', 'SE', 'CH', 'TW', 'TR', 'GB', 'US', 'UY']
        #see it, might be profitable in the futue -> https://datahub.io/core/country-list#resource-data

    def getTopPlaylist(self, country: str) -> list:
        assert country in self.country_codes, f"{country} is not a country code"
        countryTop = Playlist(self.sp.category_playlists(
            category_id='toplists', country=country, limit=1)['playlists']['items'][0])
        tracks = self.sp.playlist_tracks(countryTop.id)
        for line in tracks['items'][:1]:
            track = Track(line['track'])
            track.features = self.sp.audio_features(tracks=[track.id])
            track.analysis = self.sp.audio_analysis(track.id)
            countryTop.tracks.append(track)
        return countryTop
        
