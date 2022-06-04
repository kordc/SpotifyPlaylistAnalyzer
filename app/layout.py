import dash_bootstrap_components as dbc
from dash import dcc, html
from utils.valueBox import get_value_box

import utils.constants as C

header_card = dbc.Card(
    dbc.CardBody(
        [
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(options=[
                        {'label': 'Different top 50',
                         'value': 'Different_top_50.csv'},
                        {'label': 'Different genres',
                         'value': 'Different_genres.csv'},
                        {'label': 'Different modes',
                         'value': 'Different_modes.csv'},
                    ],
                        id=C.PRE_DROP,
                        placeholder="Select one of the predefined datasets"),
                ], width=3, style={"border-right": "2px solid #1DB954"}),
                dbc.Col([
                    dbc.Input(id=C.SEARCH_PHRASE,
                              type="text",
                              placeholder="search for artist/track/playlist",
                              style={"width": "100%"},
                              debounce=True),
                    dbc.RadioItems(options=[
                        {"label": "track", "value": "track"},
                        {"label": "playlist",
                         "value": "playlist"},
                        {"label": "album",
                         "value": "album"},
                    ],
                        value="track",
                        id=C.SEARCH_TYPE,
                        inline=True,
                        label_style={
                        "margin-right": "30px"},
                        inputStyle={"margin-right": "5px"})
                ], width=3),
                dbc.Col([
                    dbc.Button('Search', id=C.SEARCH_BUTTON, n_clicks=0,
                               style={"height": "90%"}, outline=True, color="info", className="me-1")
                ], width=1, style={"border-right": "2px solid #1DB954", 'text-align': 'center'}),
                dbc.Col([
                    dcc.Dropdown(options=[],
                                 id=C.UNDO_DROP,
                                 placeholder="Undo one of the steps"),
                ], width=2),
                dbc.Col([
                    dbc.Button('Reset', id=C.RESET_BUTTON, n_clicks=0, style={"height": "90%"},
                               outline=True, color="danger", className="me-1"),
                ], width=1, style={"border-right": "2px solid #1DB954", 'text-align': 'center'}),
                dbc.Col([
                    html.Img(
                        src="assets/logo_green.png", height="50px")
                ], width=2, style={'text-align': 'center'})
            ]),
        ], style={}
    )
)

radar_card = dbc.Card(
    dbc.CardBody(
        [
            dbc.Row(dcc.Dropdown(options=[
                {'label': "Average everything",
                 'value': 'average'},
                {'label': 'By query',
                 'value': 'by_query'},
                {'label': 'Each song separately (Mess, if you don\'t select some songs)',
                 'value': 'separate'},
            ],
                id=C.RADAR_DROPDOWN,
                placeholder="Select the behaviour of radar plot"),
            ),
            dbc.Row(dcc.Graph(id=C.RADAR))
        ]
    )
)

top_card = dbc.Card([
    dbc.CardBody([
        dbc.Col([
            dbc.Row([
                dcc.Slider(5, 20, 5,
                           value=10,
                           id=C.TOP_N_SLIDER),

                dbc.Col(dcc.Dropdown(options=[{'label': attr, "value": attr} for attr in C.NUMERICAL_COLUMNS],
                                     id=C.TOP_N_ATTR,
                                     placeholder="Top 5 in...")),

                dbc.Col(dcc.Dropdown(options=[{'label': attr, "value": attr} for attr in C.NUMERICAL_COLUMNS],
                                     id=C.TOP_N_COLOR,
                                     placeholder="color based on"),
                        )
            ]
            ),
            dbc.Row(
                dcc.Graph(id=C.TOP_N_PLOT))
        ], width=6, style={'width': '100%'})
    ])
])

parallel_lines_card = dbc.Card([
    dbc.CardBody([
        dbc.Col([
            dbc.Row(
                [
                    dbc.Col(dbc.Input(id=C.PARALLEL_COORDS_QUERIES,
                                      type="text",
                                      placeholder="Type id of query to be added/removed from the plot, e.g: 0",
                                      style={
                                          "width": "100%"},
                                      debounce=True), width=8),

                    dbc.Col(dbc.Button('Add/remove query', id=C.PARALLEL_COORDS_QUERIES_ADD, n_clicks=0,
                                       style={"height": "90%"}, outline=True, color="info", className="me-1"), width=3)
                ]),
            dbc.Row(dbc.Col(html.P(
                id=C.PARALLEL_COORDS_QUERIES_OPTIONS, children="Available options: "), width=8)),

            dbc.Row([
                dbc.Col(dbc.Input(id=C.PARALLEL_COORDS_ATTR,
                                  type="text",
                                  placeholder="Type name of attribute to be added/removed from the plot, e.g: danceability",
                                  style={
                                      "width": "100%"},
                                  debounce=True), width=8),
                dbc.Col(dbc.Button('Add/remove attr.', id=C.PARALLEL_COORDS_ATTR_ADD, n_clicks=0,
                                   style={"height": "90%"}, outline=True, color="info", className="me-1"), width=3)
            ]),
            dbc.Row(dbc.Col(html.P(id=C.PARALLEL_COORDS_ATTR_OPTIONS,
                                   children="Available options: " + " ".join(f"{v}," for v in C.NUMERICAL_COLUMNS)), width=11)),
            dbc.Row(
                dcc.Graph(id=C.PARALLEL_COORDS))
        ], width=6, style={'width': '100%'})
    ])
])

sun_card = dbc.Card([
    dbc.CardBody([
        dbc.Row(([
            dbc.Col([dbc.Input(id=C.SUNBURST_TEXT,
                               type="text",
                               placeholder="order of categorical variables separated by comma e.g mode, explicit, time_signature",
                               debounce=True),
                     html.P(f'available attributes: {", ".join(C.CATEGORICAL_COLUMNS)}')], width=8),
            dbc.Col(dbc.Button('Update', id=C.SUNBURST_SUBMIT, n_clicks=0,
                               style={"height": "90%"}, outline=True, color="info", className="me-1"), width=3),
            dcc.Graph(id=C.SUNBURST)
        ]))
    ])
], style={'margin-top': '15px'})


scatter_card = dbc.Card([
    dbc.CardBody([
        dbc.Row(([
            dbc.Col([
                html.P("x"),
                dcc.Dropdown(options=[attr for attr in C.NUMERICAL_COLUMNS],
                             id=C.SCATTER_X,
                             value=C.NUMERICAL_COLUMNS[0]),
                html.P("y"),
                dcc.Dropdown(options=[attr for attr in C.NUMERICAL_COLUMNS],
                             id=C.SCATTER_Y,
                             value=C.NUMERICAL_COLUMNS[1]),
                html.P("color"),
                dcc.Dropdown(options=[attr for attr in C.CATEGORICAL_COLUMNS],
                             id=C.SCATTER_COLOR,
                             value=C.CATEGORICAL_COLUMNS[0]),
                html.P("rug type"),
                dcc.Dropdown(options=["box", "violin", "rug", "histogram"],
                             id=C.SCATTER_RUG,
                             value="box"),

            ]),
            dbc.Col(dcc.Graph(id=C.SCATTER), width=9)

        ]))
    ])
], style={'margin-top': '15px'})


def get_layout(table, footers_definitions):
    layout =  dbc.Card([
                dbc.CardBody([
                    header_card,
                    dbc.Row([
                        dbc.Col([
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        dbc.Table(table)
                                    ]
                                )
                            )
                        ], width=6),
                        dbc.Col(radar_card, width=6)
                    ], style={'margin-top': '15px'}),  # style={"display": "none"} We could possibly use this to hide the graph entirely
                    dbc.Row([
                        dbc.Col(top_card),
                        dbc.Col(parallel_lines_card)
                    ], style={'margin-top': '15px'}),
                    sun_card,
                    scatter_card,
                    dbc.Row(
                        [dbc.Col(dbc.Card(get_value_box(**parameters), color='success', inverse=True)) 
                                                        for parameters in footers_definitions ],
                        className="mb-4",
                        id=C.FOOTER, style={'margin-top': '15px'}),
                ], style={'margin': '1% 10% 1% 10%', 'background': '#ECF0F5'})
    ], style={'background': '#ECF0F5'})

    return layout
