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

from lib import sidebar, header, mapcolombia
from df import df



# Read of jeson file
with open('data/colombia.json',encoding="UTF-8") as file:
    file_geo = json.load(file)



navbar = dbc.Navbar(
    [
        dbc.NavbarToggler(id="navbar-toggler1"),
       
            dbc.Row(
                    [    
                        dbc.Col(html.Img(src=app.get_asset_url("icono.png"), height="40px")),
                        dbc.NavItem(dbc.NavLink("Home",  href="#")),
                        dbc.NavItem(dbc.NavLink("Model",  href="#")),
                        dbc.NavItem(dbc.NavLink("About",  href="#"))
                        
                    ],
                    className="mr-auto",
            ),
    ]
)


# PLACE THE COMPONENTS IN THE LAYOUT
app.layout = html.Div(
    [navbar,header.header, sidebar.sidebar, mapcolombia.mapcolombia],
    className="ds4a-app",
)


@app.callback(
    [
    Output("total_students",'children'),
    Output("active_students",'children'),
    Output("inactive_students",'children'),
    Output("map_students_per_city",'figure')
    ],

    [Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('RangeSlider_age', 'value'),
    Input('Dropdown_maritalstatus','value'),     
    Input('Dropdown_stratum','value'),           
    Input('Dropdown_sex','value'),
    Input('Dropdown_modality','value'),
    Input('Dropdown_country','value'),
    Input('Dropdown_city','value'),
    Input('Drowpdown_state','value')                
    ],
)


def update_output(start_date, end_date, edad, var1,var2,var3,var4,var5,var6,var7):

    dff = (df[(df['fecha_ingreso'] >= start_date) & (df['fecha_ingreso'] < end_date)
    & (df['edad'] >= edad[0]) & (df['edad'] < edad[1]) 
    & (df['estado_civil'].isin([var1]) == True if var1 != None else df['estado_civil'].isin([var1]) == False)
    & (df['estrato'].isin([var2]) == True if var2 != None else df['estrato'].isin([var2]) == False)
    & (df['sexo'].isin([var3]) == True if var3 != None else df['sexo'].isin([var3]) == False)
    & (df['modalidad'].isin([var4]) == True if var4 != None else df['modalidad'].isin([var4]) == False)
    & (df['pais_residencia'].isin([var5]) == True if var5 != None else df['pais_residencia'].isin([var5]) == False)
    & (df['ciudad_residencia'].isin([var6]) == True if var6 != None else df['ciudad_residencia'].isin([var6]) == False)
    & (df['estado_plan_estudio'].isin([var7]) == True if var7 != None else df['estado_plan_estudio'].isin([var7]) == False)
    ])
    

    total_students = len(dff)

    if var7 == None:
        total_active_students = len(dff[dff["estado_plan_estudio"].isin(["Activo"])])
        total_inactive_students = len(dff[dff["estado_plan_estudio"].isin(["Inactivo"])])

    elif var7 == 'Activo':
        total_active_students = len(dff)
        total_inactive_students = 0
    
    elif var7 == 'Inactivo':
        total_active_students = 0
        total_inactive_students = len(dff)
    
    elif var7 is not ['Activo','Inactivo']:
        total_active_students = 0
        total_inactive_students = len(dff)


    ciudad = (dff.groupby(["ciudad_residencia"]).count()[["identificador_estudiante"]].reset_index().
    rename(columns={"identificador_estudiante": "cantidad"}).sort_values(by=["cantidad"],ascending = False))


    colors = {
    'background': '#1f2630',
    'text': '#7FDBFF'
    }

    
    # Map Graph
    Map_colombia=px.choropleth_mapbox(ciudad,                         
        locations='ciudad_residencia',
        featureidkey='properties.MPIO_CNMBR',                   
        color='cantidad',                            
        geojson=file_geo,                          
        zoom=3.5,                                   
        mapbox_style="carto-positron",            
        center={"lat": 4.570868, "lon": -74.297333}, 
        color_continuous_scale="Viridis",
        hover_data=['cantidad'],
        opacity=0.5,                  
    )

    


    return [total_students, total_active_students,total_inactive_students, Map_colombia]
    
if __name__ == "__main__":
    app.run_server(debug=True)