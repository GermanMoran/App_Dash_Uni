# Basics Requirements

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

###########################################################################################################
#This code allows to create the information tables of the students, taking into account each of the filters,
#it also allows the query of a particular student. The elements are organized by  row and column of boostrap
#components.
###########################################################################################################

datatable = html.Div(
    [dcc.Input(
            id='input_student_id',
            type='number',
            placeholder='type student id',
    ),
    html.Hr(),
    dbc.Row([
            dbc.Col(
                dash_table.DataTable(                               #spreadsheet
                    id='datatable_interactivity',                   #component id
                    data=df.to_dict('records'),                     #dataframe to dict
                    columns=[{"name": i, "id": i, "selectable": True} for i in df.columns],
                    editable=True,
                    sort_action='native',
                    row_selectable='single',
                    selected_rows=[0],
                    page_action='native',        #when you define page current and size, this parameter is 'native'
                    page_current=0,              #the default page is the first
                    page_size=8,                 #number of rows per page
                    style_table={'overflowX': 'auto'},
                    style_header={'backgroundColor': 'rgb(30, 30, 30)'},
                    style_cell={
                    'backgroundColor': '#1f2630',
                    'color': '7FDBFF'},
                ),
                width={'size': 8}
            ),
            dbc.Col(
                dcc.Graph(figure={}, id='pieplot_dropout')
            ),
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Graph(figure={}, id='barplot_average')
        ),
        dbc.Col(
            dcc.Graph(figure={}, id='barplot_number_courses')
        ),
        dbc.Col(
            dcc.Graph(figure={}, id='lineplot_number_courses')
        )
    ]),

    ],className="ds4a-body",
)
