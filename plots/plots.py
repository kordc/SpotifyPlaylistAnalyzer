from spotifyData.getdata import *
import plotly.express as px


class Plots:
    def __init__(self) -> None:
        pass

    def radarPlot(self, data):
        radarData = data.getFeatures().drop(
            ['name', 'key', 'mode', 'duration_ms', 'time_signature', 'isExplicit', 'instrumentalness', 'popularity', 'tempo', 'loudness'], 1)

        if isinstance(data, Playlist):
            toPlot = radarData.mean().to_frame()
        elif isinstance(data, Track):
            toPlot = radarData
        else:
            raise Exception('Wrong data type for the radar plot')

        toPlot.columns = ['r']
        toPlot['theta'] = toPlot.index

        fig = px.line_polar(toPlot, r='r', theta='theta',
                            line_close=True, color_discrete_sequence=('#1ED760', '#1ED760', '#1ED760', '#1ED760', '#1ED760', '#1ED760'))
        fig.update_traces(fill='toself')
        
        return fig

