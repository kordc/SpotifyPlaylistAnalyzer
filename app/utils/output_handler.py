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
            },
            C.SCATTER: {
                "x": "danceability",
                "y": "liveness",
                "color": "mode",
                "rug_type": "box",
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
            outputs.append(Output(C.SUNBURST, "figure"))
            outputs.append(Output(C.SCATTER, "figure"))
        if undo:
            outputs.append(Output(C.UNDO_DROP, "options"))
            outputs.append(Output(C.PARALLEL_COORDS_QUERIES, "options"))
        if footer:
            outputs.append(Output(C.FOOTER, "children"))

        return outputs

    def get_updated(self, rows: dict, request_manager=None, footers=None, table=True, search=None):
        results = []
        rows_df = pd.DataFrame(rows)
        
        if search is not None:
            key, query = search
            print(key,query)
            print(rows_df[key])
            mask = rows_df[key].str.contains(query)
            rows_df = rows_df.loc[mask]
            print(rows_df)
        if rows:
            radar_plot = self.plots_generator.radarPlot(rows_df, behaviour = self.state_control["radar"]["behaviour"])
            top_n_plot = self.plots_generator.topNTracks(rows_df)
            parallel_coords_plot = self.plots_generator.parallel_coordinates_plot(rows_df)
            sunburst = self.plots_generator.sunburst(rows_df)
            scatter = self.plots_generator.scatter(rows_df, **self.state_control[C.SCATTER])

            footers[0]["value"] = f"{rows_df['duration'].sum()}"
            std = 0 if len(rows_df["tempo"]) == 1 else int(rows_df['tempo'].std())
            footers[1]["value"] = f"{int(rows_df['tempo'].mean())} (+/- {std})"
            footers[2]["value"] = f"{int(rows_df['explicit'].mean()*100)}%"
        else:
            radar_plot = {}
            top_n_plot = {}
            parallel_coords_plot = {}
            sunburst = {}
            scatter = {}
            footers[0]["value"] = ""
            footers[1]["value"] = ""
            footers[2]["value"] = ""

        if table:
            results.append(rows)

        results.append(radar_plot)
        results.append(top_n_plot)
        results.append(parallel_coords_plot)
        results.append(sunburst)
        results.append(scatter)

        if request_manager is not None:
            results.append(request_manager.get_options())
            results.append([ {'label': f"{k}: {v['label']}", "value": k} for k,v in request_manager.requests.items() ])

        if footers is not None:
            results.append(
                [   
                    dbc.Col(dbc.Card(valueBox.get_value_box(**parameters), color='success', inverse=True)) for parameters in footers
                ]
            )

       
        return tuple(results)