# Basics Requirements
import pathlib
import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
import dash_bootstrap_components as dbc

# Data
import math
import numpy as np
import datetime as dt
import pandas as pd
import json

# Recall app
from app import app
from app import server


# LOAD THE DIFFERENT FILES
from lib import sidebar, header, stats,datatable,header_stu,header_map, mapcolombia, prob, sidebar_prob,header_prob


##############################################################
#We load the dataset.
##############################################################
from df import df,df_all_periods

#############################################################
# We load the json file to graph the map on the map page
############################################################
with open('data/colombia.json',encoding="UTF-8") as file:
    file_geo = json.load(file)

###############################################################################
#We define the path of the main page, which will allow navigation between pages
###############################################################################
app.layout=html.Div([
    dcc.Location(id='url', refresh=False,pathname="/general"),
    html.Div(id='page-content')
])

###################################################################################################
#######################################  First Page ##############################################
#Create the first navigation menu, which has four options:
#Review page: Provides basic information about the dataset and allows you to make different filters.
#Student's page: Provides specific information on a particular student and presents the probability 
#disservice of student taking into account the results of the model.
#Map page: Provides information from the dataset, taking into account the city of residence students.
#About: Provides basic information about the project.
###################################################################################################


navbar = dbc.Navbar(
    [
        dbc.NavbarToggler(id="navbar-toggler1"),
        dbc.Collapse(
            dbc.Row(
                    [  
                       dbc.Col(html.Img(src=app.get_asset_url("icono.png"), height="40px")),
                       dbc.NavItem(dbc.NavLink("Review page", disabled=True, href="#")),
                       dbc.NavItem(dbc.NavLink("Student's page", href="/students")),
                       dbc.NavItem(dbc.NavLink("Map page", href="/map")),
                       dbc.NavItem(dbc.NavLink("View's page", href="/view")),       
                    ],
                    className="mr-auto",
            ),
            id="navbar-collapse1",
            navbar=True,
        ),
    ]
)

#################################################################
# We organize the components of the Main page called review_page.
#################################################################
review_page= html.Div(
    [navbar, header.header, sidebar.sidebar, stats.stats],
    className="ds4a-app", )


#############################################################################################################
#This block of code allows to create the interaction of the reviw page: Where there are 8 outputs
#of which 5 are graphics and 3 labels that show the status of the students. In addition, there are 10 inputs,
#referring to variables such as:  age,sex stratum, modality, country, among others.
#############################################################################################################

@app.callback(
    [Output("students_per_city", "figure"),
    Output("students_per_gender", "figure"),
    Output("students_per_curse", "figure"),
    Output("students_per_stratum", "figure"),
    Output("students_per_averague", "figure"),
    Output("total_students",'children'),
    Output("active_students",'children'),
    Output("inactive_students",'children')
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

############################################################################################################
#This block is one of the most important because it allows you to filter the information taking into account
#each of the selected filters.
############################################################################################################

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
    ###################################################################################################################
    #This code allows to calculate the total number of students, active students, inactive students taking into account 
    # the applied filters
    ###################################################################################################################
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

    ##############################################################################
    #Once the information is filtered, groupings are made to generate the graphics
    ##############################################################################
    #Grouping for ciudad_residencia
    dfp = (dff.groupby(["ciudad_residencia"]).count()[["identificador_estudiante"]]
    .sort_values(by = ['identificador_estudiante'], ascending = False).reset_index()
    .rename(columns={"identificador_estudiante":"quantity"}).head(10))

    #Grouping for sexo
    dfs = (dff.groupby(["sexo"]).count()[["identificador_estudiante"]]
    .sort_values(by = ['identificador_estudiante'], ascending = False).reset_index()
    .rename(columns={"identificador_estudiante":"quantity"}).head(10))
    
    #Grouping for codigo_plan estudio
    dfc = (dff.groupby(["codigo_plan_estudio"]).count()[["identificador_estudiante"]]
    .sort_values(by = ['identificador_estudiante'], ascending = True).reset_index()
    .rename(columns={"identificador_estudiante":"quantity"}).tail(10))

    #Grouping for sratum and estado_plan estudio
    dfe = (dff.groupby(["estrato","estado_plan_estudio"]).count()[["identificador_estudiante"]]
    .sort_values(by = ['identificador_estudiante'], ascending = False)
    .rename(columns={"identificador_estudiante":"quantity"}).reset_index())
    

    # Main Graphs
    bar_students_city = px.bar(dfp, x='ciudad_residencia', y='quantity', height=400, title='Students per city',labels = {'ciudad_residencia' : 'City'})
    pie_gender = px.pie(dfs, values='quantity', names='sexo', height=400,title='Students per Gender')
    bar_students_course = px.bar(dfc, x='quantity', y='codigo_plan_estudio',orientation='h', height=400, title='Students per course',labels = {'codigo_plan_estudio' : 'Course'})
    
    if dfe.empty:
        bar_students_stratum = px.bar(dfe, x="estrato", y="quantity",height=400, title='Students per stratum',labels = {'estrato' : 'Stratum'})
    else:
        bar_students_stratum = px.bar(dfe, x="estrato", y="quantity", color='estado_plan_estudio', height=400, title='Students per stratum',labels = {'estrato' : 'Stratum'})

    if dff.empty:
        graph_aver = px.histogram(dff, x="promedio", height=400, title='Average of students',labels = {'promedio' : 'Average'})
    else:
        graph_aver = px.histogram(dff, x="promedio", color="estado_plan_estudio", height=400, title='Average of students',labels = {'promedio' : 'Average'})
     
    
    ###########################################
    # we define the colors to update the graphs
    ###########################################
  
    colors = {
    'background': '#1f2630',
    'text': '#7FDBFF'
    }
    
  
    # We update the graphics according to the selected colors
    bar_students_city.update_layout(plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['text'])
    pie_gender.update_layout(plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['text'])
    bar_students_course.update_layout(plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['text'])
    bar_students_stratum.update_layout(plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['text'])
    graph_aver.update_layout(plot_bgcolor=colors['background'],paper_bgcolor=colors['background'],font_color=colors['text'])
    

    return [bar_students_city, pie_gender, bar_students_course, bar_students_stratum, graph_aver, total_students, total_active_students,total_inactive_students]




###########################
##### SECOND PAGE #########
###########################

##############################################################################
# We create the new navbar 
############################################################################## 
navbar1 = dbc.Navbar(
    [
        dbc.NavbarToggler(id="navbar-toggler1"),
        dbc.Collapse(
            dbc.Row(
                [      
                       dbc.Col(html.Img(src=app.get_asset_url("icono.png"), height="40px")),
                       dbc.NavItem(dbc.NavLink("Review page",  href="/general")),
                       dbc.NavItem(dbc.NavLink("Student's page", disabled=True, href="#")),
                       dbc.NavItem(dbc.NavLink("Map page",  href="/map")),
                       dbc.NavItem(dbc.NavLink("view's page",  href="/view"))
                ],
                className="mr-auto",
            ),
            id="navbar-collapse1",
            navbar=True,
        ),
    ]
)


###################################################################################
#We organize the components in the layaut, we keep the same structure of the 
#previous page, we use sidebar and header_stu to filter the information, but now we 
#use the datatable component that shows specific information about the students and 
#the results of the model.
#####################################################################################
student_page= html.Div(
    [navbar1, header_stu.header_stu, sidebar.sidebar, datatable.datatable],
    className="ds4a-app",
)

####################################################################################
#We create the interactivity for the table, taking into account each of the applied 
# filters,the table changes with the use of any filter.
####################################################################################
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
    
    # Create a copy of DF
    new_df = df.copy()

    # Filter to select to student
    if student_id_selected is not None:
        new_df = new_df[new_df['identificador_estudiante'] == student_id_selected]

    # list of countries
    if pais_selected is not None:
        new_df = new_df[new_df['pais_residencia'] == pais_selected]

    # list of cities
    if ciudad_selected is not None:
        new_df = new_df[new_df['ciudad_residencia'] == ciudad_selected]

    # check box de modality
    if modalidad_selected is not None:
        if len(modalidad_selected) != 0:
            new_df = new_df[new_df['modalidad'] == modalidad_selected]

    # check box de status study plan
    if estado_selected is not None:
        if len(estado_selected) != 0:
            new_df = new_df[new_df['estado_plan_estudio'] == estado_selected]

    # check box de sex
    if sexo_selected is not None:
        if len(sexo_selected) != 0:
            new_df = new_df[new_df['sexo'] == sexo_selected]

    # lista marital status
    if estado_civil_selected is not None:
        new_df = new_df[new_df['estado_civil'] == estado_civil_selected]

    # lista stratum
    if estrato_selected is not None:
        new_df = new_df[new_df['estrato'] == estrato_selected]

    # slider of age
    new_df = new_df[(new_df['edad'] >= edad_selected[0]) & (new_df['edad'] <= edad_selected[1])]

    # caledar fecha
    new_df = new_df[(new_df['fecha_ingreso'] >= fecha_start_selected) & (new_df['fecha_ingreso'] <= fecha_end_selected)]

    return new_df.to_dict('records')


@app.callback(
    [Output(component_id='total_students1', component_property='children'),
     Output(component_id='active_students1', component_property='children'),
     Output(component_id='inactive_students1', component_property='children'),
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

####################################################################################
#We create the interactivity of the another graphs that show ,Mean of the student
#selected during all the periods, the number of courses enrolled in each period and the 
#probability of disservice.
####################################################################################
@app.callback(
    [Output(component_id='barplot_average', component_property='figure'),
     Output(component_id='barplot_number_courses', component_property='figure'),
     Output(component_id='lineplot_number_courses', component_property='figure'),
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
        

        #We define the colors
        colors = {
        'background': '#1f2630',
        'text' : '#7FDBFF'
        }
        #We create the graphs and upadte the characteristics.
        barplot = px.bar(x=array_periodo[:len(array_promedio)], y=array_promedio,labels = {'x' : 'Period','y':'Average grade'},range_y = [0,5])
        barplot.update_layout(
            title_text='Average grade per period',
            title_x=0.5,
            autosize=False,
            width=350,
            height=300,
            margin=dict(
                l=20,
                r=20,
                b=20,
                t=30
            ),
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text'],
        )
        #number of courses per period
        array_matriculados = df_all_periods.loc[df_all_periods.identificador_estudiante == student_id_selected, col_matriculados].to_numpy()[0]
        array_matriculados = array_matriculados[array_matriculados != None].astype('float')

        array_reprobados = df_all_periods.loc[df_all_periods.identificador_estudiante == student_id_selected, col_reprobados].to_numpy()[0]
        array_reprobados = array_reprobados[array_reprobados != None].astype('float')

        array_cancelados = df_all_periods.loc[df_all_periods.identificador_estudiante == student_id_selected, col_cancelados].to_numpy()[0]
        array_cancelados = array_cancelados[array_cancelados != None].astype('float')

        array_aprobados = array_matriculados - array_cancelados - array_reprobados
        courses_dict = {'Period':array_periodo,'Aproved':array_aprobados,'Failed':array_reprobados,'Canceled':array_cancelados}
        courses_df = pd.DataFrame(courses_dict)


        fig = px.bar(courses_df, 
                     x='Period',
                     y=['Aproved','Failed','Canceled'],
                     labels = {'value':'Number of courses'})
        fig.update_layout(
            title_text='Courses enrolled per period',
            title_x=0.5,
            autosize=False,
            width=350,
            height=300,
            margin=dict(
                l=20,
                r=20,
                b=20,
                t=30
            ),
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text'],
        )

        lineplot = go.Figure()
        lineplot.add_trace(go.Scatter(x=array_periodo[:len(array_promedio)], y=array_matriculados,
                                 mode='lines',
                                 name='Matriculados'))
        lineplot.add_trace(go.Scatter(x=array_periodo[:len(array_promedio)], y=array_reprobados,
                                 mode='lines',
                                 name='Reprobados'))
        lineplot.add_trace(go.Scatter(x=array_periodo[:len(array_promedio)], y=array_cancelados,
                                 mode='lines',
                                 name='Cancelados'))
        lineplot.update_layout(
            title_text='Courses enrolled per period',
            title_x=0.5,
            xaxis_title="Period",
            yaxis_title="Number of courses",
            autosize=False,
            width=350,
            height=300,
            margin=dict(
                l=20,
                r=20,
                b=20,
                t=30
            ),
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text'],
        )
        #prob dropout
        probabilidad = float(new_df.loc[student_selected,'probabilidad'])
        dropout = px.pie(values = [probabilidad,1-probabilidad],names =['dropout','No dropout'])
        dropout.update_layout(
            title_text = 'Prob dropout',
            title_x = 0.5,
            autosize=False,
            width=350,
            height=275,
            margin=dict(
                l=20,
                r=20,
                b=20,
                t=30
            ),
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text'],
        )

        return [barplot, fig,lineplot, dropout]



###########################
##### THIRD PAGE #########
###########################

#We create the same structure of the navbar
navbar3 = dbc.Navbar(
    [
  
        dbc.NavbarToggler(id="navbar-toggler1"),
        dbc.Collapse(
            dbc.Row(
                [
                       dbc.Col(html.Img(src=app.get_asset_url("icono.png"), height="40px")),
                       dbc.NavItem(dbc.NavLink("Review page",  href="/general")),
                       dbc.NavItem(dbc.NavLink("Student's page",  href="/students")),
                       dbc.NavItem(dbc.NavLink("Map page", disabled=True, href="#")),
                       dbc.NavItem(dbc.NavLink("view's page",  href="/view"))

                ],
                className="mr-auto",
            ),
            id="navbar-collapse1",
            navbar=True,
        ),
    ]
)


####################################################
# We organize the components of the map page
####################################################
map_page= html.Div(
    [navbar3, header_map.header_map,sidebar.sidebar,mapcolombia.mapcolombia],
    className="ds4a-app", 
)

######################################################################################
#We define the interactivity for the map page, it has the same structure of review page 
#review, the map is updated taking into account any filter applied.
######################################################################################
@app.callback(
    [
    Output("total_students_map",'children'),
    Output("active_students_map",'children'),
    Output("inactive_students_map",'children'),
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

    
    # we create the Map taking account the json file.
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



###########################
####### Four Page #########
###########################

# We define the navbar 
navbar4 = dbc.Navbar(
    [
        dbc.NavbarToggler(id="navbar-toggler1"),
        dbc.Row([    
                       dbc.Col(html.Img(src=app.get_asset_url("icono.png"), height="40px")),
                       dbc.NavItem(dbc.NavLink("Review page",  href="/general")),
                       dbc.NavItem(dbc.NavLink("Student's page",  href="/students")),
                       dbc.NavItem(dbc.NavLink("Map page", href="/map")),
                       dbc.NavItem(dbc.NavLink("view's Page",disabled=True, href="#"))

                        
                    ],
                    className="mr-auto",
            ),
    ]
)

####################################################
# We organize the components of the view page
####################################################

view = html.Div(
    [navbar4, header_prob.header_prob, sidebar_prob.sidebar_prob, prob.prob],
    className="ds4a-app", 
)

#we define interactivity
@app.callback(
    [Output("graph1", "figure"),
    Output("graph2", "figure"),
    Output("graph3", "figure"),
    Output("graph4", "figure"),
    Output("total_students3",'children'),
    Output("percentage_students",'children'),
    Output("probability_average",'children')
    ],
    [Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'),
    Input('RangeSlider_age', 'value'),
    Input('Dropdown_maritalstatus','value'),     
    Input('Dropdown_stratum','value'),           
    Input('Dropdown_sex','value'),
    Input('Dropdown_modality','value'),
    Input('Dropdown_country','value'),
    Input('Dropdown_city','value')
    ])

def update_output(start_date, end_date, edad, var1,var2,var3,var4,var5,var6):
    dff = (df[(df['fecha_ingreso'] >= start_date) & (df['fecha_ingreso'] < end_date)
    & (df['edad'] >= edad[0]) & (df['edad'] < edad[1]) 
    & (df['estado_civil'].isin([var1]) == True if var1 != None else df['estado_civil'].isin([var1]) == False)
    & (df['estrato'].isin([var2]) == True if var2 != None else df['estrato'].isin([var2]) == False)
    & (df['sexo'].isin([var3]) == True if var3 != None else df['sexo'].isin([var3]) == False)
    & (df['modalidad'].isin([var4]) == True if var4 != None else df['modalidad'].isin([var4]) == False)
    & (df['pais_residencia'].isin([var5]) == True if var5 != None else df['pais_residencia'].isin([var5]) == False)
    & (df['ciudad_residencia'].isin([var6]) == True if var6 != None else df['ciudad_residencia'].isin([var6]) == False)
    & (df['estado_plan_estudio'].isin(['Activo']) == True if 'Activo'!= None else df['estado_plan_estudio'].isin(['Activo']) == False)
    ])
    
    colors = {
    'background': '#1f2630',
    'text': '#7FDBFF'
    }

    total_students = len(dff)
    percentage=str(round((total_students/18592)*100,4))+' %'
    prob_average=round(dff['probabilidad'].mean(),4)
    dfp1 = (dff.groupby(["ciudad_residencia"]).mean()[["probabilidad"]].sort_values(by = ['probabilidad'], ascending = False).reset_index().head(10))
    
    
    
    ##graphs
    if dff.empty:
        graph1 = px.histogram(dff,x='probabilidad', height=300,
                               labels={'modalidad':'Modality',
                                      'probabilidad':'Probability'})
    else:
        graph1 = px.histogram(dff,x='probabilidad',color='modalidad', height=300,
                        labels={'modalidad':'Modality',
                                'probabilidad':'Probability'})


    graph1.update_layout(
            title_text='Probability per modality',
            title_x=0.5,
            autosize=False,
            width=450,
            height=280,
            margin=dict(
                l=20,
                r=20,
                b=20,
                t=30
            ),
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text'],
        )
    graph2 = px.box(dff,y='probabilidad',x='estrato', height=300,
                               labels={'estrato':'Stratum',
                                      'probabilidad':'Probability'})
    
    graph2.update_layout(
            title_text='Probability per stratum',
            title_x=0.5,
            autosize=False,
            width=450,
            height=280,
            margin=dict(
                l=20,
                r=20,
                b=20,
                t=30
            ),
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text'],
        )
    graph3 = px.violin(dff,x='probabilidad',y='sexo', height=300,
                               labels={'probabilidad':'Probability',
                                      'sexo':'Gender'})
    
    graph3.update_layout(
            title_text='Probability per gender',
            title_x=0.5,
            autosize=False,
            width=450,
            height=280,
            margin=dict(
                l=20,
                r=20,
                b=20,
                t=30
            ),
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text'],
        )
    graph4 = px.bar(dfp1,y='probabilidad',x='ciudad_residencia', height=300,
                               labels={'ciudad_residencia':'City of residence',
                                      'probabilidad':'Probability'})
    
    graph4.update_layout(
            title_text='Most probability dropout cities',
            title_x=0.5,
            autosize=False,
            width=450,
            height=280,
            margin=dict(
                l=20,
                r=20,
                b=20,
                t=30
            ),
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text'],
        )

    return [graph1,graph2,graph3,graph4,total_students, percentage,prob_average]



#########################################################################################
#We define the interactivity of the application that allows navigation between pages 
# according to the link selected.
########################################################################################
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])



def display_page(pathname):
    if pathname == '/students':
        return student_page
    elif pathname == '/map':
        return map_page
    elif pathname == '/view':
        return view
    else:
        return review_page
 

if __name__ == "__main__":
    app.run_server(debug=True)