from dash_extensions.enrich import Output
import utils.constants as C
import pandas as pd
from plots import plots
import dash_bootstrap_components as dbc
from utils import valueBox
plots_generator = plots.Plots()

def get_outputs(table=True, radar=True, undo=True, footer=True):
    outputs = []
    if table:
        outputs.append(Output(C.TABLE, "data"))
    if radar:
        outputs.append(Output(C.RADAR, "figure"))
    if undo:
        outputs.append(Output(C.UNDO_DROP, "options"))
    if footer:
        outputs.append(Output(C.FOOTER, "children"))

    return outputs

def get_updated(rows: dict, request_manager=None, footers=None, table=True, search=None):
    results = []

    rows_df = pd.DataFrame(rows)
    if search is not None:
        key, query = search
        mask = rows_df[key].str.contains(query)
        rows_df = rows_df.loc[mask]
        print(rows_df)
    if rows:
        plot = plots_generator.radarPlot(rows_df) 
        footers[0]["value"] = f"{rows_df['duration'].sum()} sec"
        footers[1]["figure"] = plots_generator.valenceGauge(rows_df)
    else:
        plot = {}
        footers[0]["value"] = ""
        footers[1]["figure"] = None

    if table:
        results.append(rows)

    results.append(plot)

    if request_manager is not None:
        results.append(request_manager.get_options())
    if footers is not None:
        results.append(
            [   
                dbc.Col(dbc.Card(valueBox.get_value_box(**parameters), color='success', inverse=True)) for parameters in footers
            ]
        )

    return tuple(results)