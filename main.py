from spotifyData.getdata import DatasetCreator
from plots.plots import Plots

if __name__ == "__main__":
    dataset = DatasetCreator()
    plots = Plots()
    pl = dataset.getTopPlaylist("PL")
    fig = plots.radarPlot(pl)
    fig.show()
