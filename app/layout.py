import dash_bootstrap_components as dbc
from dash import dcc, html
from utils.valueBox import get_value_box

import utils.constants as C

HELP = dcc.Markdown('''

    # Here the help will be placed
''')

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(
                            html.Img(src="assets/logo_no_bg.png", height="60ex")),
                    ],
                    align="left",
                    className="g-0",
                ),
                # href="NASZ ADRES POZNIEJ",
                style={"textDecoration": "none"},
            ),
            dbc.Button("Help", id="open", n_clicks=0),
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Welcome to Spotify Analyzer!"), style={'align':'center'}),
                    dbc.ModalBody(HELP),
                    dbc.ModalFooter(
                        dbc.Button(
                            "Close", id="close", className="ms-auto", n_clicks=0
                        )
                    ),
                ],
                id="modal",
                size='xl',
                scrollable=True,
                is_open=False,
            ),
        ]
    ),
    # color="dark",
    # dark=True,
)

search_card = dbc.Card(
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
                    html.P("LOADING")
                ], width=2, style={'text-align': 'center'})
            ]),
        ]
    ), style={'text-align': 'center'}
)

radar_card = dbc.Card(
    dbc.CardBody(
        [
            html.H2("General statistics"),
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
        ], style={'height': '100%', 'text-align': 'center'}
    )
)

top_card = dbc.Card([
    dbc.CardBody([
        dbc.Col([
            html.H2("Top 5 songs"),
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
        ], width=6, style={'width': '100%', 'height': '556px', 'text-align': 'center'})
    ], style={'text-align': 'center'})
])

parallel_lines_card = dbc.Card([
    dbc.CardBody([
        html.H2("Parallel Coordinates Plot"),
        dbc.Col([
            dbc.Row(dbc.Col(dbc.Checklist(options=[],
                                          id=C.PARALLEL_COORDS_QUERIES, inline=True))),

            dbc.Row(dbc.Col(dbc.Checklist(options=[{'label': x, 'value': x} for x in C.NUMERICAL_COLUMNS],
                                          id=C.PARALLEL_COORDS_ATTR, inline=True))),
            dbc.Row(
                dcc.Graph(id=C.PARALLEL_COORDS))
        ], width=6, style={'width': '100%', 'height': '508px'})
    ], style={'text-align': 'center'})
])

sun_card = dbc.Card([
    dbc.CardBody([
        html.H2("Compare data on a sunchart"),
        dbc.Row([
            dbc.Col([dbc.Input(id=C.SUNBURST_TEXT,
                               type="text",
                               placeholder="order of categorical variables separated by comma e.g mode, explicit, time_signature",
                               debounce=True),
                     html.P(f'available attributes: {", ".join(C.CATEGORICAL_COLUMNS)}')], width=11, style={'text-align': 'center'}),
            dbc.Col(dbc.Button('Update', id=C.SUNBURST_SUBMIT, n_clicks=0,
                               style={"height": "90%"}, outline=True, color="info", className="me-1"), width=1),
            dcc.Graph(id=C.SUNBURST)
        ], style={'margin': 'auto'})
    ], style={'text-align': 'center'})
], style={'margin-top': '15px'})


scatter_card = dbc.Card([
    dbc.CardBody([
        html.H2("Scatterplot"),
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
    ], style={'text-align': 'center'})
], style={'margin-top': '15px'})


def get_layout(table, footers_definitions):
    layout = dbc.Card([
        dbc.CardBody([
            navbar,
            search_card,
            dbc.Row(
                [dbc.Col(dbc.Card(get_value_box(**parameters), color='success', inverse=True))
                 for parameters in footers_definitions],
                className="mb-4",
                id=C.FOOTER, style={'margin-top': '15px'}),
            dbc.Row([
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H2("List of all songs"),
                                dbc.Table(table)
                            ], style={'text-align': 'center'}
                        )
                    )
                ], width=6, style={}),
                dbc.Col(radar_card, width=6, style={})
            ], style={'margin-top': '15px'}),  # style={"display": "none"} We could possibly use this to hide the graph entirely
            dbc.Row([
                dbc.Col(top_card),
                dbc.Col(parallel_lines_card)
            ], style={'margin-top': '15px'}),
            sun_card,
            scatter_card
        ], style={'margin': '0 6% 0 6%', 'background': '#ECF0F5'})
    ], style={'background': '#ECF0F5'})

    return layout
