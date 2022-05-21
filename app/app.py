import pandas as pd
import plotly.express as px

from dash import Dash, dash_table
from dash import dcc
from dash import html
from dash_extensions.enrich import Output, DashProxy, Input, MultiplexerTransform, State
import yaml
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from spotifyData import getdata
from plots import plots
#from dash.dependencies import Input, Output, State

import dash_bootstrap_components as dbc

credentials_path = "credentials.yaml"
with open(credentials_path) as file:
    cred = yaml.load(file, Loader=yaml.FullLoader)

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=cred['client_id'], client_secret= cred['client_secret']))
creator = getdata.DatasetCreator(sp=sp)
plots_generator = plots.Plots()

#! for the layout use dash bootstrap!!!
columns = ['name','album','artist', 'danceability',  'energy',  'speechiness',  'acousticness',  'liveness',  'valence']

#Simple extension allowing for multiple callbacks for one Output
app = DashProxy(prevent_initial_callbacks=True, transforms=[MultiplexerTransform()], external_stylesheets=[dbc.themes.BOOTSTRAP])

table = dash_table.DataTable(pd.DataFrame(columns=columns).to_dict("records"),
                            [{"name": i, "id": i} for i in columns],
                            hidden_columns = columns[3:],
                            id = "table_of_songs",
                            page_size = 10,
                            fill_width=False,
                            style_table={
                            'maxHeight': '50ex',
                            'overflowY': 'scroll',
    
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
    
                    ],
                    editable=True,
                    row_deletable=True    
                        )

app.layout =  dbc.Card([
             dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dcc.Dropdown(options=[
                                    {'label': 'Funky 80\'s', 'value': 'funky.csv'},
                                    {'label': 'top 50 metal', 'value': 'metal.csv'},
                                ],
                                    id='predefined_datasets',
                                    placeholder="Select one of the predefined datasets"),
                        html.Div(id='dd-output-container')
                    ], width = 3),
                    dbc.Col([
                        dcc.Input(
                        id="search_phrase",
                        type="text",
                        placeholder="search for artist/track/playlist",
                        style = {"width": "100%"},
                        debounce=True),
                        html.Div(id='search_container')
                    ], width = 4),
                    dbc.Col([
                        dcc.RadioItems(['track', 'playlist','album'], 'track',
                        id="search_type", 
                        inline=True,
                        inputStyle= {"margin": "0 5px 0 5px"})
                        
                    ], width=2),
                    dbc.Col([
                       html.Button('Reset', id='reset_data', n_clicks=0),
                    ], width=1),
                    dbc.Col([
                        html.Img(src="assets/logo_green.png", height= "50px")
                    ],width=2)
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Table(table),
                        dbc.Alert(id='tbl_out'),
                    ], width=6),
                    dbc.Col([
                        dcc.Graph(id="radarPlot")
                    ], width=6)])
             ])
        ])


@app.callback(
    Output('table_of_songs', 'data'),
    Input('predefined_datasets', 'value')
)
def update_output(path):
    #Callback to load predefined datasets from path
    df = pd.read_csv(path)[columns]
    return df.to_dict("records")

@app.callback(
    [Output('table_of_songs', 'data'),
    Output("radarPlot", "figure")],
    Input("search_phrase", "value"),
    State("search_type", "value"),
    State("table_of_songs", "data")
)
def update_output(phrase, type_, rows):
    #Callback from updating the data table
    outcome = creator.search(phrase, type=type_)
    if isinstance(outcome, getdata.Track):
        #! Here ideally I want to get selected attributes, this would make adding elements very easy
        rows.insert(0, outcome.getFeatures(wanted_features=columns))
    elif isinstance(outcome, getdata.Playlist):
        #! Herre ideally I want only selected attributes
        for track in outcome.tracks:
            rows.insert(0, track.getFeatures(wanted_features=columns))

    
    return rows, plots_generator.radarPlot(pd.DataFrame(rows))

@app.callback(
    Output('table_of_songs', 'data'),
    Input('reset_data', 'n_clicks'),
)
def update_output(n_clicks):
    if n_clicks > 0:
        return pd.DataFrame(columns=columns).to_dict("records")

if __name__ == "__main__":
    app.run_server(debug=True)