from spotifyData import getdata

class RequestManager():
    def __init__(self, columns: list):
        self.requests = {}
        self.num_of_requests = 0
        self.columns = columns

    def add_request(self, phrase: str):
        self.requests[self.num_of_requests] = {"label": phrase, "value": self.num_of_requests}
        self.num_of_requests += 1

    def get_options(self):
        return list(self.requests.values())

    def add_data(self, rows: list, outcome):
        if isinstance(outcome, getdata.Track):
            rows.insert(0, self.get_instance(outcome))
        elif isinstance(outcome, getdata.Playlist):
            for track in outcome.tracks:
                rows.insert(0, self.get_instance(track))
        
        return rows

    def get_instance(self, row: getdata.Track):
        features = row.getFeatures(wanted_features=self.columns)
        features["id"] = self.num_of_requests

        return features

    def remove_request(self, rows: list, request_id: str):
        if request_id is None: return rows
        self.requests.pop(request_id)
        return [row for row in rows if row["id"] != request_id]
        
