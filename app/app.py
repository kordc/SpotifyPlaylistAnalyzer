import pandas as pd
import plotly.express as px

from dash import Dash, dash_table
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

import dash_bootstrap_components as dbc

#! for the layout use dash bootstrap!!!

df = pd.read_csv("example_data.csv")[["rank", "artist_names", "track_name", "streams"]]

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

print(df.columns)

table = dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns],
                            page_size = 10,
                            fill_width=False,
                            style_table={
                            'maxHeight': '50ex',
                            'overflowY': 'scroll',
                            #'width': '100%',
                            #'minWidth': '100%',
                        },
                        #fixed_rows={'headers': True}, ! this breaks width 
                            page_action='none',  
                        style_data={
                        'whiteSpace': 'normal',
                        'height': 'auto',
                        'lineHeight': '15px'
                    },
                        filter_action="native",
                        sort_action="native",
                        sort_mode="multi",
                         style_cell_conditional=[
                        {'if': {'column_id': 'rank'},
                        'width': '10%'},
                    
                    ]    
                        )
#df.to_dict(records) creates an array of JSON like objects and each is one row of the df
#dbc.Container can replace this DIv
#! IT SEEMS THAT DATABLES IN DASH DOES NOT SUPPORT BOOTSTRAP
# app.layout= html.Div([
#     table,
    
# ],style= {"width": "200px"})
app.layout =  dbc.Card([
             dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Table(table),
                        dbc.Alert(id='tbl_out'),
                    ], width=6)])
             ])
        ])
    

if __name__ == "__main__":
    app.run_server(debug=True)