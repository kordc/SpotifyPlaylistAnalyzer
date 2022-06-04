from spotifyData import getdata, getdata_faster
import tekore as tk
from spotifyData.getdata_faster import get_feature_dict

class RequestManager():
    def __init__(self):
        self.requests = {}
        self.num_of_requests = 1
        self.your_playlist_id = 0 # This is is devoted for the tracks added by the user
        self.your_playlist_name = "Your playlist"
        
    def add_request(self, phrase: str, type_):
        #We need to handle differently tracks and other things
        phrase = phrase if type_ != "track" else self.your_playlist_name
        id_ = self.num_of_requests if type_ != "track" else self.your_playlist_id

        self.requests[id_] = {"label": phrase, "value": id_}
        #We track single tracks as someone playlist
        if type_ != "track":
            self.num_of_requests += 1

    def get_options(self):
        return list(self.requests.values())

    def add_data(self, rows: list, outcome, query_name: str):
        audio_info, audio_features = outcome
        if isinstance(audio_features, tk.model.AudioFeatures):
            rows.insert(0, self.get_instance(audio_info, audio_features, self.your_playlist_name, "track"))
        
        elif isinstance(audio_features, tk.model.ModelList):
            for info, features in zip(audio_info, audio_features):
                rows.insert(0, self.get_instance(info, features, query_name, "playlist"))
        
        return rows

    def get_instance(self, audio_info: tk.model.FullTrack, audio_features: tk.model.AudioFeatures, query_name : str, type_= "track"):
        features = get_feature_dict(audio_info, audio_features)
        features["id"] = self.num_of_requests if type_ != "track" else self.your_playlist_id
        features["query"] = query_name if type_ != "track" else self.your_playlist_name
        features["count"] = 1 #special thing for sunburst plot
        return features

    def remove_request(self, request_id):
        self.requests.pop(request_id)

    def remove_data(self, rows, request_id):
        if request_id is None:
            return rows
        self.remove_request(request_id)
        return [row for row in rows if row["id"] != request_id]

    def reset_requests(self,):
        self.requests = {}
        self.num_of_requests = 1
        
