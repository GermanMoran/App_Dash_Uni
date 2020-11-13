# We define the requeriments
import dash
import os
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px

#Use the Datetime library
from datetime import datetime as dt
from datetime import date


# Recall app
from app import app


#######################################################################
#This block of code allows to show all the graphs and results
#taking into account each of the applied filters. 
#Boostrap components are used to organize the information.
######################################################################

stats = html.Div(
    [
    dbc.Row([
        dbc.Col(
            dcc.Graph(figure={}, id='students_per_gender'),width=4
        ),
        dbc.Col(
            dcc.Graph(figure={}, id='students_per_city'),width=4
        ),
        dbc.Col(
            dcc.Graph(figure={}, id='students_per_curse'),width=4
        )
    ],justify="center",),

    dbc.Row([
        dbc.Col(html.Div(
           dcc.Graph(figure={}, id='students_per_stratum'),className="graph-container"
        ),width=6   
        ),
        dbc.Col(html.Div(
            dcc.Graph(figure={}, id='students_per_averague'),className="graph-container"
        ),width=6      
        )
    ],justify="center",),

    ],className="ds4a-body",
)