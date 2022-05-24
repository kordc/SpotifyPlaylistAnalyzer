import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class Plots:
    def __init__(self) -> None:
        pass

    def radarPlot(self, data : pd.DataFrame):
        radarData = data[['danceability',  'energy',  'speechiness',  'acousticness',  'liveness',  'valence']]
    
        toPlot = radarData.mean().to_frame()
        
        toPlot.columns = ['r']
        toPlot['theta'] = toPlot.index

        fig = px.line_polar(toPlot, r='r', theta='theta',
                            line_close=True, color_discrete_sequence=('#1ED760', '#1ED760', '#1ED760', '#1ED760', '#1ED760', '#1ED760'))
        fig.update_traces(fill='toself')
        
        return fig

    def gaugeColor(self, value):
        if value <=0.33:
            return 'red'
        elif value <= 0.5:
            return 'yellow'
        else:
            return 'darkgreen'
    
    def valenceGauge(self, data : pd.DataFrame):
        valence = data['valence'].mean()
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=valence,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Positivity", 'font': {'size': 24}},
            gauge={'axis': {'range': [None, 1], 'tickcolor': "darkblue"},
                   'bar': {'color': self.gaugeColor(valence)},
                   'steps': [
                 {'range': [0, 1], 'color': "lightgray"}]
                 }
            ))
        
        return(fig)

