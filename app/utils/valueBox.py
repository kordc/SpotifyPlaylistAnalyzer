
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc

def get_value_box(title, icon=None, value = "", figure = None):
    return [
        dbc.CardBody(
            [
               dbc.Row([
                   dbc.Col([html.H5(title, className="card-title"),
                        html.P(
                            value,
                            className="card-text",
                        )], width=9) if figure is None else dcc.Graph(title, figure=figure),
    
                dbc.Col(html.I(className=icon))
                
                ])
            ]),
    ]