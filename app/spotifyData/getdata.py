from cv2 import randShuffle
from numpy import average
from regex import D
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from urllib.parse import quote
import pandas as pd

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
        self.key_map = {0:"C", 1:"C#", 2:"D", 3:"D#", 4:"E", 5:"F", 6:"F#", 7:"G", 8:"G#", 9:"A", 10:"A#", 11:"B"}
        self.mode_map = {0:"minor", 1:"major" }

    def __str__(self) -> str:
        return self.name
    
    def getInfo(self):
        info = {
            'id' : self.id,
            'name': self.name,
            'album': self.albumName,
            'artist': self.artistName,
            'spotify': self.spotifyPlay,
            'preview': self.preview
        }
        return info

    def getFeatures(self, wanted_features = []):
        #Here also this would be ideal If I could just select wanted features
        data = {
            'name': self.name,
            'album': self.albumName,
            'artist': self.artistName,
            'isExplicit': self.isExplicit,
            'popularity': self.popularity,
        }
        data.update(self.features)
        data.pop('type')
        data.pop('id')
        data.pop('uri')
        data.pop('track_href')
        data.pop('analysis_url')
        data["duration"] = self.getDuration()
        return {f: data[f] for f in wanted_features} if wanted_features else data

    def getDuration(self) -> int: #seconds
        return self.features['duration_ms'] // 1000

    def setAudioAnalysis(self, analysis):
        analysis = analysis["track"]
        self.analysis["loudness"] = analysis["loudness"]
        self.analysis["tempo"] = analysis["tempo"]
        self.analysis["time_signature"] = analysis["time_signature"]
        self.analysis["key"] = self.key_map[analysis["key"]]
        self.analysis["mode"] = self.mode_map[analysis["mode"]]


class Playlist:
    def __init__(self, id='', link='', imgUrl='', name='') -> None:
        self.id = id
        self.link = link
        self.imgUrl = imgUrl
        self.name = name
        self.tracks = []

    def updateInfoFromOutput(self, output: dict) -> None:
        self.id = output['id']
        self.link = output['external_urls']['spotify']
        self.imgUrl = output['images'][0]['url']
        self.name = output['name']

    def getFeatures(self, wanted_features = []):
        features = [track.getFeatures() for track in self.tracks]
        features = pd.DataFrame(features)

        return features[wanted_features] if wanted_features else features

    def getInfo(self):
        info = [track.getInfo() for track in self.tracks]
        return pd.DataFrame(info)

    def __str__(self) -> str:
        return ''.join(f'{x}\n' for x in self.tracks)

    def getDurationInSec(self) -> int:
        sec = sum([track.getDuration() for track in self.tracks])
        return sec

    def getDurationInMin(self) -> tuple: #(minutes, seconds)
        sec = self.getDurationInSec()
        return (sec//60, sec-(sec//60*60))

    def getAverageTempo(self) -> float:
        return average([track.features['tempo'] for track in self.tracks])

    def isExplicit(self) -> int: #percetnage
        explicits = [1 if track.features['explicit']
                     == True else 0 for track in self.tracks]
        return int(average(explicits)*100)

class DatasetCreator:
    def __init__(self, sp=None) -> None:
        self.sp = sp if sp is not None else spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
        self.country_codes = ['AD', 'AR', 'AU', 'AT', 'BE', 'BO', 'BR', 'BG', 'CA', 'CL', 'CO', 'CR', 'CY', 'CZ', 'DK', 'DO', 'EC', 'SV', 'EE', 'FI', 'FR', 'DE', 'GR', 'GT', 'HN', 'HK', 'HU', 'IS', 'ID',
                         'IE', 'IT', 'JP', 'LV', 'LI', 'LT', 'LU', 'MY', 'MT', 'MX', 'MC', 'NL', 'NZ', 'NI', 'NO', 'PA', 'PY', 'PE', 'PH', 'PL', 'PT', 'SG', 'ES', 'SK', 'SE', 'CH', 'TW', 'TR', 'GB', 'US', 'UY', 'GLOBAL']
        #see it, might be profitable in the futue -> https://datahub.io/core/country-list#resource-data

    def updatePlaylistTracks(self, playlist: Playlist):
        tracks = self.sp.playlist_tracks(playlist.id)
        #print(tracks['items'][0])
        for line in tracks['items']:
            track = Track(line['track'])
            track.features = self.sp.audio_features(tracks=[track.id])[0]
            track.setAudioAnalysis(self.sp.audio_analysis(track.id))
            playlist.tracks.append(track)

    def updateAlbumTracks(self, album: Playlist):
        tracks = self.sp.album_tracks(album.id)
        for line in tracks['items']:
            track = self.search(line['name'], filters={'artist': line['artists'][0]['name']})
            track.features = self.sp.audio_features(tracks=[track.id])[0]
            track.setAudioAnalysis(self.sp.audio_analysis(track.id))
            album.tracks.append(track)
    
    def getTopPlaylist(self, country: str) -> list:
        assert country.upper() in self.country_codes, f"{country} is not a country code"

        if country.upper() == 'GLOBAL':
            result = self.sp.category_playlists(
                category_id='toplists', country='PL', limit=2)['playlists']['items'][1]
        else:
            result = self.sp.category_playlists(
                category_id='toplists', country=country, limit=1)['playlists']['items'][0]
        
        countryTop = Playlist()
        countryTop.updateInfoFromOutput(result)

        self.updatePlaylistTracks(countryTop)

        return countryTop
    
    def search(self, name: str, type='track', filters={}):
        assert type in ['track', 'playlist', 'album'], f'{type} is unsupported'
        q = name + ' ' + ' '.join([x+':'+filters[x] for x in filters.keys()])
        result = self.sp.search(q=q, type=type, limit=1)
        if type == 'track':
            track = Track(result['tracks']['items'][0])
            track.features = self.sp.audio_features(tracks=[track.id])[0]
            track.setAudioAnalysis(self.sp.audio_analysis(track.id))
            return track
        elif type == 'playlist':
            playlist = Playlist()
            playlist.updateInfoFromOutput(result['playlists']['items'][0])
            self.updatePlaylistTracks(playlist)
            return playlist
        else:
            playlist = Playlist()
            playlist.updateInfoFromOutput(result['albums']['items'][0])
            self.updateAlbumTracks(playlist)
            return playlist
