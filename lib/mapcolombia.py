# Basics Requirements
import pathlib
import dash
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px

# Dash Bootstrap Components
import dash_bootstrap_components as dbc

# Data
import math
import numpy as np
import datetime as dt
import pandas as pd
import json

# Recall app
from app import app
from lib import sidebar, header


###############################################################################
#This code block allows creating the container where the map will be graphed.
#Boostrap components are used to organize each of the elements.
###############################################################################

mapcolombia = html.Div(
    [
    dbc.Row([
        dbc.Col(  
           html.H4("Students per city"), width=10
        ),
        dbc.Col(
            dcc.Graph(figure={}, id='map_students_per_city'),width=10
        )
    ],justify="center",),

    ],className="ds4a-body",
)