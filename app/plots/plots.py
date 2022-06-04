import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import math
from plotly.subplots import make_subplots
import utils.constants as C
class Plots:
    def __init__(self) -> None:
        self.parallel_lines_queries = []
        self.parallel_lines_attributes = ["id"]

        self.sunburst_path = ['mode', 'explicit', 'key']

    def change_query(self,query):
        if query in self.parallel_lines_queries:
            print("removing")
            self.parallel_lines_queries.remove(query)
        else:
            self.parallel_lines_queries.append(query)

    def change_attr(self,attr):
        if attr in self.parallel_lines_attributes:
            print("removing")
            self.parallel_lines_attributes.remove(attr)
        else:
            self.parallel_lines_attributes.append(attr)

    def set_attr(self, attr: list):
        self.parallel_lines_attributes = ["id"] + attr

    def set_query(self, query: list):
        self.parallel_lines_queries = query

    def radarPlot(self,data : pd.DataFrame, behaviour="average"):
        if behaviour == "average":
                radarData = data[['danceability',  'energy',  'speechiness',  'acousticness',  'liveness',  'valence']]
                toPlot = radarData.mean()
                fig = px.line_polar(r=toPlot.values, theta=toPlot.index, line_close=True, range_r=[0,1])
        else:
                if behaviour == "separate":
                        separate_variable = "name"
                elif behaviour == "by_query":
                        separate_variable = "query"
                radarData = data[['danceability',  'energy',  'speechiness',  'acousticness',  'liveness',  'valence', separate_variable]]
                radarData = radarData.groupby([separate_variable]).mean().reset_index()
                radarData = pd.melt(radarData, id_vars=[separate_variable])

                fig = px.line_polar(radarData, r="value", theta="variable", color=separate_variable,
                            line_close=True, range_r=[0,1])
                fig.update_traces(opacity=0.7)

        fig.update_layout(margin=dict(l=0, r=0, t=25, b=25)) 

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
        
        return fig

    def topNTracks(self, data: pd.DataFrame, attribute='danceability', color='energy', top_n = 5):
        plotData = data.sort_values(by=[attribute], ascending=False)
        fig = px.bar(plotData.head(top_n), x='name', y=attribute, color=color, range_color=[0,1],color_continuous_scale=C.COLOR_SCALE_CONTINUOUS)
        fig.update_layout(title_text=f'Top {top_n} tracks based on {attribute}', title_x=0.5, title_font = {'size' : 24})

        return fig

    def keys(self, data: pd.DataFrame):
        keys = pd.DataFrame(data.value_counts())
        fig = px.bar(keys, orientation='h')
        
        return fig

    def parallel_coordinates_plot(self, df: pd.DataFrame):
        print(self.parallel_lines_attributes, self.parallel_lines_queries)

        if not self.parallel_lines_queries:
            return {}
        
        df = df[df['id'].isin(self.parallel_lines_queries)].reset_index()

        fig = px.parallel_coordinates(df[self.parallel_lines_attributes], color='id', color_continuous_scale=C.COLOR_SCALE_CONTINUOUS)

                                
        return fig

    def sunburst(self, df, num_of_cols = 3):
        df = df[C.CATEGORICAL_COLUMNS + ["count"]]
        queries = df["query"].unique()
        num_of_plots = len(queries)
        num_of_rows = max(math.ceil(num_of_plots/num_of_cols),1)

        fig = make_subplots(rows=  num_of_rows , cols = num_of_cols, 
        specs = [[{"type": "sunburst"} for i in range(num_of_cols)] for j in range(num_of_rows)],
        subplot_titles=(queries))

        curr_row = 1
        curr_col = 1
        for query in queries:
            df_to_plot = df[df["query"] == query]
            fig.add_trace(px.sunburst(df_to_plot, path = self.sunburst_path, values='count', color_discrete_sequence=C.COLOR_SCALE_DISCRETE)["data"][0], 
                            row=curr_row, col=curr_col,)
            curr_col+=1
            if curr_col == num_of_cols + 1:
                curr_col = 1
                curr_row += 1
        
        fig.update_layout(
        grid= dict(columns=num_of_cols, rows=num_of_rows),
        margin = dict(t=20, l=0, r=0, b=10),
        sunburstcolorway = C.COLOR_SCALE_DISCRETE,
        )

        return fig

    def scatter(self, df, x = "danceability", y="liveness", color= "query", rug_type= "box"):
        return px.scatter(df, x=x, y=y, color=color, marginal_y=rug_type, marginal_x= rug_type, color_discrete_sequence=C.COLOR_SCALE_DISCRETE)