import pandas as pd
import plotly.express as px

from dash import dcc, html
from dash_extensions.enrich import Output, DashProxy, Input, MultiplexerTransform, State
import yaml
import tekore as tk
from spotifyData import getdata_faster
from plots import plots
from utils import request_manager, valueBox
from utils.constants import COLUMNS, FOOTERS, EXTERNAL_STYLESHEETS
import utils.constants as C
from table import get_table
from layout import get_layout
from utils.output_handler import OutputController
import dash_bootstrap_components as dbc


credentials_path = "credentials.yaml"
with open(credentials_path) as file:
    cred = yaml.load(file, Loader=yaml.FullLoader)


app_token = tk.request_client_token(cred['client_id'], cred['client_secret'])
spotify = tk.Spotify(app_token)

creator = getdata_faster.DatasetCreator(spotify_api=spotify)
plots_generator = plots.Plots()

request_manager = request_manager.RequestManager()
output_handler = OutputController()

app = DashProxy(prevent_initial_callbacks=True, transforms=[MultiplexerTransform()], external_stylesheets=EXTERNAL_STYLESHEETS)

table = get_table(columns=COLUMNS)

app.layout = get_layout(table=table, footers_definitions=FOOTERS)


#############################################################################################3
#############################################################################################
#! THESE CALLBACKS ARE SUPPOSED TO UPDATE ALMOST EVERYTHING AS THEY CHANGE DATA 
##############################################################################################
#############################################################################################
@app.callback(
    output_handler.get_outputs(table=True, plots=True, undo=True, footer=True),
    Input(C.PRE_DROP, 'value')
)
def load_predefined_data(path):
    request_manager.reset_requests()
    rows = pd.read_csv(path).to_dict("records")
    return output_handler.get_updated(rows, request_manager, table=True)

@app.callback(
    output_handler.get_outputs(table=True, plots=True, undo=True, footer=True),
    Input(C.UNDO_DROP, 'value'), State(C.TABLE, "data")
)
def undo_step(request_id, rows):
    new_rows = request_manager.remove_data(rows, request_id)
    return output_handler.get_updated(new_rows, request_manager, FOOTERS, table=True)

@app.callback(
    output_handler.get_outputs(table=True, plots=True, undo=True, footer=True),
    State(C.SEARCH_PHRASE, "value"), State(C.SEARCH_TYPE, "value"), State(C.TABLE, "data"),
    Input(C.SEARCH_BUTTON, "n_clicks")
)
def add_search_to_table(phrase, type_, rows, n_clicks):
    if n_clicks > 0:
        outcome = creator.search(phrase, type=type_)
        request_manager.add_data(rows, outcome, query_name=phrase) #! Thisk works in place
        request_manager.add_request(phrase)
        
        return output_handler.get_updated(rows, request_manager, FOOTERS, table=True)

@app.callback(
    output_handler.get_outputs(table=True, plots=True, undo=True, footer=True),
    Input(C.RESET_BUTTON, 'n_clicks'),
)
def reset_table(n_clicks):
    if n_clicks > 0:
        request_manager.reset_requests()
        return output_handler.get_updated(pd.DataFrame(columns=COLUMNS).to_dict("records"), request_manager, FOOTERS, table=True)

@app.callback(
    output_handler.get_outputs(table=False, plots=True, undo=False, footer=True),
    Input(C.TABLE, "data_previous"), State(C.TABLE, "data")
)
def update_at_removal(old_data, rows):
    return output_handler.get_updated(rows, None, FOOTERS, table=False)

@app.callback(
    output_handler.get_outputs(table=False, plots=True, undo=False, footer=True),
    Input(C.TABLE, "selected_rows"), State(C.TABLE, "data")
)
def only_selected_rows(selected_rows,rows):
    if selected_rows:
        rows = [rows[index] for index in selected_rows]
    return output_handler.get_updated(rows, None, FOOTERS, table=False)


@app.callback(
    output_handler.get_outputs(table=False, plots=True, undo=False, footer=True),
    Input(C.TABLE, "filter_query"), State(C.TABLE, "data")
)
def update_on_filter(query,rows):
    if query:
        key, _ , query_value = query.split(" ")
        key = key[1:-1]
        search = [key, query_value]
    else:
        search = None
    return output_handler.get_updated(rows, None, FOOTERS, table=False, search= search)

#############################################################################################3
#############################################################################################
#! THESE CALLBACKS ARE SUPPOSED TO UPDATE ONLY PLOTS + STATE IN THE UPDATE HANDLER AS THESE ARE PLOTS MODIFICATORS
##############################################################################################
#############################################################################################
@app.callback(
    Output(C.RADAR, "figure"),
    Input(C.RADAR_DROPDOWN, 'value'), State(C.TABLE, "data"), Input(C.TABLE, "selected_rows")
)
def update_radar(radar_behaviour ,rows, selected_rows):
    output_handler.update_state(element=C.RADAR, key="behaviour", value=radar_behaviour)

    if selected_rows:
        rows = [rows[index] for index in selected_rows]

    return plots_generator.radarPlot(pd.DataFrame(rows), radar_behaviour)

@app.callback(
    Output(C.TOP_N_PLOT, "figure"),
    Input(C.TOP_N_SLIDER, 'value'), Input(C.TOP_N_ATTR, 'value'),  Input(C.TOP_N_COLOR, 'value'), 
    State(C.TABLE, "data"), Input(C.TABLE, "selected_rows")
)
def update_top_n(n, attribute,color ,rows, selected_rows):
    if color is None: color = "energy"
    if attribute is None: attribute = "danceability"

    output_handler.update_state(element=C.TOP_N_PLOT, key="n", value=n)
    output_handler.update_state(element=C.TOP_N_PLOT, key="attribute", value=attribute)
    output_handler.update_state(element=C.TOP_N_PLOT, key="color", value=color)

    if selected_rows:
        rows = [rows[index] for index in selected_rows]

    return plots_generator.topNTracks(pd.DataFrame(rows), attribute=attribute, color=color, top_n = n)

if __name__ == "__main__":
    app.run_server(debug=True)