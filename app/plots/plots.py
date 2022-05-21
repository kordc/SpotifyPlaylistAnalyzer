from spotifyData.getdata import *
import plotly.express as px
import pandas as pd

class Plots:
    def __init__(self) -> None:
        pass

    def radarPlot(self, data : pd.DataFrame):
        radarData = data[['danceability',  'energy',  'speechiness',  'acousticness',  'liveness',  'valence']]
    
        toPlot = radarData.mean().to_frame()
        
        #print(toPlot)
        toPlot.columns = ['r']
        toPlot['theta'] = toPlot.index

        fig = px.line_polar(toPlot, r='r', theta='theta',
                            line_close=True, color_discrete_sequence=('#1ED760', '#1ED760', '#1ED760', '#1ED760', '#1ED760', '#1ED760'))
        fig.update_traces(fill='toself')
        
        return fig

