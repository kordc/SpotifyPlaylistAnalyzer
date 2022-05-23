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
from utils import request_manager
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

request_manager = request_manager.RequestManager(columns=columns)

#Simple extension allowing for multiple callbacks for one Output
app = DashProxy(prevent_initial_callbacks=True, transforms=[MultiplexerTransform()], external_stylesheets=[dbc.themes.BOOTSTRAP])

table = dash_table.DataTable(pd.DataFrame(columns=columns).to_dict("records"),
                            [{"name": i, "id": i} for i in columns[:3]],
                            #hidden_columns = columns[3:], This is not needed we can just omit not necesarry columns and data would be unchanged
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
                        #sort_action="native",
                        sort_mode="multi",
                        row_selectable="multi",
                        row_deletable=True,
                        editable=True, 
                         style_cell_conditional=[
                        {'if': {'column_id': 'rank'},
                        'width': '10%'},
    
                    ],
                      
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
                    ], width = 3, style = {"border-right": "2px solid #3333ff"}),
                    dbc.Col([
                        dbc.Input(
                        id="search_phrase",
                        type="text",
                        placeholder="search for artist/track/playlist",
                        style = {"width": "100%"},
                        debounce=True),
                        dbc.RadioItems(options=[
                            {"label": "track", "value": "track"},
                            {"label": "playlist", "value": "playlist"},
                            {"label": "album", "value": "album"},
                        ],
                        value="track",
                        id="search_type", 
                        inline=True,
                        label_style= {"margin-right": "30px"},
                        inputStyle={"margin-right": "5px"})
                    ], width = 3),
                    dbc.Col([
                        dbc.Button('Search', id='search_data', n_clicks=0, style={"height": "90%"}, outline=True, color="info", className="me-1")
                    ], width=1, style = {"border-right": "2px solid #3333ff"}),
                    dbc.Col([
                       dcc.Dropdown(options=[],
                                    id='undo_step',
                                    placeholder="Undo one of the steps"),
                    ], width=2),
                    dbc.Col([
                       dbc.Button('Reset', id='reset_data', n_clicks=0, style={"height": "90%"}, outline=True, color="danger", className="me-1"),
                    ], width=1, style = {"border-right": "2px solid #3333ff"}),
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
                    ], width=6)]) # style={"display": "none"} We could possibly use this to hide the graph entirely
             ])
        ])


@app.callback(
    Output('table_of_songs', 'data'),
    Input('predefined_datasets', 'value')
)
def load_predefined_data(path):
    df = pd.read_csv(path)[columns]
    return df.to_dict("records")

@app.callback(
    [Output('table_of_songs', 'data'), Output("undo_step", "options"), Output("radarPlot", "figure"),],
    Input('undo_step', 'value'),
    State("table_of_songs", "data")
)
def undo_step(request_id, rows):
    new_rows = request_manager.remove_data(rows, request_id)
    plot = plots_generator.radarPlot(pd.DataFrame(new_rows)) if new_rows else {}

    return new_rows, request_manager.get_options(), plot

@app.callback(
    [Output('table_of_songs', 'data'), Output("radarPlot", "figure"), Output("undo_step", "options")],
    State("search_phrase", "value"), State("search_type", "value"), State("table_of_songs", "data"),
    Input("search_data", "n_clicks")
)
def add_search_to_table(phrase, type_, rows, n_clicks):
    if n_clicks > 0:
        outcome = creator.search(phrase, type=type_)
        request_manager.add_data(rows, outcome)
        request_manager.add_request(phrase)
        
        return rows, plots_generator.radarPlot(pd.DataFrame(rows)), request_manager.get_options()

@app.callback(
    [Output('table_of_songs', 'data'), Output("undo_step", "options"),
    Output("radarPlot", "figure"),],
    Input('reset_data', 'n_clicks'),
)
def reset_table(n_clicks):
    if n_clicks > 0:
        request_manager.reset_requests()
        return pd.DataFrame(columns=columns).to_dict("records"), request_manager.get_options(), {}


@app.callback(
    Output("radarPlot", "figure"),
    Input("table_of_songs", "data_previous"),
    State("table_of_songs", "data")
)
def update_at_removal(old_data, rows):
    return plots_generator.radarPlot(pd.DataFrame(rows))


@app.callback(
    Output("radarPlot", "figure"),
    Input("table_of_songs", "selected_rows"),
    State("table_of_songs", "data")
)
def only_selected_rows(selected_rows,rows):
    if selected_rows:
        rows = [rows[index] for index in selected_rows]
    return plots_generator.radarPlot(pd.DataFrame(rows))

if __name__ == "__main__":
    app.run_server(debug=True)