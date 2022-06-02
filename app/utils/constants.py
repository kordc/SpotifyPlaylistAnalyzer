import dash_bootstrap_components as dbc

COLUMNS = ['name','album','artist', 'danceability',  'energy',  'speechiness', 
            'acousticness',  'liveness',  'valence', "duration", "explicit",
            "popularity", "instrumentalness", "key", "loudness",
            "time_signature"]

NUMERICAL_COLUMNS = ['danceability',  'energy',  'speechiness', 
                  'acousticness',  'liveness',  'valence', "duration",
                  "popularity", "energy", "instrumentalness", "loudness"]

FOOTERS = [
            {"title": "Number of minutes", "icon": "fa fa-clock fa-5x", "value": "", "figure": None},
            {"title": "Positiveness", "icon": "fa fa-heart fa-5x", "value": "", "figure": None},
            {"title": "Nothing", "icon": "fa fa-shield fa-5x", "value": "", "figure": None},    
          ]


EXTERNAL_STYLESHEETS = [dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME]

RADAR = "radar"
RADAR_DROPDOWN = "radar_dropdown"

UNDO_DROP = "undo"
TABLE = "table"
FOOTER = "footer"
SEARCH_PHRASE = "search_phrase"
SEARCH_TYPE = "search_type"
SEARCH_BUTTON = "search_data"
PRE_DROP = "predefined_datasets"
RESET_BUTTON = "reset_data"


TOP_N_PLOT = "top_n"
TOP_N_ATTR = "top_n_attr"
TOP_N_COLOR = "top_n_color"
TOP_N_SLIDER = "top_n_slider"