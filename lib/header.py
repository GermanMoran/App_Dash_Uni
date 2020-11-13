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



#Some variables to be used in the components are defined: DatePickerRange and RangeSlider.
min_date = df.fecha_ingreso.min()
max_date = df.fecha_ingreso.max()
min_edad = df.edad.min()
max_edad = df.edad.max()

#################################################################################################################
#This block of code allows you to build the header of the main page,
#boostrap components are used to organize each of the elements.This header has two inputs and Three outputs.
# The inputs are:
# - DatePickerRange : It allows yoy to generate a calendar, taking into account the academic dates of the dataset
# - RangeSlider     : It allows you  to generate a slider and select the age range of the people in the dataset.
# The Output are:
# - html-Div components that allow showing the number of total students, active students and inactive students.
################################################################################################################
header = html.Div(
    [
    dbc.Row([
        dbc.Col(
            html.Div([
            html.Hr(),
            html.H5("Admission Date"),
            dcc.DatePickerRange(
            id='my-date-picker-range',
            min_date_allowed= min_date,
            max_date_allowed= max_date,
            start_date=df.fecha_ingreso.min(),
            end_date=df.fecha_ingreso.max(),
            #start_date=date(2015, 1, 1),
            #end_date=date(2020, 1, 1),
            style ={
                'backgroundColor': '#1f2630',
                'color': '7FDBFF'}
            )
            ],className="date_picker"),width=4
        ),         
            

        dbc.Col(
            html.Div([
            html.Hr(),
            html.H5("Age"),
            dcc.RangeSlider(
            id="RangeSlider_age",
            min=df["edad"].min(),
            max=df["edad"].max(),
            value=[df["edad"].min(), df["edad"].max()],
            marks={15: {'label': '15'},
            30: {'label': '30'},
            45: {'label': '45'},
            60: {'label': '60'},
            78: {'label': '78'}
            },        
            step=1,
            updatemode = 'drag')
            ],className="header-box"), width=2
        ),

        dbc.Col(
            html.Div([
                html.Hr(),
                html.H5("Number of students"),
                html.Div(id ="total_students")
            ],className="header-box"),width=2
        ),

        dbc.Col(
            html.Div([
            html.Hr(),
            html.H5("Active students"),
            html.Div(id = "active_students")
            ],className="header-box"),width=2
        ),

        dbc.Col(
            html.Div([
            html.Hr(),
            html.H5("Inactive students"),
            html.Div(id = "inactive_students")
            ],className="header-box"),width=2
        )
               
    ])
    ], className="ds4a-header")
