# Basics Requirements
import pathlib
import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_bootstrap_components as dbc


#Use the Datetime library
from datetime import datetime as dt
from datetime import date

# Recall app
from app import app
#Import the data
from df import df


###########################################################
#we create some variables necessary to build the different
#filter of the components
###########################################################

country = df['pais_residencia'].unique()
city = df['ciudad_residencia'].unique()
marital_status = df['estado_civil'].unique()
stratum = df['estrato'].unique()


dropdown_country =dcc.Dropdown(
    id='Dropdown_country',
    options=[{'label': i, 'value': i} for i in country],
    placeholder = 'Select ..'   
)

dropdown_city = dcc.Dropdown(
    id='Dropdown_city',
    options=[{'label': i, 'value': i} for i in city],
    placeholder = 'Select ..'
)

dropdown_maritalstatus = dcc.Dropdown(
    id='Dropdown_maritalstatus',
    options=[{'label': i, 'value': i} for i in marital_status],
    placeholder = 'Select ..'
)

dropdown_stratum = dcc.Dropdown(
    id='Dropdown_stratum',
    options=[{'label': i, 'value': i} for i in stratum],
    placeholder="Select .."
)


dropdown_modality = dcc.Dropdown(
    id='Dropdown_modality',
    options=[{'label': i, 'value': i} for i in ['Virtual', 'Presencial','Distancia']],
    placeholder="Select .."
 
)


drowpdown_sex = dcc.Dropdown(
    id='Dropdown_sex',
    options=[{'label': i, 'value': i} for i in ['Masculino', 'Femenino']],
    placeholder="Select .."  
)


##############################################################
# We organize each of the elements created in a new container.
##############################################################
sidebar_prob=html.Div(
    [   
        
        html.H5("Select Country"),
        dropdown_country,
        html.Hr(),
        html.Hr(),
        html.H5("Select City"),
        dropdown_city,
        html.Hr(),
        html.Hr(),
        html.H5("Select Modality"),
        dropdown_modality,
        html.Hr(),
        html.Hr(),
        html.H5("Select Gender"),
        drowpdown_sex,
        html.Hr(),
        html.Hr(),
        html.H5("Select Civil State"),
        dropdown_maritalstatus,
        html.Hr(),
        html.Hr(),
        html.H5("Stratum"),
        dropdown_stratum,
        html.Hr(),
    ],className='ds4a-sidebar'   
)
