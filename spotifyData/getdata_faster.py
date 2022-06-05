import tekore as tk #Thank you tekore for creating such a wonderful module :) 

key_map = {0:"C", 1:"C#", 2:"D", 3:"D#", 4:"E", 5:"F", 6:"F#", 7:"G", 8:"G#", 9:"A", 10:"A#", 11:"B"}
mode_map = {0:"minor", 1:"major" }

def get_feature_dict(audio_info: tk.model.FullTrack, audio_features: tk.model.AudioFeatures):
    features = {}

    features["artist"] = audio_info.artists[0].name
    features["explicit"] = audio_info.explicit
    features["name"] = audio_info.name
    features["album"] = audio_info.album.name
    features["popularity"] = audio_info.popularity

    features["acousticness"] = audio_features.acousticness
    features["danceability"] = audio_features.danceability
    features["duration"] = audio_features.duration_ms // 1000 // 60
    features["energy"] = audio_features.energy
    features["instrumentalness"] = audio_features.instrumentalness
    features["key"] = key_map[audio_features.key]
    features["liveness"] = audio_features.liveness
    features["loudness"] = audio_features.loudness
    features["mode"] = mode_map[audio_features.mode]
    features["speechiness"] = audio_features.speechiness
    features["time_signature"] = audio_features.time_signature
    features["valence"] = audio_features.valence
    features["tempo"] = audio_features.tempo
    

    return features

class DatasetCreator:
    """Handle track/playlist/album searches on spotify API"""
    def __init__(self, spotify_api=None) -> None:
        self.spotify_api = spotify_api
    
    def search(self, name: str, type='track', filters={}):
        assert type in ['track', 'playlist', 'album'], f'{type} is unsupported'
        q = name + ' ' + ' '.join([x+':'+filters[x] for x in filters.keys()])
        result = self.spotify_api.search(query=q, types=(type,), limit=1)
        item_id = result[0].items[0].id

        if type == 'track':
            return self.spotify_api.track(item_id), self.spotify_api.track_audio_features(item_id)

        elif type == 'playlist':
            track_info = []
            track_features = tk.model.ModelList()
            max_ids_in_request = 50
            ids = []
            for track in self.spotify_api.playlist_items(item_id, as_tracks=True)['items']:
                ids.append(track["track"]["id"])
            
            for i in range(0,len(ids),max_ids_in_request):
                track_info += self.spotify_api.tracks(ids[i:i+max_ids_in_request])
                track_features += self.spotify_api.tracks_audio_features(ids[i:i+max_ids_in_request])
            
            return track_info, track_features

        else:
            track_info = []
            track_features = tk.model.ModelList()
            max_ids_in_request = 50
            ids = []
            album = self.spotify_api.album(item_id)

            for track in album.tracks.items:
                ids.append(track.id)

            for i in range(0, len(ids), max_ids_in_request):
                track_info += self.spotify_api.tracks(ids[i:i+max_ids_in_request])
                track_features += self.spotify_api.tracks_audio_features(ids[i:i+max_ids_in_request])

            return track_info, track_features

