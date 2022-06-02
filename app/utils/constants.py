import dash_bootstrap_components as dbc

COLUMNS = ['name','album','artist', 'danceability',  'energy',  'speechiness', 
            'acousticness',  'liveness',  'valence', "duration", "explicit",
            "popularity", "instrumentalness", "key", "loudness",
            "time_signature", "tempo"]

NUMERICAL_COLUMNS = ['danceability',  'energy',  'speechiness', 
                  'acousticness',  'liveness',  'valence', "duration",
                  "popularity", "energy", "instrumentalness", "loudness", "tempo"]

PARALLEL_ATTR = COLUMNS[3:]

FOOTERS = [
            {"title": "Number of minutes", "icon": "fa fa-clock fa-5x", "value": "", "figure": None},
            {"title": "Mean of the BPM", "icon": "fa fa-heart fa-5x", "value": "", "figure": None},
            {"title": "Percentage of explicit songs", "icon": "fa fa-exclamation fa-5x", "value": "", "figure": None},    
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

PARALLEL_COORDS = "parallel_coords"
PARALLEL_COORDS_ATTR = "parallel_coords_attr"
PARALLEL_COORDS_ATTR_RESET = "parallel_coords_attr_reset"
PARALLEL_COORDS_QUERIES = "parallel_coords_queries"
PARALLEL_COORDS_QUERIES_RESET = "parallel_coords_queries_reset"