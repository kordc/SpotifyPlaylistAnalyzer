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
                                    dcc.Graph(id=C.RADAR)
                                ], width=6)]) # style={"display": "none"} We could possibly use this to hide the graph entirely
                        ]),
                dbc.Row(
                    [dbc.Col(dbc.Card(get_value_box(**parameters), color='success', inverse=True)) 
                                                    for parameters in footers_definitions ],
                    className="mb-4",
                    id=C.FOOTER),
                ])

    return layout