from spotifyData.getdata import DatasetCreator

if __name__ == "__main__":
    dataset = DatasetCreator()
    playlist = dataset.getTopPlaylist("PL")
    a = dataset.search('global-top-50', type='playlist')
    print(len(a.tracks))
