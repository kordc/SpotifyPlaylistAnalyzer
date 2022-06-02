import dash_bootstrap_components as dbc
from dash import dcc, html
from utils.valueBox import get_value_box

import utils.constants as C

def get_layout(table, footers_definitions):
    layout =  dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                            dbc.Col([
                                dcc.Dropdown(options=[
                                                    {'label': 'Funky 80\'s', 'value': 'funky.csv'},
                                                    {'label': 'top 50 metal', 'value': 'metal.csv'},
                                                    ],
                                            id=C.PRE_DROP,
                                            placeholder="Select one of the predefined datasets"),
                                    ], width = 3, style = {"border-right": "2px solid #3333ff"}),
                            dbc.Col([
                                dbc.Input(  id=C.SEARCH_PHRASE,
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
                                                id=C.SEARCH_TYPE, 
                                                inline=True,
                                                label_style= {"margin-right": "30px"},
                                                inputStyle={"margin-right": "5px"})
                                    ], width = 3),
                        dbc.Col([
                                    dbc.Button('Search', id=C.SEARCH_BUTTON, n_clicks=0, 
                                            style={"height": "90%"}, outline=True, color="info", className="me-1")
                                ], width=1, style = {"border-right": "2px solid #3333ff"}),
                        dbc.Col([
                                    dcc.Dropdown(options=[],
                                                id=C.UNDO_DROP,
                                                placeholder="Undo one of the steps"),
                                ], width=2),
                        dbc.Col([
                                    dbc.Button('Reset', id=C.RESET_BUTTON, n_clicks=0, style={"height": "90%"}, 
                                    outline=True, color="danger", className="me-1"),
                                ], width=1, style = {"border-right": "2px solid #3333ff"}),
                        dbc.Col([
                                    html.Img(src="assets/logo_green.png", height= "50px")
                                ],width=2)
                            ]),
                    dbc.Row([
                        dbc.Col([
                                    dbc.Table(table),
                                ], width=6),
                        dbc.Col([
                                 dbc.Row( dcc.Dropdown(options=[
                                                    {'label': "Average everything", 'value': 'average'},
                                                    {'label': 'By query', 'value': 'by_query'},
                                                    {'label': 'Each song separately (Mess, if you don\'t select some songs)', 'value': 'separate'},
                                                    ],
                                            id=C.RADAR_DROPDOWN,
                                            placeholder="Select the behaviour of radar plot"),
                                    ),
                                 dbc.Row(dcc.Graph(id=C.RADAR))   
                                ], width=6)]) # style={"display": "none"} We could possibly use this to hide the graph entirely
                        ]),
                    dbc.Row([
                                dbc.Col([
                                        dbc.Row( [
                                                dcc.Slider(0, 30, 5,
                                                        value=10,
                                                        id=C.TOP_N_SLIDER),

                                                dbc.Col(dcc.Dropdown(options=[ {'label': attr, "value": attr} for attr in C.NUMERICAL_COLUMNS],
                                                                id=C.TOP_N_ATTR,
                                                                placeholder="Top 5 in...")),
                                                                
                                                dbc.Col(dcc.Dropdown(options=[ {'label': attr, "value": attr} for attr in C.NUMERICAL_COLUMNS],
                                                                        id=C.TOP_N_COLOR,
                                                                        placeholder="color based on"),
                                                        ),
                                                ]
                                        ),
                                        dbc.Row(dcc.Graph(id=C.TOP_N_PLOT))   
                                        ], width=6),
                                dbc.Col([
                                        dbc.Row([
                                                dbc.Col(dcc.Dropdown(options=[],
                                                        id=C.PARALLEL_COORDS_QUERIES,
                                                        placeholder="Select query to be added/removed from plot"), width=8),
                                                dbc.Col(dbc.Button('Reset queries', id=C.PARALLEL_COORDS_QUERIES_RESET, n_clicks=0, 
                                                style={"height": "90%"}, outline=True, color="danger", className="me-1"),width=3)    
                                        ]),
                                        dbc.Row([
                                                dbc.Col(dcc.Dropdown(options=C.PARALLEL_ATTR,
                                                        id=C.PARALLEL_COORDS_ATTR,
                                                        placeholder="Select attributes to be added/removed from plot"), width=8),
                                                dbc.Col(dbc.Button('Reset attributes', id=C.PARALLEL_COORDS_ATTR_RESET, n_clicks=0, 
                                                style={"height": "90%"}, outline=True, color="danger", className="me-1"),width=3)     
                                        ]),
                                        dbc.Row(dcc.Graph(id=C.PARALLEL_COORDS)) 
                                ], width=6)
                        ]),
                dbc.Row(
                    [dbc.Col(dbc.Card(get_value_box(**parameters), color='success', inverse=True)) 
                                                    for parameters in footers_definitions ],
                    className="mb-4",
                    id=C.FOOTER),
                ])

    return layout