# Basics Requirements
import pathlib
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


###########################################################
#
#           APP LAYOUT:
#
###########################################################

# LOAD THE DIFFERENT FILES
from lib import sidebar, header, datatable
from df import df, df_all_periods

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

navbar = dbc.Navbar(
    [
        #dbc.Col(dbc.NavbarBrand("Uniremington", href="#"), sm=3, md=2),
        dbc.NavbarToggler(id="navbar-toggler1"),
       
            dbc.Row(
                    [    
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.NavItem(dbc.NavLink("Home",  href="#")),
                        dbc.NavItem(dbc.NavLink("Model",  href="#")),
                        dbc.NavItem(dbc.NavLink("About",  href="#"))
                        
                    ],
                    className="mr-auto",
            ),
    ]
)


# PLACE THE COMPONENTS IN THE LAYOUT
# Create Layout
app.layout = html.Div(
    [navbar, header.header,sidebar.sidebar,datatable.datatable],
    className="ds4a-app",  # You can also add your own css files by locating them into the assets folder
)


# Creates the title of the app


###############################################
#
#           APP INTERACTIVITY:
#
###############################################

@app.callback(
    Output(component_id='datatable_interactivity', component_property='data'),
    [Input(component_id='input_student_id', component_property='value'),
     Input(component_id='Dropdown_country', component_property='value'),
     Input(component_id='Dropdown_city', component_property='value'),
     Input(component_id='Dropdown_modality', component_property='value'),
     Input(component_id='Drowpdown_state', component_property='value'),
     Input(component_id='Dropdown_sex', component_property='value'),
     Input(component_id='Dropdown_maritalstatus', component_property='value'),
     Input(component_id='Dropdown_stratum', component_property='value'),
     Input(component_id='RangeSlider_age', component_property='value'),
     Input(component_id='my-date-picker-range', component_property='start_date'),
     Input(component_id='my-date-picker-range', component_property='end_date'),
     Input(component_id='datatable_interactivity', component_property='selected_rows')]
)
def update_table(student_id_selected, pais_selected, ciudad_selected, modalidad_selected, estado_selected,
                 sexo_selected, estado_civil_selected, estrato_selected, edad_selected, fecha_start_selected,fecha_end_selected,student_selected):
    new_df = df.copy()

    # lista de paises
    if student_id_selected is not None:
        new_df = new_df[new_df['identificador_estudiante'] == student_id_selected]

    # lista de paises
    if pais_selected is not None:
        new_df = new_df[new_df['pais_residencia'] == pais_selected]

    # lista de ciudades
    if ciudad_selected is not None:
        new_df = new_df[new_df['ciudad_residencia'] == ciudad_selected]

    # check box de modalidad
    if modalidad_selected is not None:
        if len(modalidad_selected) != 0:
            new_df = new_df[new_df['modalidad'] == modalidad_selected]

    # check box de estado
    if estado_selected is not None:
        if len(estado_selected) != 0:
            new_df = new_df[new_df['estado_plan_estudio'] == estado_selected]

    # check box de sexo
    if sexo_selected is not None:
        if len(sexo_selected) != 0:
            new_df = new_df[new_df['sexo'] == sexo_selected]

    # lista de estado civil
    if estado_civil_selected is not None:
        new_df = new_df[new_df['estado_civil'] == estado_civil_selected]

    # lista de estrato
    if estrato_selected is not None:
        new_df = new_df[new_df['estrato'] == estrato_selected]

    # slider de edad
    new_df = new_df[(new_df['edad'] >= edad_selected[0]) & (new_df['edad'] <= edad_selected[1])]

    # caledar fecha
    new_df = new_df[(new_df['fecha_ingreso'] >= fecha_start_selected) & (new_df['fecha_ingreso'] <= fecha_end_selected)]

    return new_df.to_dict('records')

@app.callback(
    [Output(component_id='total_students', component_property='children'),
     Output(component_id='active_students', component_property='children'),
     Output(component_id='inactive_students', component_property='children'),
     ],
    [Input(component_id='datatable_interactivity', component_property='selected_rows')]
)
def update_table(student_selected):
    if student_selected == None:
        label_total = 0
        label_activo = 0
        label_inactivo = 0
    else:
        student_df = df.iloc[student_selected, :]
        label_total = 1
        if 'Inactivo' in student_df.estado_plan_estudio:
            label_activo = 0
            label_inactivo = 1
        else:
            label_activo = 1
            label_inactivo = 0
    return label_total, label_activo, label_inactivo

@app.callback(
    [Output(component_id='barplot_average', component_property='figure'),
     Output(component_id='barplot_number_courses', component_property='figure'),
     Output(component_id='pieplot_dropout', component_property='figure')],
    [Input(component_id='datatable_interactivity', component_property='selected_rows'),
     Input(component_id='datatable_interactivity', component_property='data')
     ]
)
def update_graph(student_selected,data):
    new_df = pd.DataFrame(data)
    if student_selected == None or new_df.empty:
        return {}
    else:
        col_periodo = [col for col in df_all_periods.columns if col.startswith('periodo_')]
        col_promedio = [col for col in df_all_periods.columns if col.startswith('promedio_periodo_')]
        col_matriculados = [col for col in df_all_periods.columns if col.startswith('cursos_matriculados_')]
        col_reprobados = [col for col in df_all_periods.columns if col.startswith('cursos_reprobados_')]
        col_cancelados = [col for col in df_all_periods.columns if col.startswith('cursos_cancelados_')]

        #average grade
        student_id_selected = int(new_df.loc[student_selected,'identificador_estudiante'])
        array_periodo = df_all_periods.loc[df_all_periods.identificador_estudiante == student_id_selected, col_periodo].to_numpy()[0]
        array_periodo = array_periodo[array_periodo != None] + ' s'

        array_promedio = df_all_periods.loc[df_all_periods.identificador_estudiante == student_id_selected, col_promedio].to_numpy()[0]
        array_promedio = array_promedio[array_promedio != None]

        barplot = px.bar(x=array_periodo[:len(array_promedio)], y=array_promedio,labels = {'x' : 'Period','y':'Average grade'},range_y = [0,5])

        #number of courses per period
        array_matriculados = df_all_periods.loc[df_all_periods.identificador_estudiante == student_id_selected, col_matriculados].to_numpy()[0]
        array_matriculados = array_matriculados[array_matriculados != None]

        array_reprobados = df_all_periods.loc[df_all_periods.identificador_estudiante == student_id_selected, col_reprobados].to_numpy()[0]
        array_reprobados = array_reprobados[array_reprobados != None]

        array_cancelados = df_all_periods.loc[df_all_periods.identificador_estudiante == student_id_selected, col_cancelados].to_numpy()[0]
        array_cancelados = array_cancelados[array_cancelados != None]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=array_periodo[:len(array_promedio)], y=array_matriculados,
                                 mode='lines',
                                 name='Matriculados'))
        fig.add_trace(go.Scatter(x=array_periodo[:len(array_promedio)], y=array_reprobados,
                                 mode='lines',
                                 name='Reprobados'))
        fig.add_trace(go.Scatter(x=array_periodo[:len(array_promedio)], y=array_cancelados,
                                 mode='lines',
                                 name='Cancelados'))
        

        #prob dropout
        dropout = px.pie(values = [0.3,0.7],names =['No dropout','dropout'])
        # Agrgando color a los graficos
        colors = {
        'background': '#1f2630',
        'text': '#7FDBFF'
        }

    
        # Actualizacionde los graficos color
        barplot.update_layout(plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['text'])
        fig.update_layout(plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['text'])
        dropout.update_layout(plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['text'])


      

        return barplot, fig, dropout


###############################################################
# Load and modify the data that will be used in the app.
#################################################################

if __name__ == "__main__":
    app.run_server(debug=True)