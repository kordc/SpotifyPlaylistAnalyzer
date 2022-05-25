import dash_bootstrap_components as dbc

COLUMNS = ['name','album','artist', 'danceability',  'energy',  'speechiness',  'acousticness',  'liveness',  'valence', "duration"]

FOOTERS = [
            {"title": "Number of minutes", "icon": "fa fa-clock fa-5x", "value": "", "figure": None},
            {"title": "Positiveness", "icon": "fa fa-heart fa-5x", "value": "", "figure": None},
            {"title": "Nothing", "icon": "fa fa-shield fa-5x", "value": "", "figure": None},    
          ]


EXTERNAL_STYLESHEETS = [dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME]

RADAR = "radar"
UNDO_DROP = "undo"
TABLE = "table"
FOOTER = "footer"
SEARCH_PHRASE = "search_phrase"
SEARCH_TYPE = "search_type"
SEARCH_BUTTON = "search_data"
PRE_DROP = "predefined_datasets"
RESET_BUTTON = "reset_data"