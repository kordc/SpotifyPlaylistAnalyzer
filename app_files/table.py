from dash import Dash, dash_table
import pandas as pd
import utils.constants as C

def get_table(columns):
    table = dash_table.DataTable(pd.DataFrame(columns=columns).to_dict("records"),
                            [{"name": i, "id": i} for i in columns[:4]],
                            #hidden_columns = columns[3:], This is not needed we can just omit not necesarry columns and data would be unchanged
                            id = C.TABLE,
                            fill_width=False,
                            style_table={
                            'height': '454px',
                            'overflowY': 'scroll',
                            },
                            #fixed_rows={'headers': True}, ! this breaks width 
                            page_action='none',  
                            style_data={
                            'whiteSpace': 'normal',
                            'height': 'auto',
                            'lineHeight': '15px'
                        },
                            filter_action="native",
                            #sort_action="native",
                            sort_mode="multi",
                            row_selectable="multi",
                            row_deletable=True,
                            editable=True, 
                            style_cell_conditional=[
                            {'if': {'column_id': 'rank'},
                            'width': '10%'},
        
                        ])

    return table
