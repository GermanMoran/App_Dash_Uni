import dash
import dash_table
from dash.dependencies import Input, Output, State, ClientsideFunction
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
from df import df

################################################################################
#This code block allows creating probability graphs to active students taking
# account the results of the model.
################################################################################

prob = html.Div(
    [
    dbc.Row([
             dbc.Col(
            dcc.Graph(figure={}, id='graph1')
            ),
            dbc.Col(
                dcc.Graph(figure={}, id='graph2')
            ),
    ]),
    dbc.Row([
       
        dbc.Col(
            dcc.Graph(figure={}, id='graph3'),className="graph-container"
                ),
        dbc.Col(
            dcc.Graph(figure={}, id='graph4'),className="graph-container"
        )
    ]),


    ],className="ds4a-body",
)
