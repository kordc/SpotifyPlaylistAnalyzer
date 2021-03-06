import pandas as pd
import plotly.express as px

from dash_extensions.enrich import Output, DashProxy, Input, MultiplexerTransform, State
import tekore as tk
from spotifyData import getdata_faster
from plots import plots
from utils import request_manager
from utils.constants import COLUMNS, FOOTERS, EXTERNAL_STYLESHEETS
import utils.constants as C
from table import get_table
from layout import get_layout
from utils.output_handler import OutputController

import os

cred={}
cred['client_id'] = os.getenv("SPOTIPY_CLIENT_ID")
cred['client_secret'] = os.getenv("SPOTIPY_CLIENT_SECRET")

app_token = tk.request_client_token(cred['client_id'], cred['client_secret'])
spotify = tk.Spotify(app_token)

creator = getdata_faster.DatasetCreator(spotify_api=spotify)
plots_generator = plots.Plots()
plots_generator.set_attr([C.NUMERICAL_COLUMNS[0]]) # This sets default attribute to show on plots

request_manager = request_manager.RequestManager()
output_handler = OutputController(plots_generator)

app = DashProxy(prevent_initial_callbacks=True, transforms=[MultiplexerTransform()], external_stylesheets=EXTERNAL_STYLESHEETS)

server = app.server

table = get_table(columns=COLUMNS)

app.title = "Spotify Analyzer"

app.layout = get_layout(table=table, footers_definitions=FOOTERS)


#############################################################################################3
#############################################################################################
#! THESE CALLBACKS ARE SUPPOSED TO UPDATE ALMOST EVERYTHING AS THEY CHANGE DATA 
##############################################################################################
#############################################################################################
@app.callback(
    output_handler.get_outputs(table=True, plots=True, undo=True, footer=True, value_parallel = True, loading=C.LOADING_PREDEFINED),
    Input(C.PRE_DROP, 'value')
)
def load_predefined_data(path):
    
    request_manager.reset_requests()
    rows = pd.read_csv(path)
    queries = []
    for query in rows["query"].unique():
        queries.append(request_manager.num_of_requests) # this is for parallel coordinates plot
        request_manager.add_request(query, "playlist")
    
    return output_handler.get_updated(rows.to_dict("records"), request_manager, FOOTERS, table=True, checklist_values=queries)

@app.callback(
    output_handler.get_outputs(table=True, plots=True, undo=True, footer=True, loading=C.LOADING_UNDO),
    Input(C.UNDO_DROP, 'value'), State(C.TABLE, "data")
)
def undo_step(request_id, rows):
    if request_id is not None:
        plots_generator.change_query(int(request_id)) # This is for parallel coordinates plot

    new_rows = request_manager.remove_data(rows, request_id)
    return output_handler.get_updated(new_rows, request_manager, FOOTERS, table=True)

@app.callback(
    output_handler.get_outputs(table=True, plots=True, undo=True, footer=True, value_parallel=True, loading=C.LOADING_SEARCH),
    State(C.SEARCH_PHRASE, "value"), State(C.SEARCH_TYPE, "value"), State(C.TABLE, "data"),
    Input(C.SEARCH_BUTTON, "n_clicks"), State(C.PARALLEL_COORDS_QUERIES, "value")
)
def add_search_to_table(phrase, type_, rows, n_clicks, checklist_values):
    if n_clicks > 0:
        outcome = creator.search(phrase, type=type_)
        request_manager.add_data(rows, outcome, query_name=phrase) #! Thisk works in place

        #This is for parallel coordinates plot
        if checklist_values is None: checklist_values = []
        query_id = 0 if type_ == "track" else request_manager.num_of_requests
        if query_id not in checklist_values:
            checklist_values.append(query_id)

        request_manager.add_request(phrase, type_)

        return output_handler.get_updated(rows, request_manager, FOOTERS, table=True, checklist_values = checklist_values)

@app.callback(
    output_handler.get_outputs(table=True, plots=True, undo=True, footer=True, loading=C.LOADING_RESET),
    Input(C.RESET_BUTTON, 'n_clicks'),
)
def reset_table(n_clicks):
    if n_clicks > 0:
        request_manager.reset_requests()
        plots_generator.set_query([])
        return output_handler.get_updated(pd.DataFrame(columns=COLUMNS).to_dict("records"), request_manager, FOOTERS, table=True)

@app.callback(
    output_handler.get_outputs(table=False, plots=True, undo=False, footer=True, loading=C.LOADING_REMOVAL),
    Input(C.TABLE, "data_previous"), State(C.TABLE, "data")
)
def update_at_removal(old_data, rows):
    return output_handler.get_updated(rows, None, FOOTERS, table=False)

@app.callback(
    output_handler.get_outputs(table=False, plots=True, undo=False, footer=True, loading=C.LOADING_SELECT),
    Input(C.TABLE, "selected_rows"), State(C.TABLE, "data")
)
def only_selected_rows(selected_rows,rows):
    if selected_rows:
        rows = [rows[index] for index in selected_rows]
    return output_handler.get_updated(rows, None, FOOTERS, table=False)


@app.callback(
    output_handler.get_outputs(table=False, plots=True, undo=False, footer=True, loading=C.LOADING_FILTER),
    Input(C.TABLE, "filter_query"), State(C.TABLE, "data")
)
def update_on_filter(query,rows):
    if query:
        #This querying system works weirdly I have to do some gymnastic with returned sentences to make it work
        query = query.split(" ")
        if len(query) == 2:
            key, query_value = query[0], query[1], (" ".join(query[2:])).replace('"','')
        else:
            key, _, query_value = query[0], query[1], (" ".join(query[2:])).replace('"','')
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
    Input(C.RADAR_DROPDOWN, 'value'), State(C.TABLE, "data"), State(C.TABLE, "selected_rows")

)
def update_radar(radar_behaviour ,rows, selected_rows):
    output_handler.update_state(element=C.RADAR, key="behaviour", value=radar_behaviour)

    if selected_rows:
        rows = [rows[index] for index in selected_rows]

    return plots_generator.radarPlot(pd.DataFrame(rows), radar_behaviour)

@app.callback(
    Output(C.TOP_N_PLOT, "figure"),
    Input(C.TOP_N_SLIDER, 'value'), Input(C.TOP_N_ATTR, 'value'),  Input(C.TOP_N_COLOR, 'value'), 
    State(C.TABLE, "data"), State(C.TABLE, "selected_rows")
)
def update_top_n(n, attribute,color ,rows, selected_rows):
    if color is None: color = "energy"
    if attribute is None: attribute = "danceability"

    output_handler.update_state(element=C.TOP_N_PLOT, key="n", value=n)
    output_handler.update_state(element=C.TOP_N_PLOT, key="attribute", value=attribute)
    output_handler.update_state(element=C.TOP_N_PLOT, key="color", value=color)

    if selected_rows:
        rows = [rows[index] for index in selected_rows]

    return plots_generator.topNTracks(pd.DataFrame(rows), attribute=attribute, color=color, n = n)

@app.callback(
    Output(C.PARALLEL_COORDS, "figure"), 
    Input(C.PARALLEL_COORDS_QUERIES, "value"), State(C.TABLE, "data"), State(C.TABLE, "selected_rows"))
def add_query(query, rows, selected_rows):
    plots_generator.set_query(sorted(query))

    if selected_rows:
        rows = [rows[index] for index in selected_rows]
    
    return plots_generator.parallel_coordinates_plot(pd.DataFrame(rows))

@app.callback(
    Output(C.PARALLEL_COORDS, "figure"), 
    Input(C.PARALLEL_COORDS_ATTR, "value"), State(C.TABLE, "data"), State(C.TABLE, "selected_rows"))
def add_attr(attr, rows, selected_rows):
    
    plots_generator.set_attr(attr)

    if selected_rows:
        rows = [rows[index] for index in selected_rows]
    
    return plots_generator.parallel_coordinates_plot(pd.DataFrame(rows))

@app.callback(
    Output(C.SUNBURST, "figure"), 
    Input(C.SUNBURST_SUBMIT, "n_clicks"), State(C.SUNBURST_TEXT, "value"), State(C.TABLE, "data"), State(C.TABLE, "selected_rows"))
def update_sunburst(n_clicks, path, rows, selected_rows):
    if n_clicks > 0: 
        print(path)
        plots_generator.sunburst_path = [x.strip() for x in path.split(",")]

        if selected_rows:
            rows = [rows[index] for index in selected_rows]
    
    return plots_generator.sunburst(pd.DataFrame(rows))

@app.callback(
    Output(C.SCATTER, "figure"),
    Input(C.SCATTER_X, "value"), Input(C.SCATTER_Y, "value"), Input(C.SCATTER_COLOR, "value"), Input(C.SCATTER_RUG, "value"), State(C.TABLE, "data"), State(C.TABLE, "selected_rows")
)
def update_scatter(x,y,color, rug_type, rows, selected_rows):
    if selected_rows:
            rows = [rows[index] for index in selected_rows]

    output_handler.update_state(element=C.SCATTER, key="x", value=x)
    output_handler.update_state(element=C.SCATTER, key="y", value=y)
    output_handler.update_state(element=C.SCATTER, key="color", value=color)
    output_handler.update_state(element=C.SCATTER, key="rug_type", value=rug_type)

    return plots_generator.scatter(pd.DataFrame(rows), x,y,color,rug_type)
    

@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


if __name__ == "__main__":
    app.run_server(debug=True)
