
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc

def get_value_box(title : str, icon=None, value = "", figure = None):
    """This function return kind of falue box with font awesome icon at the right

    Args:
        title (str): Header of the value box
        icon (str, optional): font awesome icon search
        value (str, optional): Text inside
        figure (dict, optional): If you want you can place plotly dict inside

    Returns:
        dbc.CardBody: with the component inside
    """
    return [
        dbc.CardBody(
            [
               dbc.Row([
                   dbc.Col([html.H6(title, className="card-title"),
                        html.P(
                            value,
                            className="card-text", 
                            style={'font-weight': 'bold', 'font-size': '250%'}
                   )], width=9) if figure is None else dcc.Graph(title, figure=figure),
                dbc.Col(html.I(className=icon))
                ])
            ]),
    ]
