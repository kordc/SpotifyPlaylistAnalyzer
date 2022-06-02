from dash_extensions.enrich import Output
import utils.constants as C
import pandas as pd
from plots import plots
import dash_bootstrap_components as dbc
from utils import valueBox
plots_generator = plots.Plots()


class OutputController:
    def __init__(self,):
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


    def update_state(self, element, key, value):
        self.state_control[element][key] = value

    def get_outputs(self, table=True, plots=True, undo=True, footer=True):
        outputs = []
        if table:
            outputs.append(Output(C.TABLE, "data"))
        if plots:
            outputs.append(Output(C.RADAR, "figure"))
            outputs.append(Output(C.TOP_N_PLOT, "figure"))
        if undo:
            outputs.append(Output(C.UNDO_DROP, "options"))
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
            radar_plot = plots_generator.radarPlot(rows_df, behaviour = self.state_control["radar"]["behaviour"])
            top_n_plot = plots_generator.topNTracks(rows_df)
            footers[0]["value"] = f"{rows_df['duration'].sum()} sec"
            footers[1]["figure"] = plots_generator.valenceGauge(rows_df)
        else:
            radar_plot = {}
            footers[0]["value"] = ""
            footers[1]["figure"] = None

        if table:
            results.append(rows)

        results.append(radar_plot)
        results.append(top_n_plot)

        if request_manager is not None:
            results.append(request_manager.get_options())

        if footers is not None:
            results.append(
                [   
                    dbc.Col(dbc.Card(valueBox.get_value_box(**parameters), color='success', inverse=True)) for parameters in footers
                ]
            )

        return tuple(results)