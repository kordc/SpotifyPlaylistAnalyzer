from dash_extensions.enrich import Output
import utils.constants as C
import pandas as pd
from plots import plots
import dash_bootstrap_components as dbc
from utils import valueBox

class OutputController:
    def __init__(self, plots_generator):
        self.state_control = {
            C.RADAR: {
                "behaviour" : "average"
            },
            C.TOP_N_PLOT: {
                "n": 5,
                "attribute": "danceability",
                "color": "energy",
            }
        }
        self.plots_generator = plots_generator


    def update_state(self, element, key, value):
        self.state_control[element][key] = value

    def get_outputs(self, table=True, plots=True, undo=True, footer=True):
        outputs = []
        if table:
            outputs.append(Output(C.TABLE, "data"))
        if plots:
            outputs.append(Output(C.RADAR, "figure"))
            outputs.append(Output(C.TOP_N_PLOT, "figure"))
            outputs.append(Output(C.PARALLEL_COORDS, "figure"))
        if undo:
            outputs.append(Output(C.UNDO_DROP, "options"))
            outputs.append(Output(C.PARALLEL_COORDS_QUERIES, "options"))
        if footer:
            outputs.append(Output(C.FOOTER, "children"))

        return outputs

    def get_updated(self, rows: dict, request_manager=None, footers=None, table=True, search=None):
        results = []
        #print(rows)
        rows_df = pd.DataFrame(rows)
        if search is not None:
            key, query = search
            mask = rows_df[key].str.contains(query)
            rows_df = rows_df.loc[mask]
        if rows:
            radar_plot = self.plots_generator.radarPlot(rows_df, behaviour = self.state_control["radar"]["behaviour"])
            top_n_plot = self.plots_generator.topNTracks(rows_df)
            parallel_coords_plot = self.plots_generator.parallel_coordinates_plot(rows_df)

            footers[0]["value"] = f"{rows_df['duration'].sum()}"
            std = 0 if len(rows_df["tempo"]) == 1 else int(rows_df['tempo'].std())
            footers[1]["value"] = f"{int(rows_df['tempo'].mean())} +- {std}"
            footers[2]["value"] = f"{int(rows_df['explicit'].mean()*100)}%"
        else:
            radar_plot = {}
            top_n_plot = {}
            parallel_coords_plot = {}
            footers[0]["value"] = ""
            footers[1]["value"] = ""
            footers[2]["value"] = ""

        if table:
            results.append(rows)

        results.append(radar_plot)
        results.append(top_n_plot)
        results.append(parallel_coords_plot)

        if request_manager is not None:
            results.append(request_manager.get_options())
            results.append(request_manager.get_options())

        if footers is not None:
            results.append(
                [   
                    dbc.Col(dbc.Card(valueBox.get_value_box(**parameters), color='success', inverse=True)) for parameters in footers
                ]
            )

       
        return tuple(results)