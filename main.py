from spotifyData.getdata import *

if __name__ == "__main__":
    dataset = DatasetCreator()
    playlist = dataset.getTopPlaylist("PL")
    print(playlist.getFeatures())
